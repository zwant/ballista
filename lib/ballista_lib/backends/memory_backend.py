from ballista_lib.backends import Backend
from ballista_lib import BallistaException

class RedisBackend(Backend):
	name = 'MEMORY'

	def __init__(self):
		self.features = {}
	
	def get_features(self):
		return self.features.keys()

	def remove_feature(self, feature):
		del self.features[feature]

	def get_strategy(self, feature):
		return NotImplementedError('Please use a implementation backend and not the base class')

	def set_strategy(self, feature, strategy, **kwargs):
		return NotImplementedError('Please use a implementation backend and not the base class')

	def remove_strategy(self, feature):
		return NotImplementedError('Please use a implementation backend and not the base class')
