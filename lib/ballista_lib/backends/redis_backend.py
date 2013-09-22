import redis
from ballista_lib.backends import Backend
from ballista_lib import BallistaException

NAMESPACE = 'ballista'

class RedisBackend(Backend):
	name = 'REDIS'

	def __init__(self, host=None, port=None, db=None):
		if host and port and db:
			self.redis = redis.StrictRedis(host=host, 
										   port=port, 
										   db=db)
		else:
			raise BallistaException('The Redis backend requires host, port and db')
	
	def get_features(self):
		return self.redis.smembers(self._all_features_key())

	def remove_feature(self, feature):
		pipe = self.redis.pipeline()
		pipe.delete(self._feature_key(feature))
		pipe.srem(self._all_features_key(), feature)
		pipe.execute()

	def get_strategy(self, feature):
		return NotImplementedError('Please use a implementation backend and not the base class')

	def set_strategy(self, feature, strategy, **kwargs):
		return NotImplementedError('Please use a implementation backend and not the base class')

	def remove_strategy(self, feature):
		return NotImplementedError('Please use a implementation backend and not the base class')

	def _all_features_key(self):
		return '{namespace}/all-features'.format(namespace=NAMESPACE)

	def _feature_key(self, feature_name):
		return '{namespace}/features/{feature_name}'.format(namespace=NAMESPACE, feature_name=feature_name)