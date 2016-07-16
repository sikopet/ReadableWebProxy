

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import WebMirror.rules
import WebMirror.SpecialCase
import WebMirror.LogBase as LogBase
import runStatus
import queue
import time
import os.path
import os
import sys
import sqlalchemy.exc
import random
import settings
import pprint

import Misc.diff_match_patch as dmp
from sqlalchemy import desc

from sqlalchemy.sql import text
from sqlalchemy import distinct
from sqlalchemy.dialects import postgresql

import WebMirror.util.urlFuncs
import urllib.parse
import traceback
import datetime

from sqlalchemy.sql import text
from sqlalchemy.sql import func
import WebMirror.util.webFunctions as webFunctions

import hashlib
from WebMirror.Exceptions import DownloadException
import WebMirror.Fetch
import WebMirror.database as db
from config import C_RESOURCE_DIR


if "debug" in sys.argv:
	CACHE_DURATION = 1
	RSC_CACHE_DURATION = 1
	# CACHE_DURATION = 60 * 5
	# RSC_CACHE_DURATION = 60 * 60 * 5
else:
	CACHE_DURATION = 60 * 60 * 24 * 7
	RSC_CACHE_DURATION = 60 * 60 * 24 * 147



GLOBAL_BAD = [
			'/xmlrpc.php',
			'gprofiles.js',
			'netvibes.com',
			'accounts.google.com',
			'edit.yahoo.com',
			'add.my.yahoo.com',
			'public-api.wordpress.com',
			'r-login.wordpress.com',
			'twitter.com',
			'facebook.com',
			'public-api.wordpress.com',
			'wretch.cc',
			'ws-na.amazon-adsystem.com',
			'delicious.com',
			'paypal.com',
			'digg.com',
			'topwebfiction.com',
			'/page/page/',
			'addtoany.com',
			'stumbleupon.com',
			'delicious.com',
			'/comments/feed/',
			'fbcdn-',
			'/wp-json/',
			'reddit.com',
			'/osd.xml',
			'/wp-login.php',
			'?openidserver=1',
			'newsgator.com',
			'technorati.com',
			'pixel.wp.com',
			'a.wikia-beacon.com',
			'b.scorecardresearch.com',
			'//mail.google.com',
			'javascript:void',
			'twitter.com/intent/',
			'www.pinterest.com/pin/',
			'www.wattpad.com/login?',
			'/embed?',

			# Tumblr can seriously go fuck itself with a rusty stake
			'tumblr.com/widgets/',
			'www.tumblr.com/login',
			'://tumblr.com',
			'&share=tumblr',

			'/wp-content/plugins/',
			'/wp-content/themes/',
			'/wp-json/oembed/',

			# At least one site (booksie) is serving the favicon with a mime-type
			# of "text/plain", which then confuses the absolute crap out of the
			# mime-type dispatcher.
			# Since I'm not re-serving favicons anyways, just do not fetch them ever.
			'favicon.ico',

			# Try to not scrape inline images
			';base64,',
	]



def getHash(fCont):

	m = hashlib.md5()
	m.update(fCont)
	return m.hexdigest()




def saveCoverFile(filecont, fHash, filename):
	# use the first 3 chars of the hash for the folder name.
	# Since it's hex-encoded, that gives us a max of 2^12 bits of
	# directories, or 4096 dirs.
	fHash = fHash.upper()
	dirName = fHash[:3]

	dirPath = os.path.join(C_RESOURCE_DIR, dirName)
	if not os.path.exists(dirPath):
		os.makedirs(dirPath)

	ext = os.path.splitext(filename)[-1]
	ext   = ext.lower()

	# The "." is part of the ext.
	filename = '{filename}{ext}'.format(filename=fHash, ext=ext)


	# The "." is part of the ext.
	filename = '{filename}{ext}'.format(filename=fHash, ext=ext)

	# Flask config values have specious "/./" crap in them. Since that gets broken through
	# the abspath canonization, we pre-canonize the config path so it compares
	# properly.
	confpath = os.path.abspath(C_RESOURCE_DIR)

	fqpath = os.path.join(dirPath, filename)
	fqpath = os.path.abspath(fqpath)

	if not fqpath.startswith(confpath):
		raise ValueError("Generating the file path to save a cover produced a path that did not include the storage directory?")

	locpath = fqpath[len(confpath):]
	if not os.path.exists(fqpath):
		print("Saving file to path: '{fqpath}'!".format(fqpath=fqpath))
		with open(fqpath, "wb") as fp:
			fp.write(filecont)
	else:
		print("File '{fqpath}' already exists!".format(fqpath=fqpath))

	if locpath.startswith("/"):
		locpath = locpath[1:]
	return locpath

def build_rewalk_time_lut(rules):
	ret = {}

	for rset in rules:
		if rset['netlocs']:
			for netloc in rset['netlocs']:
				if rset['rewalk_interval_days']:
					ret[netloc] = rset['rewalk_interval_days']
	return ret

########################################################################################################################
#
#	##     ##    ###    #### ##    ##     ######  ##          ###     ######   ######
#	###   ###   ## ##    ##  ###   ##    ##    ## ##         ## ##   ##    ## ##    ##
#	#### ####  ##   ##   ##  ####  ##    ##       ##        ##   ##  ##       ##
#	## ### ## ##     ##  ##  ## ## ##    ##       ##       ##     ##  ######   ######
#	##     ## #########  ##  ##  ####    ##       ##       #########       ##       ##
#	##     ## ##     ##  ##  ##   ###    ##    ## ##       ##     ## ##    ## ##    ##
#	##     ## ##     ## #### ##    ##     ######  ######## ##     ##  ######   ######
#
########################################################################################################################


class SiteArchiver(LogBase.LoggerMixin):

	loggerPath = "Main.SiteArchiver"

	# Fetch items up to 1,000,000 (1 million) links away from the root source
	# This (functionally) equates to no limit.
	# The db defaults to  (e.g. max signed integer value) anyways
	FETCH_DISTANCE = 1000 * 1000

	def __init__(self, cookie_lock, db_interface, new_job_queue, run_filters=True, response_queue=None, use_socks=False):
		# print("SiteArchiver __init__()")
		super().__init__()

		self.new_job_queue = new_job_queue
		self.cookie_lock = cookie_lock
		self.resp_q  = response_queue
		self.db_sess = db_interface
		self.db      = db

		# print("SiteArchiver database imported")
		ruleset = WebMirror.rules.load_rules()
		self.netloc_rewalk_times = build_rewalk_time_lut(ruleset)
		self.ruleset = ruleset
		self.fetcher = WebMirror.Fetch.ItemFetcher
		self.wg = webFunctions.WebGetRobust(cookie_lock=cookie_lock, use_socks=use_socks)

		self.specialty_handlers = WebMirror.rules.load_special_case_sites()


		from activePlugins import INIT_CALLS
		for item in INIT_CALLS:
			item(self)

		# print("SiteArchiver rules loaded")
		self.relinkable = set()
		for item in ruleset:
			[self.relinkable.add(url) for url in item['fileDomains']]         #pylint: disable=W0106
			if item['netlocs'] != None:
				[self.relinkable.add(url) for url in item['netlocs']]             #pylint: disable=W0106


		self.ctnt_filters = {}
		self.rsc_filters  = {}


		for item in ruleset:

			if not item['netlocs']:
				continue

			for netloc in item['netlocs']:
				self.ctnt_filters[netloc] = item['netlocs']

			for netloc in item['fileDomains']:
				self.rsc_filters[netloc]  = item['fileDomains']

			# print("processing rsc")
			# print(item['fileDomains'])
			# rsc_vals  = self.buildUrlPermutations(item['fileDomains'], item['netlocs'])

		# self.log.info("Content filter size: %s. Resource filter size %s.", len(self.ctnt_filters), len(self.rsc_filters))
		# print("SiteArchiver initializer complete")

	########################################################################################################################
	#
	#	########    ###     ######  ##    ##    ########  ####  ######  ########     ###    ########  ######  ##     ## ######## ########
	#	   ##      ## ##   ##    ## ##   ##     ##     ##  ##  ##    ## ##     ##   ## ##      ##    ##    ## ##     ## ##       ##     ##
	#	   ##     ##   ##  ##       ##  ##      ##     ##  ##  ##       ##     ##  ##   ##     ##    ##       ##     ## ##       ##     ##
	#	   ##    ##     ##  ######  #####       ##     ##  ##   ######  ########  ##     ##    ##    ##       ######### ######   ########
	#	   ##    #########       ## ##  ##      ##     ##  ##        ## ##        #########    ##    ##       ##     ## ##       ##   ##
	#	   ##    ##     ## ##    ## ##   ##     ##     ##  ##  ##    ## ##        ##     ##    ##    ##    ## ##     ## ##       ##    ##
	#	   ##    ##     ##  ######  ##    ##    ########  ####  ######  ##        ##     ##    ##     ######  ##     ## ######## ##     ##
	#
	########################################################################################################################

	# Minimal proxy because I want to be able to call the fetcher without affecting the DB.
	def fetch(self, job, preretrieved=None):
		fetcher = self.fetcher(rules       = self.ruleset,
							target_url     = job.url,
							start_url      = job.starturl,
							cookie_lock    = self.cookie_lock,
							job            = job,
							wg_handle      = self.wg,
							response_queue = self.resp_q,
							db_sess        = self.db_sess)
		response = fetcher.fetch(preretrieved = preretrieved)
		return response

	# This is the main function that's called by the task management system.
	# Retreive remote content at `url`, call the appropriate handler for the
	# transferred content (e.g. is it an image/html page/binary file)
	def dispatchRequest(self, job, preretrieved=None):
		response = self.fetch(job, preretrieved=preretrieved)
		self.log.info("Dispatching job: %s, url: %s", job, job.url)
		self.processResponse(job, response)

	def processResponse(self, job, response):
		if "file" in response:
			# No title is present in a file response
			self.upsertFileResponse(job, response)
		elif 'rss-content' in response:
			self.upsertRssItems(job, response['rss-content'], job.url)
			self.upsertResponseLinks(job, plain=[entry['linkUrl'] for entry in response['rss-content']])
		else:
			self.upsertReponseContent(job, response)
			self.upsertResponseLinks(job, plain=response['plainLinks'], resource=response['rsrcLinks'])

		# Reset the fetch time download



	# Update the row with the item contents
	def upsertReponseContent(self, job, response):

		start = urllib.parse.urlsplit(job.starturl).netloc
		interval = settings.REWALK_INTERVAL_DAYS
		if start in self.netloc_rewalk_times and self.netloc_rewalk_times[start]:
			interval = self.netloc_rewalk_times[start]

		assert interval > 7
		ignoreuntiltime = (datetime.datetime.now() + datetime.timedelta(days=interval))

		# while True:
		# 	history_size = len(list(job.versions))
		# 	if history_size > 0:
		# 		break
		# 	try:
		# 		self.log.info("Need to push content into history table (current length: %s).", history_size)
		# 		job.title           = (job.title + " ")    if job.title    else " "
		# 		job.content         = (job.content + " ")  if job.content  else " "
		# 		job.mimetype        = (job.mimetype + " ") if job.mimetype else " "

		# 		job.fetchtime = datetime.datetime.now() - datetime.timedelta(days=7)

		# 		self.db_sess.commit()
		# 		self.log.info("Pushing old job content into history table!")
		# 		break
		# 	except sqlalchemy.exc.OperationalError:
		# 		self.db_sess.rollback()
		# 	except sqlalchemy.exc.InvalidRequestError:
		# 		self.db_sess.rollback()

		while 1:
			try:

				job.title           = response['title']
				job.content         = response['contents']
				job.mimetype        = response['mimeType']
				job.ignoreuntiltime = ignoreuntiltime


				if "text" in job.mimetype:
					job.is_text  = True
				else:
					job.is_text  = False

				job.state    = 'complete'

				# Disabled for space-reasons.
				# if 'rawcontent' in response:
				# 	job.raw_content = response['rawcontent']

				job.fetchtime = datetime.datetime.now()

				self.db_sess.commit()
				self.log.info("Marked plain job with id %s, url %s as complete!", job.id, job.url)
				break
			except sqlalchemy.exc.OperationalError:
				self.db_sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				self.db_sess.rollback()

	def insertRssItem(self, entry, feedurl):

		have = self.db_sess.query(self.db.FeedItems) \
			.filter(self.db.FeedItems.contentid == entry['guid'])   \
			.limit(1)                                  \
			.scalar()

		# print("keys = ", list(entry.keys()))


		if have:
			return
		else:
			if not ("srcname" in entry):
				self.log.error("'srcname' not in entry for item from '%s' (contenturl: '%s', title: '%s', guid: '%s')" % (feedurl, entry['linkUrl'], entry['title'], entry['guid']))
				return
			authors     = [tmp['name'] for tmp in entry['authors'] if 'name' in tmp]

			# Deduplicate repeat tags of the differing case.
			tags = {}
			for tag in entry['tags']:
				tags[tag.lower()] = tag

			new = self.db.FeedItems(
					contentid  = entry['guid'],
					title      = entry['title'],
					srcname    = entry['srcname'],
					feedurl    = feedurl,
					contenturl = entry['linkUrl'],

					type       = entry['feedtype'],
					contents   = entry['contents'],

					author     = authors,
					tags       = list(tags.values()),

					updated    = datetime.datetime.fromtimestamp(entry['updated']),
					published  = datetime.datetime.fromtimestamp(entry['published'])
				)

			self.db_sess.add(new)
			self.db_sess.commit()




	def upsertRssItems(self, job, entrylist, feedurl):

		start = urllib.parse.urlsplit(job.starturl).netloc
		interval = settings.REWALK_INTERVAL_DAYS
		if start in self.netloc_rewalk_times:
			interval = self.netloc_rewalk_times[start]
		ignoreuntiltime = (datetime.datetime.now() + datetime.timedelta(days=interval))
		print("[upsertFileResponse] Ignore until: ", ignoreuntiltime)

		while 1:
			try:
				self.db_sess.flush()
				if not (job.state == "fetching" or job.state == 'processing'):
					self.log.critical("Someone else modified row first? State: %s, url: %s", job.state, job.url)
				job.state           = 'complete'
				job.fetchtime       = datetime.datetime.now()
				job.ignoreuntiltime = ignoreuntiltime

				self.db_sess.commit()
				self.log.info("Marked RSS job with id %s, url %s as complete (%s)!", job.id, job.url, job.state)
				break

			except sqlalchemy.exc.InvalidRequestError:
				print("InvalidRequest error!")
				self.db_sess.rollback()
				traceback.print_exc()
			except sqlalchemy.exc.OperationalError:
				print("InvalidRequest error!")
				self.db_sess.rollback()
			except sqlalchemy.exc.IntegrityError:
				print("[upsertRssItems] -> Integrity error!")
				traceback.print_exc()
				self.db_sess.rollback()

		# print("InsertFeed!")
		for feedentry in entrylist:
			# print(feedentry)
			# print(feedentry.keys())
			# print(feedentry['contents'])
			# print(feedentry['published'])


			while 1:
				try:
					self.insertRssItem(feedentry, feedurl)
					break

				except sqlalchemy.exc.InvalidRequestError:
					print("InvalidRequest error!")
					self.db_sess.rollback()
					traceback.print_exc()
				except sqlalchemy.exc.OperationalError:
					print("OperationalError error!")
					self.db_sess.rollback()
				except sqlalchemy.exc.IntegrityError:
					print("[upsertRssItems] -> Integrity error!")
					traceback.print_exc()
					self.db_sess.rollback()

	def generalLinkClean(self, link, badwords):
		if link.startswith("data:"):
			return None
		if any([item in link for item in badwords]):
			# print("Filtered:", link)
			return None
		return link

	# Todo: FIXME
	def filterContentLinks(self, job, links, badwords):
		ret = set()
		for link in links:
			link = self.generalLinkClean(link, badwords)
			if not link:
				continue
			netloc = urllib.parse.urlsplit(link).netloc
			if netloc in self.ctnt_filters and job.netloc in self.ctnt_filters[netloc]:
				# print("Valid content link: ", link)
				ret.add(link)
		return ret

	def filterResourceLinks(self, job, links, badwords):
		ret = set()
		for link in links:
			link = self.generalLinkClean(link, badwords)
			if not link:
				continue
			netloc = urllib.parse.urlsplit(link).netloc
			if netloc in self.rsc_filters:
				# print("Valid resource link: ", link)
				ret.add(link)
		return ret

	def getBadWords(self, job):
		badwords = GLOBAL_BAD
		for item in [rules for rules in self.ruleset if rules['netlocs'] and job.netloc in rules['netlocs']]:
			badwords += item['badwords']

		# A "None" can occationally crop up. Filter it.
		badwords = [badword for badword in badwords if badword]
		return badwords

	def upsertResponseLinks(self, job, plain=[], resource=[]):
		plain    = set(plain)
		resource = set(resource)

		unfiltered = len(plain)+len(resource)

		badwords = self.getBadWords(job)

		plain    = self.filterContentLinks(job,  plain,    badwords)
		resource = self.filterResourceLinks(job, resource, badwords)

		filtered = len(plain)+len(resource)
		self.log.info("Upserting %s links (%s filtered)" % (filtered, unfiltered))

		items = []
		[items.append((link, True))  for link in plain]
		[items.append((link, False)) for link in resource]

		self.log.info("Page had %s unfiltered content links, %s unfiltered resource links.", len(plain), len(resource))

		if self.resp_q != None and False:
			for link, istext in items:
				start = urllib.parse.urlsplit(link).netloc

				assert link.startswith("http")
				assert start
				new = {
					'url'       : link,
					'starturl'  : job.starturl,
					'netloc'    : start,
					'distance'  : job.distance+1,
					'is_text'   : istext,
					'priority'  : job.priority,
					'type'      : job.type,
					'state'     : "new",
					'fetchtime' : datetime.datetime.now(),
					}
				self.resp_q.put(("new_link", new))

				while self.resp_q.qsize() > 1000:
					time.sleep(0.1)

			self.log.info("Links upserted. Items in processing queue: %s", self.resp_q.qsize())
		else:

			#  Fucking huzzah for ON CONFLICT!
			cmd = text("""
					INSERT INTO
						web_pages
						(url, starturl, netloc, distance, is_text, priority, type, addtime, state)
					VALUES
						(:url, :starturl, :netloc, :distance, :is_text, :priority, :type, :addtime, :state)
					ON CONFLICT (url) DO
						UPDATE
							SET
								state           = EXCLUDED.state,
								starturl        = EXCLUDED.starturl,
								netloc          = EXCLUDED.netloc,
								is_text         = EXCLUDED.is_text,
								distance        = LEAST(EXCLUDED.distance, web_pages.distance),
								priority        = GREATEST(EXCLUDED.priority, web_pages.priority),
								addtime         = LEAST(EXCLUDED.addtime, web_pages.addtime)
							WHERE
							(
									web_pages.ignoreuntiltime < :ignoreuntiltime
								AND
									web_pages.url = EXCLUDED.url
								AND
									(web_pages.state = 'complete' OR web_pages.state = 'error')
							)
						;
					""".replace("	", " ").replace("\n", " "))

			# cmd = text("""
			# 		INSERT INTO
			# 			web_pages
			# 			(url, starturl, netloc, distance, is_text, priority, type, addtime, state)
			# 		VALUES
			# 			(:url, :starturl, :netloc, :distance, :is_text, :priority, :type, :addtime, :state)
			# 		ON CONFLICT DO NOTHING
			# 			;
			# 		""".replace("	", " ").replace("\n", " "))

			# Only commit per-URL if we're tried to do the update in batch, and failed.
			commit_each = False
			for link, istext in items:
				while 1:
					try:
						start = urllib.parse.urlsplit(link).netloc

						assert link.startswith("http")
						assert start


						# Forward-data the next walk, time, rather then using now-value for the thresh.
						new = {
							'url'             : link,
							'starturl'        : job.starturl,
							'netloc'          : start,
							'distance'        : job.distance+1,
							'is_text'         : istext,
							'priority'        : job.priority,
							'type'            : job.type,
							'state'           : "new",
							'addtime'         : datetime.datetime.now(),

							# Don't retrigger unless the ignore time has elaped.
							'ignoreuntiltime' : datetime.datetime.now(),
							}
						self.db_sess.execute(cmd, params=new)
						if commit_each:
							self.db_sess.commit()
						break
					except sqlalchemy.exc.ProgrammingError:
						self.log.warn("SQLAlchemy ProgrammingError - Retrying.")
						self.db_sess.rollback()
						traceback.print_exc()
						commit_each = True
					except sqlalchemy.exc.InternalError:
						self.log.warn("SQLAlchemy InternalError - Retrying.")
						self.db_sess.rollback()
						commit_each = True
					except sqlalchemy.exc.OperationalError:
						if not commit_each:
							self.log.warn("SQLAlchemy OperationalError - Retrying with commit_each.")
						else:
							self.log.warn("SQLAlchemy OperationalError with commit_each. Retrying.")
						self.db_sess.rollback()
						# traceback.print_exc()
						commit_each = True
						time.sleep(random.random())
					except sqlalchemy.exc.InvalidRequestError:
						self.log.warn("SQLAlchemy InvalidRequestError - Retrying.")
						self.db_sess.rollback()
						commit_each = True
					except sqlalchemy.exc.SQLAlchemyError:
						self.log.warn("SQLAlchemy SQLAlchemyError - Retrying.")
						self.db_sess.rollback()
						commit_each = True

			self.db_sess.commit()

	def upsertFileResponse(self, job, response):
		# Response dict structure:
		# {"file" : True, "url" : url, "mimeType" : mimeType, "fName" : fName, "content" : content}
		# print("File response!")
		# Yeah, I'm hashing twice in lots of cases. Bite me
		fHash = getHash(response['content'])


		start = urllib.parse.urlsplit(job.starturl).netloc
		interval = settings.REWALK_INTERVAL_DAYS
		if start in self.netloc_rewalk_times:
			interval = self.netloc_rewalk_times[start]

		assert interval > 7
		ignoreuntiltime = (datetime.datetime.now() + datetime.timedelta(days=interval))
		print("[upsertFileResponse] Ignore until: ", ignoreuntiltime)

		while 1:
			try:
				# Look for existing files with the same MD5sum. If there are any, just point the new file at the
				# fsPath of the existing one, rather then creating a new file on-disk.
				have = self.db_sess.query(self.db.WebFiles) \
					.filter(self.db.WebFiles.fhash == fHash)   \
					.limit(1)                                  \
					.scalar()

				if have:
					match = self.db_sess.query(self.db.WebFiles)              \
						.filter(self.db.WebFiles.fhash == fHash)                \
						.filter(self.db.WebFiles.filename == response['fName']) \
						.limit(1)                                               \
						.scalar()
					if match:
						job.file = match.id
					else:
						new = self.db.WebFiles(
							filename = response['fName'],
							fhash    = fHash,
							fspath   = have.fspath,
							)
						self.db_sess.add(new)
						self.db_sess.commit()
						job.file = new.id
				else:
					savedpath = saveCoverFile(response['content'], fHash, response['fName'])
					new = self.db.WebFiles(
						filename = response['fName'],
						fhash    = fHash,
						fspath   = savedpath,
						)
					self.db_sess.add(new)
					self.db_sess.commit()
					job.file = new.id

				job.state           = 'complete'
				job.is_text         = False
				job.fetchtime       = datetime.datetime.now()
				job.ignoreuntiltime = ignoreuntiltime

				self.log.info("Marked file job with id %s, url %s as complete!", job.id, job.url)

				job.mimetype = response['mimeType']
				self.db_sess.commit()
				break
			except sqlalchemy.exc.OperationalError:
				self.db_sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				self.db_sess.rollback()
		# print("have:", have)




	########################################################################################################################
	#
	#	########  ########   #######   ######  ########  ######   ######      ######   #######  ##    ## ######## ########   #######  ##
	#	##     ## ##     ## ##     ## ##    ## ##       ##    ## ##    ##    ##    ## ##     ## ###   ##    ##    ##     ## ##     ## ##
	#	##     ## ##     ## ##     ## ##       ##       ##       ##          ##       ##     ## ####  ##    ##    ##     ## ##     ## ##
	#	########  ########  ##     ## ##       ######    ######   ######     ##       ##     ## ## ## ##    ##    ########  ##     ## ##
	#	##        ##   ##   ##     ## ##       ##             ##       ##    ##       ##     ## ##  ####    ##    ##   ##   ##     ## ##
	#	##        ##    ##  ##     ## ##    ## ##       ##    ## ##    ##    ##    ## ##     ## ##   ###    ##    ##    ##  ##     ## ##
	#	##        ##     ##  #######   ######  ########  ######   ######      ######   #######  ##    ##    ##    ##     ##  #######  ########
	#
	########################################################################################################################


	def getRpcResp(self):
		'''
		Get a job row item from the database.

		Also updates the row to be in the "fetching" state.
		'''
		# self.db_sess.begin()

		# Try to get a task untill we are explicitly out of tasks,
		# return self._get_task_internal(wattpad)


		# self.log.info("Trying to get a job.")
		try:
			job_item = self.new_job_queue.get_nowait()
			# self.log.info("New job: %s", job_item)
			return job_item
		except queue.Empty:
			# self.log.info("No jobs in queue? (qsize =  %s)", self.new_job_queue.qsize())
			return False
		if not job_item:
			return False

		raise ValueError



	def get_job_from_id(self, jobid):

		self.db_sess.flush()
		job = self.db_sess.query(self.db.WebPages) \
			.filter(self.db.WebPages.id == jobid)    \
			.one()
		self.db_sess.flush()

		if not job:
			self.db_sess.commit()
			return False

		# Don't dump old jobs that have been accidentally reset.
		if job.state == 'new':
			job.state = 'fetching'
			self.db_sess.commit()

		if job.state != 'fetching':
			self.db_sess.commit()
			self.log.info("Job not in expected state (state: %s).", job.state)
			return None

		self.db_sess.commit()
		self.log.info("Job for url: '%s' fetched. State: '%s'", job.url, job.state)

		self.db_sess.flush()


		return job


	def process_rpc_response(self, rpcresp):
		"""
		Expected response structure:
			{
			 'call': 'getItem',
			 'cancontinue': True,
			 'dispatch_key': 'fetcher',
			 'extradat': {'mode': 'fetch'},
			 'jobid': 547397438,
			 'module': 'WebRequest',
			 'ret': (item_content, item_filename, item_mimetype),
			 'success': True,
			 'user': 'client_2'
			}

		Response on error:

			{
			 'cancontinue': True,
			 'error': 'unknown',
			 'jobid': 570102816,
			 'success': False,
			 'traceback': 'Traceback (most recent call last):\n'
			              '  File "/root/AutoTriever/client.py", line 85, in _process\n'
			              '    ret = self.process(body)\n'
			              '  File "/root/AutoTriever/dispatcher.py", line 99, in '
			              'process\n'
			              "    ret = self.doCall(command['module'], command['call'], "
			              'args, kwargs)\n'
			              '  File "/root/AutoTriever/dispatcher.py", line 60, in doCall\n'
			              '    return self.classCache[module].calls[call](*call_args, '
			              '**call_kwargs)\n'
			              '  File "/root/AutoTriever/util/WebRequest.py", line 543, in '
			              'getItem\n'
			              '    raise urllib.error.URLError("Failed to retreive file from '
			              'page \'%s\'!" % itemUrl)\n'
			              'urllib.error.URLError: <urlopen error Failed to retreive file '
			              'from page '
			              "'http://dandeliontrail.livejournal.com/data/rss?tag=once "
			              "promised'!>\n",
			 'user': 'client_1'
			}


		"""

		try:
			job = self.get_job_from_id(rpcresp['jobid'])
			if job == False:
				self.log.error("Received job that doesn't exist in the database? Wut? (Id: %s -> %s)", rpcresp['jobid'], job)
				return
			if job == None:
				self.log.error("Job already being processed? Wut? (Id: %s)", rpcresp['jobid'])
				return

			if 'ret' in rpcresp:
				preretrieved = rpcresp['ret']
				self.dispatchRequest(job, preretrieved)
			else:
				content = "DOWNLOAD FAILED"
				content += "<br>"
				if 'traceback' in rpcresp:
					content += "<pre>"
					content += rpcresp['traceback']
					content += "</pre>"
					for line in rpcresp['traceback'].strip().split("\n"):
						self.log.error("Remote traceback: %s", line)
				# job.raw_content = content
				job.state = 'error'
				job.errno = -4
				self.db_sess.commit()
				self.log.error("Error in remote fetch.")

		except KeyboardInterrupt:
			runStatus.run = False
			runStatus.run_state.value = 0
			print("Keyboard Interrupt!")


	def taskProcess(self):
		'''
		Return true if there was something to do, false if not.
		'''
		job = None
		try:

			while runStatus.run_state.value == 1:
				rpcresp = self.getRpcResp()
				if not rpcresp:
					return False
				self.process_rpc_response(rpcresp)

			# if job.netloc in self.specialty_handlers:
			# 	self.log.info("Job %s for url %s has a specialty handler!", job, job.url)
			# 	self.special_case_handle(job)
			# else:
			# 	if job:

		except Exception:
			# err_f = os.path.join("./logs", "error - {}.txt".format(time.time()))
			# with open(err_f, "w") as fp:
			# 	if job:
			# 		fp.write("Job: {val}\n".format(val=job))
			# 		fp.write("Job-netloc: {val}\n".format(val=job.netloc))
			# 		fp.write("Job-url: {val}\n".format(val=job.url))
			# 		job.state = "error"
			# 		self.db_sess.commit()

			# 	fp.write(traceback.format_exc())

			for line in traceback.format_exc().split("\n"):
				self.log.critical("%s", line.rstrip())
		return True

	def get_row(self, url, distance=None, priority=None):
		if distance == None:
			distance = self.db.MAX_DISTANCE-2

		if priority == None:
			priority = self.db.DB_REALTIME_PRIORITY

		# Rather then trying to add, and rolling back if it exists,
		# just do a simple check for the row first. That'll
		# probably be faster in the /great/ majority of cases.
		while 1:
			# self.db_sess.begin()
			try:
				row =  self.db_sess.query(self.db.WebPages) \
					.filter(self.db.WebPages.url == url)       \
					.scalar()

				self.db_sess.commit()
				break
			except sqlalchemy.exc.InvalidRequestError:
				self.db_sess.rollback()
			except sqlalchemy.exc.OperationalError:
				self.db_sess.rollback()
			except sqlalchemy.exc.IntegrityError:
				self.db_sess.rollback()


		if row:
			self.log.info("Item already exists in database.")
		else:
			self.log.info("Row does not exist in DB")
			url_netloc = urllib.parse.urlsplit(url).netloc

			# New jobs are inserted in the "fetching" state since we
			# don't want them to be picked up by the fetch engine
			# while they're still in-progress
			row = self.db.WebPages(
				state     = 'fetching',
				url       = url,
				starturl  = url,
				netloc    = url_netloc,
				distance  = distance,
				is_text   = True,
				priority  = priority,
				type      = "unknown",
				fetchtime = datetime.datetime.now(),
				)

			# Because we can have parallel operations happening here, we spin on adding&committing the new
			# row untill the commit either succeeds, or we get an integrity error, and then successfully
			# fetch the row inserted by another thread at the same time.
			while 1:
				try:
					# self.db_sess.begin()
					self.db_sess.add(row)
					self.db_sess.commit()
					print("Row added?")
					break
				except sqlalchemy.exc.InvalidRequestError:
					print("InvalidRequest error!")
					self.db_sess.rollback()
					traceback.print_exc()
				except sqlalchemy.exc.OperationalError:
					print("InvalidRequest error!")
					self.db_sess.rollback()
				except sqlalchemy.exc.IntegrityError:
					print("[synchronousJobRequest] -> Integrity error!")
					self.db_sess.rollback()
					row = self.db_sess.query(self.db.WebPages) \
						.filter(self.db.WebPages.url == url)            \
						.one()
					self.db_sess.commit()
					break
		return row


	def synchronousDispatchPrefetched(self, url, parentjob, content, mimetype, filename="None"):
		self.log.info("Manually initiated dispatch for prefetched-content at '%s'", url)
		row = self.get_row(url)

		fetcher = self.fetcher(self.ruleset, url, parentjob.starturl, job=row, cookie_lock=None, wg_handle=self.wg, response_queue=self.resp_q)
		ret = fetcher.dispatchContent(content, filename, mimetype)
		self.processResponse(row, ret)



	def synchronousJobRequest(self, url, ignore_cache=False):
		"""
		trigger an immediate, synchronous dispatch of a job for url `url`,
		and return the fetched row upon completion

		"""
		self.log.info("Manually initiated request for content at '%s'", url)

		row = self.get_row(url)

		thresh_text_ago = datetime.datetime.now() - datetime.timedelta(seconds=CACHE_DURATION)
		thresh_bin_ago  = datetime.datetime.now() - datetime.timedelta(seconds=RSC_CACHE_DURATION)

		if ignore_cache:
			self.log.info("Cache ignored due to override")
		else:
			# if row.state == "complete" and row.fetchtime > thresh_text_ago:
			# if row.state == "complete" and row.fetchtime > thresh_bin_ago and "text" not in row.mimetype.lower():
			# 	self.log.info("Using cached fetch results as content was retreived within the last %s seconds.", CACHE_DURATION)
			# 	return row
			if row.state == "complete":
				self.log.info("Using cached fetch results.")
				self.log.info("dbid: %s", row.id)
				return row
			else:
				self.log.info("Item has exceeded cache time by text: %s, rsc: %s. (fetchtime: %s) Re-acquiring.", thresh_text_ago, thresh_bin_ago, row.fetchtime)

		row.state     = 'new'
		row.distance  = self.db.MAX_DISTANCE-2
		row.priority  = self.db.DB_REALTIME_PRIORITY

		# dispatchRequest modifies the row contents directly.
		self.dispatchRequest(row)

		# Commit, because why not
		self.db_sess.commit()

		return row


def test():
	archiver = SiteArchiver(None)

	new = {
		'url'       : 'http://www.royalroadl.com/fiction/1484',
		'starturl'  : 'http://www.royalroadl.com/',
		'netloc'    : "www.royalroadl.com",
		'distance'  : 50000,
		'is_text'   : True,
		'priority'  : 500000,
		'type'      : 'unknown',
		'fetchtime' : datetime.datetime.now(),
		}

	cmd = text("""
			INSERT INTO
				web_pages
				(url, starturl, netloc, distance, is_text, priority, type, fetchtime)
			VALUES
				(:url, :starturl, :netloc, :distance, :is_text, :priority, :type, :fetchtime)
			ON CONFLICT DO NOTHING
			""")
	print("doing")
	# ins = archiver.db.get_session().execute(cmd, params=new)
	# print("Doneself. Ret:")
	# print(ins)
	# print(archiver.resetDlstate())
	print(archiver.getRpcResp())
	# print(archiver.getRpcResp())
	# print(archiver.getRpcResp())
	# print(archiver.taskProcess())
	pass

def test2():
	ruleset = WebMirror.rules.load_rules()
	netloc_rewalk_times = build_rewalk_time_lut(ruleset)
	print(netloc_rewalk_times)


if __name__ == "__main__":
	test2()


