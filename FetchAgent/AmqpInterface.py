#!/usr/bin/env python3
import msgpack
import settings as settings_file
import datetime
import traceback
import queue
from . import AmqpConnector
import logging
import threading
import os.path
import time
import ssl
import uuid
import statsd
import cachetools


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

		assert "taskq_task"         in settings
		assert "taskq_response"     in settings

		assert 'taskq_name' in settings
		assert 'respq_name' in settings
		self.settings = settings

		self.put_idx = 0
		self.get_idx = 0

		self.ext_taskq = queue.Queue()
		self.ext_repq  = queue.Queue()

		sslopts = self.getSslOpts()
		self.vhost = settings["RABBIT_VHOST"]
		self.connectors = []
		for threadno in range(settings['consumer_threads']):
			self.log.info("Creating worker %s", threadno)
			self.connectors.append(
				AmqpConnector.Connector(
													userid                 = settings["RABBIT_LOGIN"],
													password               = settings["RABBIT_PASWD"],
													host                   = settings["RABBIT_SRVER"],
													virtual_host           = settings["RABBIT_VHOST"],
													ssl                    = sslopts,
													master                 = settings['master'],
													synchronous            = settings['synchronous'],
													flush_queues           = settings['flush_queues'],
													prefetch               = settings['prefetch'],
													durable                = settings['durable'],
													heartbeat              = settings['heartbeat'],
													task_exchange_type     = settings['task_exchange_type'],
													poll_rate              = settings['poll_rate'],
													task_queue             = settings["taskq_task"],
													response_queue         = settings["taskq_response"],
													response_exchange_type = settings['response_exchange_type'],
													task_exchange          = settings["task_exchange"],
													response_exchange      = settings["response_exchange"],
													socket_timeout         = settings["socket_timeout"],
													ack_rx                 = settings["ack_rx"],

													external_task_queue     = self.ext_taskq,
													external_response_queue = self.ext_repq,
													)
				)
			# We spread out the socket creation along the timeout interval, so
			# that all the connectors don't function in apparent lockstep
			time.sleep(settings['socket_timeout'] / settings['consumer_threads'])


		# The chunk structure is slightly annoying, so just limit to 200 partial messages.
		self.chunks     = cachetools.LRUCache(maxsize=200)
		self.chunk_lock = threading.Lock()

		self.log.info("Connected AMQP Interface: %s", self.connectors)
		self.log.info("Connection parameters: %s, %s, %s, %s", settings["RABBIT_LOGIN"], settings["RABBIT_PASWD"], settings["RABBIT_SRVER"], settings["RABBIT_VHOST"])

		self.log.info("Setting up stats reporter")

		self.mon_con = statsd.StatsClient(
				host = settings['GRAPHITE_DB_IP'],
				port = 8125,
				prefix = 'ReadableWebProxy.FetchAgent',
				)

		self.log.info("Setup complete!")


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
		self.put_idx = (self.put_idx + 1) % len(self.connectors)
		return self.connectors[self.put_idx].putMessage(data)
		# self.log.info("Outgoing data size: %s bytes.", len(data))


	def get_item(self):
		for x in range(len(self.connectors)):
			ret = self.connectors[x].getMessage()
			if ret:
				self.log.info("Received data size: %s bytes.", len(ret))
				return ret
		return ret

	def process_chunk(self, chunk_message):
		assert 'chunk-type'   in chunk_message
		assert 'chunk-num'    in chunk_message
		assert 'total-chunks' in chunk_message
		assert 'data'         in chunk_message
		assert 'merge-key'    in chunk_message

		total_chunks  = chunk_message['total-chunks']
		chunk_num     = chunk_message['chunk-num']
		data          = chunk_message['data']
		merge_key     = chunk_message['merge-key']

		with self.chunk_lock:
			if not merge_key in self.chunks:
				self.chunks[merge_key] = {
					'first-seen'  : datetime.datetime.now(),
					'chunk-count' : total_chunks,
					'chunks'      : {}
				}

			# Check our chunk count is sane.
			assert self.chunks[merge_key]['chunk-count'] == total_chunks
			self.chunks[merge_key]['chunks'][chunk_num] = data

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
				self.log.info("Have %s/%s items for chunk, %s different partial messages in queue.", len(self.chunks[merge_key]['chunks']), total_chunks, len(self.chunks))
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
					for line in traceback.format_exc().split("\n"):
						self.log.error(line)
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
		self.log.info("Closing connector wrapper: %s -> %s", self.logPath, self.vhost)
		for connector in self.connectors:
			connector.stop()


	def dispatch_outgoing(self):

		for qname, q in self.mdict[self.settings['taskq_name']].items():
			while not q.empty():
				try:
					job = q.get_nowait()
					jkey = uuid.uuid1().hex
					job['jobmeta'] = {
						'sort_key' : jkey,
						'qname'    : qname,
						}
					self.mon_con.incr("Fetch.Get.{}".format(qname), 1)
					self.dispatch_map[jkey] = (qname, time.time())
					self.put_job(job)
				except queue.Empty:
					break

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

			if not any(['sort_key' in new['jobmeta'], 'qname' in new['jobmeta']]):
				self.log.error("No sort key in job! Wat?")
				self.log.error("Job contents: '%s'", new)
				continue

			if 'sort_key' in new['jobmeta'] and new['jobmeta']['sort_key'] in self.dispatch_map:
				qname, started_at = self.dispatch_map[new['jobmeta']['sort_key']]
			elif 'qname' in new['jobmeta']:
				qname = new['jobmeta']['qname']
				started_at = None

			elif 'sort_key' in new['jobmeta'] and not new['jobmeta']['sort_key'] in self.dispatch_map:
				self.log.error("Job sort key not in known table! Does the job predate the current execution session?")
				self.log.error("Job key: '%s'", new['jobmeta']['sort_key'])
				self.log.error("Job contents: '%s'", new)
				continue
			else:
				self.log.error("No sort key or queue name in response!")
				self.log.error("Response meta: %s", new['jobmeta'])
				continue

			if not qname in self.mdict[self.settings['respq_name']]:
				self.log.error("Job response queue missing?")
				self.log.error("Queue name: '%s'", qname)
				continue

			self.mdict[self.settings['respq_name']][qname].put(new)

			if started_at:
				fetchtime = (time.time() - started_at) * 1000
				self.mon_con.timing("Fetch.Duration.{}".format(qname), fetchtime)
				self.log.info("Demultiplexed job for '%s'. Time to response: %s", qname, fetchtime)
			else:
				self.log.info("Demultiplexed job for '%s'. Original fetchtime missing!", qname)


			self.mon_con.incr("Fetch.Resp.{}".format(qname), 1)



	def runner(self):
		self.mdict['amqp_runstate'] = True

		while self.mdict['amqp_runstate']:
			time.sleep(1)
			self.dispatch_outgoing()
			self.process_retreived()

		self.log.info("Saw exit flag. Closing interface")
		self.close()


class PlainRabbitQueueHandler(object):
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

		assert "taskq_task"         in settings
		assert "taskq_response"     in settings

		assert 'taskq_name' in settings
		assert 'respq_name' in settings
		self.settings = settings

		sslopts = self.getSslOpts()
		self.vhost = settings["RABBIT_VHOST"]
		self.connector = AmqpConnector.Connector(userid                = settings["RABBIT_LOGIN"],
												password               = settings["RABBIT_PASWD"],
												host                   = settings["RABBIT_SRVER"],
												virtual_host           = settings["RABBIT_VHOST"],
												ssl                    = sslopts,
												master                 = settings['master'],
												synchronous            = settings['synchronous'],
												flush_queues           = settings['flush_queues'],
												prefetch               = settings['prefetch'],
												durable                = settings['durable'],
												heartbeat              = settings['heartbeat'],
												task_exchange_type     = settings['task_exchange_type'],
												poll_rate              = settings['poll_rate'],
												task_queue             = settings["taskq_task"],
												response_queue         = settings["taskq_response"],
												response_exchange_type = settings['response_exchange_type'],
												task_exchange          = settings["task_exchange"],
												response_exchange      = settings["response_exchange"],
												socket_timeout         = settings["socket_timeout"],
												ack_rx                 = settings["ack_rx"],
												)


		self.log.info("Connected AMQP Interface: %s", self.connector)
		self.log.info("Connection parameters: %s, %s, %s, %s", settings["RABBIT_LOGIN"], settings["RABBIT_PASWD"], settings["RABBIT_SRVER"], settings["RABBIT_VHOST"])


		self.log.info("Setting up stats reporter")

		self.mon_con = statsd.StatsClient(
				host = settings['GRAPHITE_DB_IP'],
				port = 8125,
				prefix = 'ReadableWebProxy.FetchAgent',
				)

		self.log.info("Setup complete!")

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


	def get_item(self):
		ret = self.connector.getMessage()
		if ret:
			self.log.info("Received data size: %s bytes.", len(ret))
		return ret


	def put_job(self, new_job):

		# packed_job = msgpack.packb(new_job, use_bin_type=True)
		self.connector.putMessage(new_job, synchronous=1000)

	def __del__(self):
		self.close()

	def close(self):
		self.log.info("Closing connector wrapper: %s -> %s", self.logPath, self.vhost)
		self.connector.stop()


	def dispatch_outgoing(self):
		qname = self.settings['taskq_name']
		while not self.mdict[qname].empty():
			try:
				job = self.mdict[qname].get_nowait()
				self.put_job(job)
				self.mon_con.incr("Feed.Put.{}".format(qname), 1)
			except queue.Empty:
				break

	def process_retreived(self):
		qname = self.settings['respq_name']
		while True:
			new = self.get_item()

			if not new:
				# print("No job item?", new)
				return
			self.mdict[qname].put(new)

			self.mon_con.incr("Feed.Recv.{}".format(qname), 1)


	def runner(self):
		self.mdict['amqp_runstate'] = True

		while self.mdict['amqp_runstate']:
			time.sleep(1)
			self.dispatch_outgoing()
			self.process_retreived()

		self.log.info("Saw exit flag. Closing interface")
		self.close()







STATE = {}

def monitor(manager):
	while manager['amqp_runstate']:
		for connector in STATE['rpc_instance'].connectors:
			connector.checkLaunchThread()
		STATE['feed_instance'].connector.checkLaunchThread()
		time.sleep(1)
		print("Monitor looping!")


# Note:
def startup_interface(manager):
	rpc_amqp_settings = {
		'consumer_threads'        : 4,

		'RABBIT_LOGIN'            : settings_file.RPC_RABBIT_LOGIN,
		'RABBIT_PASWD'            : settings_file.RPC_RABBIT_PASWD,
		'RABBIT_SRVER'            : settings_file.RPC_RABBIT_SRVER,
		'RABBIT_VHOST'            : settings_file.RPC_RABBIT_VHOST,
		'master'                  : True,
		'prefetch'                : 25,
		# 'prefetch'                : 5,
		'task_exchange_type'      : 'direct',
		'response_exchange_type'  : 'direct',

		'taskq_task'              : 'task.q',
		'taskq_response'          : 'response.q',

		"poll_rate"               : 1/100,

		'heartbeat'               :  45,
		'socket_timeout'          :  90,

		'flush_queues'            : False,
		'durable'                 : True,

		'taskq_name'              : 'outq',
		'respq_name'              : 'inq',

		'GRAPHITE_DB_IP'          : settings_file.GRAPHITE_DB_IP,

		'synchronous'             : False,

		'task_exchange'           : 'tasks.e',
		'response_exchange'       : 'resps.e',

		'ack_rx'                  : True
	}

	feed_amqp_settings = {
		'RABBIT_LOGIN'            : settings_file.RABBIT_LOGIN,
		'RABBIT_PASWD'            : settings_file.RABBIT_PASWD,
		'RABBIT_SRVER'            : settings_file.RABBIT_SRVER,
		'RABBIT_VHOST'            : settings_file.RABBIT_VHOST,
		'master'                  : True,
		'prefetch'                : 25,
		# 'prefetch'                : 5,
		'task_exchange_type'      : 'fanout',
		'taskq_task'              : 'task.q',
		'taskq_response'          : 'response.q',
		'response_exchange_type'  : 'direct',

		"poll_rate"               : 1/100,

		'heartbeat'               :  45,
		'socket_timeout'          :  90,

		'flush_queues'            : False,
		'durable'                 : True,

		'taskq_name'              : 'feed_outq',
		'respq_name'              : 'feed_inq',

		'GRAPHITE_DB_IP'          : settings_file.GRAPHITE_DB_IP,

		'synchronous'             : False,

		'task_exchange'           : 'tasks.e',
		'response_exchange'       : 'resps.e',

		'ack_rx'                  : True
	}

	STATE['rpc_instance'] = RabbitQueueHandler(rpc_amqp_settings, manager)
	STATE['rpc_thread'] = threading.Thread(target=STATE['rpc_instance'].runner)
	STATE['rpc_thread'].start()

	STATE['feed_instance'] = PlainRabbitQueueHandler(feed_amqp_settings, manager)
	STATE['feed_thread'] = threading.Thread(target=STATE['feed_instance'].runner)
	STATE['feed_thread'].start()

	STATE['monitor_thread'] = threading.Thread(target=monitor, args=[manager])
	STATE['monitor_thread'].start()


def shutdown_interface(manager):
	print("Halting AMQP interface")
	manager['amqp_runstate'] = False
	STATE['rpc_thread'].join()
	STATE['feed_thread'].join()
	STATE['monitor_thread'].join()

