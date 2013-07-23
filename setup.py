from setuptools import setup

version = '0.3'

setup(
	name='mailbox',
	version=version,
	description="Python library for readin IMAP mailboxes and parsing emails",
	long_description= open('README.md').read(),
	keywords='email, IMAP, parsing emails',
	author='Martin Rusev',
	author_email='martinrusev@live.com',
	url='https://github.com/martinrusev/mailbox',
	license='MIT',
	packages=['mailbox'],
	package_dir={'mailbox':'mailbox'},
	zip_safe=False,
	install_requires=[],

) 