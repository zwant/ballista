class Backend(object):
	name = None

	def get_features(self):
		return NotImplementedError('Please use a implementation backend and not the base class')

	def remove_feature(self, feature):
		return NotImplementedError('Please use a implementation backend and not the base class')

	def get_strategy(self, feature):
		return NotImplementedError('Please use a implementation backend and not the base class')

	def set_strategy(self, feature, strategy, **kwargs):
		return NotImplementedError('Please use a implementation backend and not the base class')

	def remove_strategy(self, feature):
		return NotImplementedError('Please use a implementation backend and not the base class')