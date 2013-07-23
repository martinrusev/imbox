#!/usr/bin/env python
import os


def fullsplit(path, result=None):
	"""
	Split a pathname into components (the opposite of os.path.join) in a
	platform-neutral way.
	"""
	if result is None:
		result = []
	head, tail = os.path.split(path)
	if head == '':
		return [tail] + result
	if head == path:
		return result
	return fullsplit(head, [tail] + result)

def read(filename):
	return open(os.path.join(os.path.dirname(__file__), filename)).read()

packages, data_files = [], []
root_dir = os.path.dirname(__file__)

for dirpath, dirnames, filenames in os.walk(root_dir):
	# Ignore dirnames that start with '.'
	for i, dirname in enumerate(dirnames):
		if dirname.startswith('.'): del dirnames[i]
	if '__init__.py' in filenames:
		packages.append('.'.join(fullsplit(dirpath)))
	elif filenames:
		data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])


sdict = {
	'name' : 'mailbox',
	'version' : 0.1,
	'long_description' : read('README.md'),
	'author' : 'Martin Rusev',
	'author_email' : 'martinrusev@live.com',
	'packages' : packages,
	'data_files' : data_files,
	'install_requires': 
	[
		'pip',
	],
   }

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(**sdict)
