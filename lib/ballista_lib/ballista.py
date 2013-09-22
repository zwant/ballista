import backends

BACKENDS = {backend_class.name: backend_class for backend_class in backends.Backend.__subclasses__()}

class Ballista(object):
	def __init__(self, user_id, request, backend, **kwargs):
		if backend not in BACKENDS:
			raise BallistaException('Backend {0} is not available. Available backends are: {1}'.format(backend, BACKENDS.keys()))

		self.backend = BACKENDS[backend](**kwargs)
		self.request = request
		self.user_id = user_id

	def load(self, feature_name, *args):
		return self.backend.get_feature(feature_name).load(*args)

	def fire(self, feature_name):
		return self.backend.get_feature(feature_name).fire(self.user_id, self.request)
