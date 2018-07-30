from setuptools import setup
import os

import imbox

version = imbox.__version__


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
    packages=['imbox', 'imbox.vendors'],
    package_dir={'imbox': 'imbox'},
    zip_safe=False,
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ),
    test_suite='tests',
)
