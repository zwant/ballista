from setuptools import setup, find_packages

requires = [
	'Ballista-lib',
	'Flask',
	'redis-py'
]

setup(
    name = "ballista",
    version = "0.1",
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = requires,
)
