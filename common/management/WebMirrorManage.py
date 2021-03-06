
import calendar
import datetime
import json
import os
import os.path
import datetime
import traceback
from concurrent.futures import ThreadPoolExecutor

import urllib.error
import urllib.parse

from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import or_
from sqlalchemy.sql import func
from sqlalchemy.orm import outerjoin
import sqlalchemy.exc
import sqlalchemy.orm.exc
from sqlalchemy_continuum.utils import version_table

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

from WebMirror.Engine import SiteArchiver
import WebMirror.OutputFilters.util.feedNameLut as feedNameLut
import WebMirror.rules
import WebMirror.SiteSync.fetch
import WebMirror.SpecialCase
import WebMirror.NewJobQueue

import RawArchiver.RawActiveModules
import RawArchiver.RawEngine

import common.database as db
import common.Exceptions
import common.management.file_cleanup
import common.management.util
import common.global_constants
import common.util.webFunctions as webFunctions

import Misc.HistoryAggregator.Consolidate
import Misc.NuForwarder.NuHeader
import flags
import config
from config import C_RAW_RESOURCE_DIR


import WebMirror.TimedTriggers.RollingRewalkTrigger
import WebMirror.TimedTriggers.QueueTriggers
import WebMirror.SiteSync.fetch
import WebMirror.OutputFilters.rss.FeedDataParser



def exposed_remote_fetch_enqueue(url):
	'''
	Place a normal fetch request for url `url` into the remote fetch queue.

	Requires the FetchAgent service to be running.
	'''

	print("Enqueueing ")
	trig = WebMirror.TimedTriggers.QueueTriggers.NuQueueTrigger()
	trig.enqueue_url(url)

def exposed_trigger_nu_homepage_fetch():
	'''
	Trigger testing for the QueueTrigger system
	'''
	trig = WebMirror.TimedTriggers.QueueTriggers.NuQueueTrigger()
	trig.go()

def exposed_do_nu_head_cycle():
	'''
	Do a fetch and wait for results session through the NU Header system.
	'''
	Misc.NuForwarder.NuHeader.fetch_and_flush()


def exposed_fetch(url, debug=True, rss_debug=False):
	'''
	Do a synchronous fetch of content from url `url`.
	'''

	# try:
	# 	WebMirror.SpecialCase.startAmqpFetcher()
	# except RuntimeError:  # Fetcher already started
	# 	pass

	if rss_debug:
		print("Debugging RSS")
		flags.RSS_DEBUG = True

	parsed = urllib.parse.urlparse(url)
	root = urllib.parse.urlunparse((parsed[0], parsed[1], "", "", "", ""))

	new = db.WebPages(
		url       = url,
		starturl  = root,
		netloc    = parsed.netloc,
		distance  = 50000,
		is_text   = True,
		priority  = 500000,
		type      = 'unknown',
		fetchtime = datetime.datetime.now(),
		)

	if debug:
		print(new)

	try:
		with db.session_context() as sess:
			archiver = SiteArchiver(None, sess, None)
			archiver.synchronousJobRequest(url, ignore_cache=True)
	except Exception as e:
		traceback.print_exc()

def exposed_fetch_silent(tgt):
	'''
	Identical to `test_retrieve`, except debug printing is supressed.
	'''
	exposed_fetch(tgt, debug=False)


def exposed_raw_test_retrieve(url):
	'''
	Lower level fetch test, otherwise similar to `test_retreive`
	'''

	# try:
	# 	WebMirror.SpecialCase.startAmqpFetcher()
	# except RuntimeError:  # Fetcher already started
	# 	pass


	parsed = urllib.parse.urlparse(url)
	root = urllib.parse.urlunparse((parsed[0], parsed[1], "", "", "", ""))


	with db.session_context() as sess:

		row = sess.query(db.RawWebPages).filter(db.RawWebPages.url == url).scalar()
		if row:
			row.state = 'new'
		else:
			row = db.RawWebPages(
				url       = url,
				starturl  = root,
				netloc    = parsed.netloc,
				distance  = 50000,
				priority  = 500000,
				state     = 'new',
				fetchtime = datetime.datetime.now(),
				)
			sess.add(row)


		try:
			archiver = RawArchiver.RawEngine.RawSiteArchiver(
				total_worker_count = 1,
				worker_num         = 0,
				new_job_queue      = None,
				cookie_lock        = None,
				db_interface       = sess,
				response_queue     = None
				)
			archiver.do_job(row)
		except Exception as e:
			traceback.print_exc()

def exposed_longest_rows():
	'''
	Fetch the rows from the database where the `content` field is longest.
	Return is limited to the biggest 50 rows.
	VERY SLOW (has to scan the entire table)
	'''
	with db.session_context() as sess:
		print("Getting longest rows from database")
		have = sess.execute("""
			SELECT
				id, url, length(content), content
			FROM
				web_pages
			ORDER BY
				LENGTH(content) DESC NULLS LAST
			LIMIT 50;
			""")
		print("Rows:")
		savepath = "./large_files/"
		for row in have:
			print(row[0], row[1])
			try:
				os.makedirs(savepath)
			except FileExistsError:
				pass
			with open(os.path.join(savepath, "file %s.txt" % row[0]), "wb") as fp:
				urlst = "URL: %s\n\n" % row[1]
				size = "Length: %s\n\n" % row[2]
				fp.write(urlst.encode("utf-8"))
				fp.write(size.encode("utf-8"))
				fp.write("{}".format(row[3]).encode("utf-8"))

def exposed_fix_null():
	'''
	Reset any rows in the table where the `ignoreuntiltime` column
	is null. Updates in 50K row increments.11
	'''
	step = 50000

	with db.session_context() as sess:
		end = sess.execute("""SELECT MAX(id) FROM web_pages WHERE  ignoreuntiltime IS NULL;""")
		end = list(end)[0][0]

		start = sess.execute("""SELECT MIN(id) FROM web_pages WHERE ignoreuntiltime IS NULL;""")
		start = list(start)[0][0]

		changed = 0

		if not start:
			print("No null rows to fix!")
			return

		start = start - (start % step)

		for x in range(start, end, step):
			# SQL String munging! I'm a bad person!
			# Only done because I can't easily find how to make sqlalchemy
			# bind parameters ignore the postgres specific cast
			# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
			have = sess.execute("""UPDATE web_pages SET ignoreuntiltime = 'epoch'::timestamp WHERE ignoreuntiltime IS NULL AND id < %s AND id >= %s;""" % (x, x-step))
			# print()
			print('%10i, %7.4f, %6i' % (x, x/end * 100, have.rowcount))
			changed += have.rowcount
			if changed > 10000:
				print("Committing (%s changed rows)...." % changed, end=' ')
				sess.commit()
				print("done")
				changed = 0
		sess.commit()


def delete_internal(sess, ids, netloc, badwords):

	if ids:
		print("Updating for netloc(s) %s. %s rows requiring update." % (netloc, len(ids)))
	else:
		print("No rows needing retriggering for netloc %s." % (netloc))

	chunk_size = 5000
	for chunk_idx in range(0, len(ids), chunk_size):
		chunk = ids[chunk_idx:chunk_idx+chunk_size]
		while 1:
			try:
				ctbl = version_table(db.WebPages)

				# Allow ids that only exist in the history table by falling back to a
				# history-table query if the main table doesn't have the ID.
				try:
					ex = sess.query(db.WebPages.url).filter(db.WebPages.id == chunk[0]).one()[0]
				except sqlalchemy.orm.exc.NoResultFound:
					try:
						ex = sess.query(ctbl.c.url).filter(ctbl.c.id == chunk[0]).all()[0][0]
					except IndexError:
						ex = None

				triggered = [tmp for tmp in badwords if tmp in ex]
				print("Example removed URL: '%s'" % (ex))
				print("Triggering badwords: '%s'" % triggered)
				assert triggered


				q1 = sess.query(db.WebPages).filter(db.WebPages.id.in_(chunk))
				affected_rows_main = q1.delete(synchronize_session=False)

				q2 = sess.query(ctbl).filter(ctbl.c.id.in_(chunk))
				affected_rows_ver = q2.delete(synchronize_session=False)

				sess.commit()
				print("Deleted %s rows (%s version table rows) for netloc %s. %0.2f%% done." %
						(affected_rows_main, affected_rows_ver, netloc, 100 * ((chunk_idx) / len(ids))))
				break
			except sqlalchemy.exc.InternalError:
				print("Transaction error (sqlalchemy.exc.InternalError). Retrying.")
				sess.rollback()
			except sqlalchemy.exc.OperationalError:
				print("Transaction error (sqlalchemy.exc.OperationalError). Retrying.")
				sess.rollback()
			except sqlalchemy.exc.IntegrityError:
				print("Transaction error (sqlalchemy.exc.IntegrityError). Retrying.")
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				print("Transaction error (sqlalchemy.exc.InvalidRequestError). Retrying.")
				traceback.print_exc()
				sess.rollback()


def exposed_purge_invalid_urls(selected_netloc=None):
	'''
	Iterate over each ruleset in the rules directory, and generate a compound query that will
	delete any matching rows.
	For rulesets with a large number of rows, or many badwords, this
	can be VERY slow.

	Similar in functionality to `clear_bad`, except it results in many fewer queryies,
	and is therefore likely much more performant.
	'''
	with db.session_context() as sess:
		for ruleset in WebMirror.rules.load_rules():

			if      (
							(ruleset['netlocs'] and ruleset['badwords'])
						and
						(
							(ruleset['netlocs'] and ruleset['badwords'] and selected_netloc is None)
							or
							(selected_netloc != None and selected_netloc in ruleset['netlocs'])
						)
					):

				agg_bad = [tmp for tmp in ruleset['badwords']]
				agg_bad.extend(common.global_constants.GLOBAL_BAD_URLS)

				# So there's no way to escape a LIKE string in postgres.....
				search_strs = ["%{}%".format(badword.replace(r"_", r"\_").replace(r"%", r"\%").replace(r"\\", r"\\")) for badword in agg_bad]

				print("Badwords:")
				for bad in search_strs:
					print("	Bad: ", bad)
				print("Netlocs:")
				print(ruleset['netlocs'])

				# We have to delete from the normal table before the versioning table,
				# because deleting from the normal table causes inserts into the versioning table
				# due to the change tracking triggers.


				ands = [
						or_(*(db.WebPages.url.like(ss) for ss in search_strs))
					]

				if selected_netloc:
					print("Doing specific netloc filtering!")
					ands.append((db.WebPages.netloc == selected_netloc))
				else:
					print("Filtering by all netlocs in rule file.")
					ands.append(db.WebPages.netloc.in_(ruleset['netlocs']))


				loc = and_(*ands)
				# print("Doing count on table ")
				# count = sess.query(db.WebPages) \
				# 	.filter(or_(*opts)) \
				# 	.count()

				ids = sess.query(db.WebPages.id) \
					.filter(loc)                 \
					.all()

				ids = set(ids)

				if ids == 0:
					print("{num} items match badwords from file {file}. No deletion required ".format(file=ruleset['filename'], num=len(ids)))
				else:
					print("{num} items match badwords from file {file}. Deleting ".format(file=ruleset['filename'], num=len(ids)))


				# Returned list of IDs is each ID packed into a 1-tuple. Unwrap those tuples so it's just a list of integer IDs.
				ids = [tmp[0] for tmp in ids]
				delete_internal(sess, ids, selected_netloc if selected_netloc else ruleset['netlocs'], agg_bad)


def exposed_purge_invalid_url_history():
	'''
	Functionally identical to `purge_invalid_urls`, but
	operates on the history table only.

	This means that it will operate on row IDs that have been deleted from the main DB (intentionally or not)
	'''

	with db.session_context() as sess:
		ctbl = version_table(db.WebPages)
		for ruleset in WebMirror.rules.load_rules():

			if ruleset['netlocs'] and ruleset['badwords']:

				agg_bad = [tmp for tmp in ruleset['badwords']]
				agg_bad.extend(common.global_constants.GLOBAL_BAD_URLS)

				# So there's no way to escape a LIKE string in postgres.....
				search_strs = ["%{}%".format(badword.replace(r"_", r"\_").replace(r"%", r"\%").replace(r"\\", r"\\")) for badword in agg_bad]

				print("Badwords:")
				for bad in search_strs:
					print("	Bad: ", bad)
				print("Netlocs:")
				print(ruleset['netlocs'])

				# We have to delete from the normal table before the versioning table,
				# because deleting from the normal table causes inserts into the versioning table
				# due to the change tracking triggers.


				ands = [
						or_(*(ctbl.c.url.like(ss) for ss in search_strs))
					]

				print("Filtering by all netlocs in rule file.")
				ands.append(ctbl.c.netloc.in_(ruleset['netlocs']))


				ids = sess.query(ctbl.c.id) \
					.filter(and_(*ands))                 \
					.all()

				# Collapse duplicates
				ids = set(ids)

				if ids == 0:
					print("{num} items match badwords from file {file}. No deletion required ".format(file=ruleset['filename'], num=len(ids)))
				else:
					print("{num} items match badwords from file {file}. Deleting ".format(file=ruleset['filename'], num=len(ids)))


				# Returned list of IDs is each ID packed into a 1-tuple. Unwrap those tuples so it's just a list of integer IDs.
				ids = [tmp[0] for tmp in ids]
				delete_internal(sess, ids, ruleset['netlocs'], ruleset['badwords'])


def exposed_db_count_netlocs():
	'''
	Select and count the number of instances for each netloc in
	the database.

	Returns the netlocs sorted by count in decending order.
	'''

	with db.session_context() as sess:
		q = sess.query(db.WebPages.netloc, func.count(db.WebPages.netloc).label("count")) \
			.group_by(db.WebPages.netloc)\
			.order_by(desc(func.count(db.WebPages.netloc)))
		print("Doing query.")
		res = q.all()
		res = list(res)
		for row in res:
			print("Row: ", row)

		with open("nl_counts.json", "w") as fp:
			json.dump(res, fp)




def exposed_filter_links(path):
	"""
	Filter a file of urls at `path`. If a url in the file
	is not already a start url in the mirror system, it
	is printed to the console.
	"""
	if not os.path.exists(path):
		raise IOError("File at path '%s' doesn't exist!" % path)

	with open(path, "r") as fp:
		urls = fp.readlines()
	urls = [item.strip() for item in urls if item.strip()]

	# print(urls)

	havestarts = []
	for ruleset in WebMirror.rules.load_rules():
		if ruleset['starturls']:
			havestarts += ruleset['starturls']

	for item in urls:
		if item not in havestarts:
			print(item)


def exposed_fetch_titles(url_file):
	'''
	Fetch a set of urls, and print the page title for each
	'''
	with open(url_file, "r") as fp:
		content = fp.readlines()



	wg = webFunctions.WebGetRobust()


	for url in content:
		meta = common.management.util.get_page_title(wg, url)
		print('Missing: "%s" %s: "%s",' % (url, " " * (50 - len(url)), meta))


	print(content)


def exposed_nu_fetch_sources():
	'''
	Fetch the active sources from NovelUpdates
	'''
	names = WebMirror.SiteSync.fetch.fetch_other_sites()
	for name in names:
		print("	- ", name)


def exposed_nu_new_from_feeds(fetch_title=False):
	'''
	Parse outbound netlocs from NovelUpdates releases, extracting
	any sites that are not known in the feednamelut.
	'''

	rules = WebMirror.rules.load_rules()
	urls = [item['starturls'] if item['starturls'] else [] + item['feedurls'] if item['feedurls'] else [] for item in rules]
	urls = [item for sublist in urls for item in sublist]

	starturldict = {WebMirror.OutputFilters.util.feedNameLut.patch_blogspot(urllib.parse.urlsplit(url).netloc) : url for url in urls}


	wg = webFunctions.WebGetRobust()

	with db.session_context() as sess:

		nu_items = sess.query(db.NuReleaseItem)             \
			.filter(db.NuReleaseItem.validated == True)     \
			.filter(db.NuReleaseItem.actual_target != None) \
			.all()

		mapdict = {WebMirror.OutputFilters.util.feedNameLut.patch_blogspot(urllib.parse.urlsplit(row.actual_target).netloc) : row.actual_target for row in nu_items}
		print("Nu outbound items: ", len(mapdict))

		# Some sites have gone down or are now squatters.
		# Mask them off.
		mask_netlocs = [
			'endofdays42.ph.tn',
			'endofdays42.000webhostapp.com',
			'host307.hostmonster.com',
			'plus.google.com',

			'thundertranslations.com',
			'ww1.thundertranslations.com',
			'ww12.thundertranslations.com',
			'ww2.thundertranslations.com',

			'hugginglovetranslations.heliohost.org',
			'suspendeddomain.org',
			'www.facebook.com',
			'www.testing.wuxiaworld.com',

			'www.patreon.com',
			'wordpress.com',
			'forum.gravitytales.com',
			'www.wangkaiinternational.com',    # Some garbage korean soap opera actor's website?

			'drive.google.com',
			'gakno.com.mx',          # Mexican food manufacturer?

			'kitakamiooi.com',   # Redirects to www.kitakamiooi.com
			'kanojo.eu',

			'www.tumblr.com',


			# In the LUT already
			'catatopatch.wixsite.com',
			'kitsune.club',   # Also failing DNS resolution
			'uncommittedtranslations.bravesites.com',

			'www.optranslations.net',  # Ded
			'steadytranslation.com',
			'translatinotaku.ml',
			'www.worldofwatermelons.com',
			'ww5.worldofwatermelons.com',

			# Manga site?
			'ckmscans.halofight.com',
		]

		missing = 0
		for netloc, tgturl in mapdict.items():

			if netloc in mask_netlocs:
				continue

			if WebMirror.OutputFilters.util.feedNameLut.getNiceName(sess, None, netloc):
				continue

			if netloc in starturldict:
				continue


			WebMirror.OutputFilters.util.feedNameLut.getNiceName(sess, None, netloc)
			title = netloc
			if fetch_title:
				title = common.management.util.get_page_title(wg, tgturl)
			print("Missing: ", (netloc, title, tgturl))
			missing += 1
		print("Nu outbound items: ", len(mapdict), "missing:", missing)

def exposed_find_dead_netlocs():
	'''
	Try to fetch each URL in the available netlocs and see if they're valid.
	'''
	pass


def exposed_fetch_other_feed_sources():
	'''
	Walk the listed pages for both AhoUpdates and NovelUpdates,
	retreiving a list of the translators from each.
	'''
	WebMirror.SiteSync.fetch.fetch_other_sites()


def exposed_fix_missing_history():
	'''
	Fix any items that don't have an entry in the history table.
	'''
	Misc.HistoryAggregator.Consolidate.fix_missing_history()

def exposed_flatten_history():
	'''
	Flatten the page change history.
	This limits the retained page versions to one-per-hour for the
	last 48 hours, once per day for the last 32 days, and once per
	week after that.
	'''
	Misc.HistoryAggregator.Consolidate.consolidate_history()

def exposed_flatten_fix_missing_history():
	'''
	Functionally equivalent to `flatten_history`, `fix_missing_history`
	'''
	Misc.HistoryAggregator.Consolidate.consolidate_history()
	Misc.HistoryAggregator.Consolidate.fix_missing_history()


def exposed_test_new_job_queue():
	'''
	Testing function for NewJobQueue components
	'''

	instance = WebMirror.NewJobQueue.JobAggregatorInternal(None, None)

	want = instance.outbound_job_wanted("www.novelupdates.com", "http://www.novelupdates.com/")
	print(want)
	want = instance.outbound_job_wanted("twitter.com", "https://twitter.com/Baka_Tsuki")
	print(want)
	want = instance.outbound_job_wanted("twitter.com", "https://twitter.com/Nano_Desu_Yo")
	print(want)


def exposed_drop_priorities():
	'''
	Reset the priority of every row in the table to the IDLE_PRIORITY level
	'''

	step  = 10000

	with db.session_context() as sess:
		print("Getting minimum row in need or update..")
		start = sess.execute("""SELECT min(id) FROM web_pages WHERE priority != 500000""")
		start = list(start)[0][0]
		print("Minimum row ID: ", start, "getting maximum row...")
		stop = sess.execute("""SELECT max(id) FROM web_pages WHERE priority != 500000""")
		stop = list(stop)[0][0]
		print("Maximum row ID: ", stop)

		if not start:
			print("No null rows to fix!")
			return

		print("Need to fix rows from %s to %s" % (start, stop))
		start = start - (start % step)

		changed = 0
		for idx in range(start, stop, step):
			try:
				# SQL String munging! I'm a bad person!
				# Only done because I can't easily find how to make sqlalchemy
				# bind parameters ignore the postgres specific cast
				# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
				have = sess.execute("""update web_pages set priority = 500000 where priority != 500000 AND id > {} AND id <= {};""".format(idx, idx+step))
				# print()

				processed  = idx - start
				total_todo = stop - start
				print('%10i, %10i, %7.4f, %6i' % (idx, stop, processed/total_todo * 100, have.rowcount))
				changed += have.rowcount
				if changed > step:
					print("Committing (%s changed rows)...." % changed, end=' ')
					sess.commit()
					print("done")
					changed = 0

			except sqlalchemy.exc.OperationalError:
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				sess.rollback()


		sess.commit()


def unwrap_ret(ret):

	ret = list(ret)
	if not ret:
		print("Not list ret!", list(ret))
		return 0

	if not ret[0]:
		print("Not ret[0]", ret[0])
		return 0
	if not ret[0][0]:
		print("Coercing to zero?")
		return 0
	print("Returning ret[0][0]: ", ret[0][0])
	return ret[0][0]

def delete_by_netloc_internal(netloc):
	'''
	List netlocs from database that aren't in the rules.
	'''

	step  = 10000

	with db.session_context() as sess:
		print("Getting minimum row in need or update..")
		start = sess.execute("""SELECT min(id) FROM web_pages WHERE netloc = :nl""", {"nl":netloc})
		start = unwrap_ret(start)
		print("Minimum row ID: ", start, "getting maximum row...")
		stop = sess.execute("""SELECT max(id) FROM web_pages WHERE netloc = :nl""", {"nl":netloc})
		stop = unwrap_ret(stop)
		print("Maximum row ID: ", stop)

		startv = sess.execute("""SELECT min(id) FROM web_pages_version WHERE netloc = :nl""", {"nl":netloc})
		startv = unwrap_ret(startv)
		print("Minimum version row ID: ", startv, "getting maximum version row...")
		stopv = sess.execute("""SELECT max(id) FROM web_pages_version WHERE netloc = :nl""", {"nl":netloc})
		stopv = unwrap_ret(stopv)
		print("Maximum version row ID: ", stopv)

		if not (start or startv) :
			print("No null rows to fix!")
			return

		print("Need to fix rows from %s to %s" % (start, stop))
		print("Need to fix version rows from %s to %s" % (startv, stopv))
		start = start - (start % step)

		changed = 0
		for idx in range(start, stop, step):
			try:
				# SQL String munging! I'm a bad person!
				# Only done because I can't easily find how to make sqlalchemy
				# bind parameters ignore the postgres specific cast
				# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
				have = sess.execute("""DELETE FROM web_pages WHERE netloc = :nl AND id > :idmin AND id <= :idmax;""", {'idmin':idx, 'idmax':idx+step, 'nl':netloc})
				# print()

				processed  = idx - start
				total_todo = stop - start
				print('%10i, %10i, %7.4f, %6i' % (idx, stop, processed/total_todo * 100, have.rowcount))
				changed += have.rowcount
				if changed > step:
					print("Committing (%s changed rows)...." % changed, end=' ')
					sess.commit()
					print("done")
					changed = 0

			except sqlalchemy.exc.OperationalError:
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				sess.rollback()


		changed = 0
		for idx in range(startv, stopv, step):
			try:
				# SQL String munging! I'm a bad person!
				# Only done because I can't easily find how to make sqlalchemy
				# bind parameters ignore the postgres specific cast
				# The id range forces the query planner to use a much smarter approach which is much more performant for small numbers of updates
				have = sess.execute("""DELETE FROM web_pages_version WHERE netloc = :nl AND id > :idmin AND id <= :idmax;""", {'idmin':max(idx-1, 0), 'idmax':idx+step+1, 'nl':netloc})
				# print()

				processed  = idx - startv
				total_todo = stopv - startv
				print('%10i, %10i, %7.4f, %6i' % (idx, stopv, processed/total_todo * 100, have.rowcount))
				changed += have.rowcount
				if changed > step:
					print("Committing (%s changed rows)...." % changed, end=' ')
					sess.commit()
					print("done")
					changed = 0

			except sqlalchemy.exc.OperationalError:
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				sess.rollback()

		sess.commit()

def exposed_delete_transactions():
	'''
	List netlocs from database that aren't in the rules.
	'''

	with db.session_context() as sess:

		print("Getting minimum transaction table date..")
		start = sess.execute("""SELECT min(issued_at) FROM transaction""")
		start = unwrap_ret(start)
		print("Minimum transaction time: ", start, "getting maximum transaction table date...")
		stop = sess.execute("""SELECT max(issued_at) FROM transaction""")
		stop = unwrap_ret(stop)
		print("Maximum transaction time: ", stop)

		step = datetime.timedelta(hours=8)
		mind = start
		while mind < stop:
			print("Doing delete from %s to %s" % (mind, mind+step))

			have = sess.execute("""DELETE FROM transaction WHERE issued_at >= :startd AND issued_at <= :stopd;""", {'startd':mind, 'stopd':mind+step})
			print('Deleted %6i rows. Committing...' % (have.rowcount, ))
			sess.commit()
			print('Comitted')

			# print()


			mind += step


def exposed_delete_netlocs():
	'''
	List netlocs from database that aren't in the rules.
	'''
	rm = [
		'www.wattpad.com',                                                                                     # - [(2,)]
		'www.booksie.com',                                                                                     # - [(4369566,)]
	]


	with db.session_context() as sess:
		print("Doing web_pages delete")
		have = sess.execute("""DELETE FROM web_pages WHERE netloc = 'www.wattpad.com' OR netloc = 'www.booksie.com';""")
		print("Deleted %s rows. committing" % have.rowcount)
		sess.commit()
		print("Doing web_pages_version delete")
		have = sess.execute("""DELETE FROM web_pages_version WHERE netloc = 'www.wattpad.com' OR netloc = 'www.booksie.com';""")
		print("Deleted %s rows. committing" % have.rowcount)
		sess.commit()
		print("Done!")



def exposed_rolling_rewalk():

	run = WebMirror.TimedTriggers.RollingRewalkTrigger.RollingRewalkTriggerBase()
	run._go()


def exposed_rewalk_all_old():

	run = WebMirror.TimedTriggers.RollingRewalkTrigger.RollingRewalkTriggerBase()
	run.retrigger_other()





def exposed_nu_retrigger_series_pages():
	'''

	'''
	step = 500000

	with db.session_context() as sess:
		end = sess.execute("""SELECT MAX(id) FROM web_pages;""")
		end = list(end)[0][0]

		start = sess.execute("""SELECT MIN(id) FROM web_pages;""")
		start = list(start)[0][0]

		changed = 0

		if not start:
			print("No null rows to fix!")
			return

		start = start - (start % step)

		for x in range(start, end, step):

			have = sess.execute("""UPDATE web_pages SET state='new', priority=50000 WHERE url LIKE 'http://www.novelupdates.com/series/%%/' AND id < %s AND id >= %s AND state != 'new';""" % (x, x-step))

			print('%10i, %7.4f, %6i, %6i' % (x, x/end * 100, have.rowcount, changed))
			changed += have.rowcount
			if changed > 100:
				print("Committing (%s changed rows)...." % changed, end=' ')
				sess.commit()
				print("done")
				changed = 0
		sess.commit()


