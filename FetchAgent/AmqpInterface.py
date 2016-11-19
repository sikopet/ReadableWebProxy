#!/usr/bin/env python3
import msgpack
import multiprocessing
import settings
import datetime
import queue
import logging
import threading
import os.path
import time
import ssl
import uuid
import FetchAgent.AmqpConnector


class RabbitQueueHandler(object):
	die = False

	def __init__(self, settings, mdict):

		self.logPath = 'Main.Feeds.RPC'

		self.log = logging.getLogger(self.logPath)
		self.log.info("RPC Management class instantiated.")
		self.mdict = mdict

		self.dispatch_map = {}

		# Require clientID in settings
		assert "RABBIT_LOGIN"       in settings
		assert "RABBIT_PASWD"       in settings
		assert "RABBIT_SRVER"       in settings
		assert "RABBIT_VHOST"       in settings
		assert "RABBIT_FEED_VHOST"  in settings

		assert "taskq_task"         in settings
		assert "taskq_response"     in settings

		sslopts = self.getSslOpts()
		self.vhost = settings["RABBIT_VHOST"]
		self.connector = FetchAgent.AmqpConnector.Connector(userid            = settings["RABBIT_LOGIN"],
												password           = settings["RABBIT_PASWD"],
												host               = settings["RABBIT_SRVER"],
												virtual_host       = settings["RABBIT_VHOST"],
												ssl                = sslopts,
												master             = settings.get('master', True),
												synchronous        = settings.get('synchronous', False),
												flush_queues       = False,
												prefetch           = settings.get('prefetch', 25),
												durable            = True,
												heartbeat          = 60,
												task_exchange_type = 'direct',
												poll_rate          = settings.get('poll_rate', 1.0/100),
												task_queue         = settings["taskq_task"],
												response_queue     = settings["taskq_response"],
												)

		# self.feed_connector = FetchAgent.AmqpConnector.Connector(userid            = settings["RABBIT_FEED_LOGIN"],
		# 										password           = settings["RABBIT_FEED_PASWD"],
		# 										host               = settings["RABBIT_FEED_SRVER"],
		# 										virtual_host       = settings["RABBIT_FEED_VHOST"],
		# 										ssl                = sslopts,
		# 										master             = settings.get('master', True),
		# 										synchronous        = settings.get('synchronous', False),
		# 										flush_queues       = False,
		# 										prefetch           = settings.get('prefetch', 25),
		# 										durable            = True,
		# 										heartbeat          = 60,
		# 										task_exchange_type = 'fanout',
		# 										poll_rate          = settings.get('poll_rate', 1.0/100),
		# 										task_queue         = settings["taskq_task"],
		# 										response_queue     = settings["taskq_response"],
		# 										)


		self.chunks = {}

		self.log.info("Connected AMQP Interface: %s", self.connector)
		self.log.info("Connection parameters: %s, %s, %s, %s", settings["RABBIT_LOGIN"], settings["RABBIT_PASWD"], settings["RABBIT_SRVER"], settings["RABBIT_VHOST"])

	def getSslOpts(self):
		'''
		Verify the SSL cert exists in the proper place.
		'''
		certpath = './rabbit_pub_cert/'

		caCert = os.path.abspath(os.path.join(certpath, './cacert.pem'))
		cert = os.path.abspath(os.path.join(certpath, './cert1.pem'))
		keyf = os.path.abspath(os.path.join(certpath, './key1.pem'))

		assert os.path.exists(caCert), "No certificates found on path '%s'" % caCert
		assert os.path.exists(cert), "No certificates found on path '%s'" % cert
		assert os.path.exists(keyf), "No certificates found on path '%s'" % keyf

		ret = {"cert_reqs" : ssl.CERT_REQUIRED,
				"ca_certs" : caCert,
				"keyfile"  : keyf,
				"certfile"  : cert,
			}
		print("Certificate config: ", ret)

		return ret

	def put_item(self, data):
		# self.log.info("Putting data: %s", data)
		self.connector.putMessage(data, synchronous=1000)
		# self.log.info("Outgoing data size: %s bytes.", len(data))


	def get_item(self):
		ret = self.connector.getMessage()
		if ret:
			self.log.info("Received data size: %s bytes.", len(ret))
		return ret

	def process_chunk(self, chunk_message):
		assert 'chunk-type'   in chunk_message
		assert 'chunk-num'    in chunk_message
		assert 'total-chunks' in chunk_message
		assert 'data'         in chunk_message
		assert 'merge-key'    in chunk_message

		merge_key     = chunk_message['merge-key']
		total_chunks  = chunk_message['total-chunks']
		chunk_num     = chunk_message['chunk-num']
		data          = chunk_message['data']
		merge_key     = chunk_message['merge-key']

		if not merge_key in self.chunks:
			self.chunks[merge_key] = {
				'first-seen'  : datetime.datetime.now(),
				'chunk-count' : total_chunks,
				'chunks'      : {}
			}

		# Check our chunk count is sane.
		assert self.chunks[merge_key]['chunk-count'] == total_chunks
		self.chunks[merge_key]['chunks'][chunk_num] = data


		# TODO: clean out partial messages based on their age (see 'first-seen')

		if len(self.chunks[merge_key]['chunks']) == total_chunks:
			components = list(self.chunks[merge_key]['chunks'].items())
			components.sort()
			packed_message = b''.join([part[1] for part in components])
			ret = msgpack.unpackb(packed_message, encoding='utf-8', use_list=False)

			del self.chunks[merge_key]

			self.log.info("Received all chunks for key %s! Decoded size: %0.3fk from %s chunks. Active partial chunked messages: %s.",
				merge_key, len(packed_message) / 1024, len(components), len(self.chunks))

			return ret

		else:
			return None

	def unchunk(self, new_message):
		new = msgpack.unpackb(new_message, encoding='utf-8', use_list=False)

		# If we don't have a chunking type, it's probably an old-style message.
		if not 'chunk-type' in new:
			return new

		# Messages smaller then the chunk_size are not split, and can just be returned.
		if new['chunk-type'] == "complete-message":
			assert 'chunk-type' in new
			assert 'data'       in new
			return new['data']
		elif new['chunk-type'] == "chunked-message":
			return self.process_chunk(new)
		else:
			raise RuntimeError("Unknown message type: %s", new['chunk-type'])

	def get_job(self):
		while True:
			new = self.get_item()
			if new:
				self.log.info("Processing AMQP response item!")
				try:
					tmp = self.unchunk(new)

					# If unchunk returned something, return that.
					# if it didn't return anything, it means that new
					# was a message chunk, but we don't have the
					# whole thing yet, so continue.
					if tmp:
						return tmp
				except Exception:
					self.log.error("Failure unpacking message!")
					msgstr = str(new)
					if len(new) < 5000:
						self.log.error("Message content: %s", msgstr)
					else:
						self.log.error("Message length: '%s'", len(msgstr))
			else:
				return None

	def put_job(self, new_job):
		assert 'module'       in new_job
		assert 'call'         in new_job
		assert 'dispatch_key' in new_job
		assert 'jobid'        in new_job
		assert new_job['jobid'] != None

		assert 'jobmeta'     in new_job

		# Make sure we have a returned data list for the added job.

		packed_job = msgpack.packb(new_job, use_bin_type=True)
		self.put_item(packed_job)

	def __del__(self):
		self.close()

	def close(self):
		if hasattr(self, "connector") and self.connector:
			print("Closing connector wrapper: ", self.logPath, self.vhost)
			self.connector.stop()
			self.connector = None


	def dispatch_outgoing(self):
		for qname, q in self.mdict['outq'].items():
			while not q.empty():
				try:
					job = q.get_nowait()
					jkey = uuid.uuid1().hex
					job['jobmeta'] = {'sort_key' : jkey}
					self.dispatch_map[jkey] = qname
					self.put_job(job)
				except queue.Empty:
					break
		while not self.mdict['rssq'].empty():
			job = self.mdict['rssq'].get_nowait()
			self.feed_connector.putMessage(job, synchronous=1000)


	def process_retreived(self):
		while True:
			new = self.get_job()
			if not new:
				# print("No job item?", new)
				return

			if not 'jobmeta' in new:
				self.log.error("No metadata in job! Wat?")
				self.log.error("Job contents: '%s'", new)
				continue
			if not 'sort_key' in new['jobmeta']:
				self.log.error("No sort key in job! Wat?")
				self.log.error("Job contents: '%s'", new)
				continue

			jkey = new['jobmeta']['sort_key']
			if not jkey in self.dispatch_map:
				self.log.error("Job sort key not in known table! Does the job predate the current execution session?")
				self.log.error("Job key: '%s'", jkey)
				self.log.error("Job contents: '%s'", new)
				continue

			qname = self.dispatch_map[jkey]
			if not qname in self.mdict['inq']:
				self.log.error("Job response queue missing?")
				self.log.error("Queue name: '%s'", qname)
				continue

			self.log.info("Demultiplexed job for '%s'", qname)
			self.mdict['inq'][qname].put(new)


	def runner(self):
		self.mdict['amqp_runstate'] = True

		while self.mdict['amqp_runstate']:
			time.sleep(1)
			self.dispatch_outgoing()
			self.process_retreived()

		self.log.info("Saw exit flag. Closing interface")
		self.close()






STATE = {}

def startup_interface(manager):
	amqp_settings = {
		'RABBIT_LOGIN'         : settings.RPC_RABBIT_LOGIN,
		'RABBIT_PASWD'         : settings.RPC_RABBIT_PASWD,
		'RABBIT_SRVER'         : settings.RPC_RABBIT_SRVER,
		'RABBIT_VHOST'         : settings.RPC_RABBIT_VHOST,

		'RABBIT_FEED_LOGIN'    : settings.RABBIT_LOGIN,
		'RABBIT_FEED_PASWD'    : settings.RABBIT_PASWD,
		'RABBIT_FEED_SRVER'    : settings.RABBIT_SRVER,
		'RABBIT_FEED_VHOST'    : settings.RABBIT_VHOST,
		'master'          : True,
		'prefetch'        : 250,
		# 'prefetch'        : 50,
		# 'prefetch'        : 5,
		'queue_mode'      : 'direct',
		'taskq_task'      : 'task.q',
		'taskq_response'  : 'response.q',

		"poll_rate"       : 1/100,

	}

	STATE['instance'] = RabbitQueueHandler(amqp_settings, manager)
	STATE['thread'] = threading.Thread(target=STATE['instance'].runner)
	STATE['thread'].start()



def shutdown_interface(manager):
	print("Halting AMQP interface")
	manager['amqp_runstate'] = False
	STATE['thread'].join()

