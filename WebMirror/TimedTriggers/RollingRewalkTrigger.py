

import config
import urllib.parse
import datetime
import time
import zlib
import settings
import datetime
import sqlalchemy.exc

import common.database as dbm

import WebMirror.rules
import WebMirror.TimedTriggers.TriggerBase


class RollingRewalkTriggerBase(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass):


	pluginName = "RollingRewalk Trigger"

	loggerPath = 'RollingRewalk'



	def retrigger_netloc(self, netloc, ago):

		sess = self.db.get_db_session()
		while 1:
			try:
				q = sess.query(self.db.WebPages) \
					.filter(self.db.WebPages.netloc == netloc)  \
					.filter(self.db.WebPages.state == 'complete')   \
					.filter(self.db.WebPages.fetchtime < ago)
				affected_rows = q.update({"state" : "new"})
				sess.commit()
				self.log.info("Updated for netloc %s - %s rows", netloc, affected_rows)
				break
			except sqlalchemy.exc.InternalError:
				self.log.info("Transaction error. Retrying.")
				sess.rollback()
			except sqlalchemy.exc.OperationalError:
				self.log.info("Transaction error. Retrying.")
				sess.rollback()
			except sqlalchemy.exc.IntegrityError:
				self.log.info("Transaction error. Retrying.")
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				self.log.info("Transaction error. Retrying.")
				sess.rollback()

	def retrigger_other(self):
		sess = self.db.get_db_session()
		ago = datetime.datetime.now() - datetime.timedelta(days=settings.REWALK_INTERVAL_DAYS + 3)
		while 1:
			try:
				q = sess.query(self.db.WebPages) \
					.filter(self.db.WebPages.state == 'complete')   \
					.filter(self.db.WebPages.fetchtime < ago)
				affected_rows = q.update({"state" : "new"})
				sess.commit()
				self.log.info("Updated for all unspecified netlocs - %s rows", affected_rows)
				break
			except sqlalchemy.exc.InternalError:
				self.log.info("Transaction error. Retrying.")
				sess.rollback()
			except sqlalchemy.exc.OperationalError:
				self.log.info("Transaction error. Retrying.")
				sess.rollback()
			except sqlalchemy.exc.IntegrityError:
				self.log.info("Transaction error. Retrying.")
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				self.log.info("Transaction error. Retrying.")
				sess.rollback()


	def go(self):

		rules = WebMirror.rules.load_rules()
		self.log.info("Rolling re-trigger of starting URLs.")



		starturls = []
		for ruleset in [tmp for tmp in rules if (tmp and tmp['starturls'])]:
			for starturl in ruleset['starturls']:
				if not ruleset['rewalk_interval_days']:
					interval = settings.REWALK_INTERVAL_DAYS
				else:
					interval = ruleset['rewalk_interval_days']
				nl = urllib.parse.urlsplit(starturl).netloc
				starturls.append((interval, nl))

		starturls = set(starturls)
		starturls = list(starturls)
		starturls.sort()

		sess = self.db.get_db_session()

		for interval, nl in starturls:

			if "wattpad.com" in nl:
				continue
			if "booksie.com" in nl:
				continue

			# "+2" is to (hopefully) allow the normal rewalk system to catch the site.
			ago = datetime.datetime.now() - datetime.timedelta(days=(interval + 2))

			self.retrigger_netloc(nl, ago)

			# def conditional_check(row):
			# 	if day == today or row.fetchtime < (datetime.datetime.now() - datetime.timedelta(days=settings.REWALK_INTERVAL_DAYS)):
			# 		print("Retriggering: ", row, row.fetchtime, row.url)
			# 		row.state    = "new"
			# 		row.distance = 0
			# 		row.priority = dbm.DB_IDLE_PRIORITY
			# 		row.ignoreuntiltime = datetime.datetime.now() - datetime.timedelta(days=1)

			# self.retriggerUrl(url, conditional=conditional_check)

		self.retrigger_other()
		self.log.info("Old files retrigger complete.")


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	run = RollingRewalkTriggerBase()
	run._go()

