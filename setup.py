from setuptools import setup
import os


# Get version without importing, which avoids dependency issues
def get_version():
    import re
    with open('imbox/version.py') as version_file:
        return re.search(r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""",
                         version_file.read()).group('version')


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


setup(
    name='imbox',
    version=get_version(),
    description="Python IMAP for Human beings",
    long_description=read('README.md'),
    keywords='email, IMAP, parsing emails',
    author='Martin Rusev',
    author_email='martin@amon.cx',
    url='https://github.com/martinrusev/imbox',
    license='MIT',
    packages=['imbox', 'imbox.vendors'],
    package_dir={'imbox': 'imbox'},
    install_requires=[
        'chardet',
    ],
    python_requires='>=3.3',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
)
