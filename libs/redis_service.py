# Python Level Imports
import redis
import logging

# django imports
from django.conf import settings

logger = logging.getLogger(__name__)


HOST = 'localhost'
PASSWORD = 'Bmcu28VN'

class MyRedisClient(object):
	"""
	Redis client for Leads app
	"""
	# def __init__(self, host=HOST, port=PORT, db=DB, password=PASSWORD):
	def __init__(self, host=HOST, password=PASSWORD):
		"""
		Init of redis client
		"""
		# pool = redis.ConnectionPool(
		#     socket_timeout=10,
		#     socket_connect_timeout=10,
		#     host=host,
		#     port=port,
		#     db=db,
		#     password=password,
		#     decode_responses=True,
		# )
		# self.client = redis.Redis(connection_pool=pool)
		self.conn_radis = redis.Redis(host='localhost',password="Bmcu28VN")


	def insert_Key_data(self,key,data,ex=None):
		try:
			if ex :
				self.conn_radis.set(key,data,ex)
			else:
				self.conn_radis.set(key,data)
			logger.info("Mail Sent ")
			return 1
		except:
			logger.error("Insertion of data to redis is failed", exc_info=True)


	def get_Key_data(self,key):
		try:
			return self.conn_radis.get(key)	
		except:
			logger.error("Getting data from redis is failed", exc_info=True)

	def delete_Key_data(self,key):
		try:
			self.conn_radis.delete(key)
			return 1
		except:
			logger.error("Dleleting data is failed", exc_info=True)

	def key_exists(self,key):
		try:
			return self.conn_radis.exists(key)
		except:
			logger.error("redis connection Failed", exc_info=True)

