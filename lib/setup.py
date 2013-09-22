from setuptools import setup, find_packages

requires = [
	'redis'
]

setup(
    name = "ballista-lib",
    version = "0.1",
    packages = find_packages('ballista_lib'),
    package_dir = {'': 'ballista_lib'},
    install_requires = requires,
)
