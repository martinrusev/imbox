from setuptools import setup

version = '0.2'

setup(
	name='mailbox',
	version=version,
	description="Python library for reading IMAP email boxes and parsing the content to JSON",
	long_description= open('README.md').read(),
	keywords='email, IMAP, email to json',
	author='Martin Rusev',
	author_email='martinrusev@live.com',
	url='https://github.com/martinrusev/mailbox',
	license='MIT',
	packages=['mailbox'],
	package_dir={'mailbox':'mailbox'},
	zip_safe=False,
	install_requires=[],

) 