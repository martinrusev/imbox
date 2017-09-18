from setuptools import setup
import os

version = '0.9'


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name='imbox',
    version=version,
    description="Python IMAP for Human beings",
    long_description=read('README.rst'),
    keywords='email, IMAP, parsing emails',
    author='Martin Rusev',
    author_email='martin@amon.cx',
    url='https://github.com/martinrusev/imbox',
    license='MIT',
    packages=['imbox'],
    package_dir={'imbox': 'imbox'},
    zip_safe=False,
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ),
)
