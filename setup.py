from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in gulf_vision/__init__.py
from gulf_vision import __version__ as version

setup(
	name="gulf_vision",
	version=version,
	description="multiple industries",
	author="abdul basit ali",
	author_email="custom@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
