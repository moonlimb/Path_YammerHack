#!/usr/bin/env python
from setuptools import setup, find_packages
import os, re

VERSION_FILE = os.path.join('yammer', '_version.py')
version = 'unknown'
try:
    content = open(VERSION_FILE, 'rt').read()
except EnvironmentError:
    pass
else:
    m = re.search('^\s*__version__\s*=\s*[\'\"]([^\'\"]*)[\'\"]', content, re.M)
    if m:
        version = m.group(1)
    else:
        raise RuntimeError('unable to parse version from %s' % VERSION_FILE)


setup(name='python-yammer',
      version=version,
      description='Library for interacting with the Yammer API',
      author='James Turk, Adam Gschwender',
      author_email='jturk@sunlightfoundation.com, adam.gschwender@mccann.com',
      url='http://github.com/McCannErickson/python-yammer/',
      packages=find_packages(),
      long_description=open('README.rst').read(),
      license='BSD',
      platforms=['any'],
      keywords=['yammer'],
      zip_safe=True,
      install_requires=['oauth2', 'httplib2'],
      test_suite='tests',
      tests_require=['coverage', 'mock'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
      )
