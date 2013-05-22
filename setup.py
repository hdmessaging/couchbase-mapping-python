#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2009 Christopher Lenz
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
try:
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False

# Build setuptools-specific options (if installed).
if not has_setuptools:
    print "WARNING: setuptools/distribute not available. Console scripts will not be installed."
    setuptools_options = {}
else:
    setuptools_options = {
        'install_requires': ['couchbase==0.8.2'],
        'test_suite': 'couchdb.tests.suite',
        'zip_safe': True,
    }


setup(
    name='CouchbaseMapping',
    version='0.1.0',
    description='Python object mapping for Couchbase',
    long_description=open('README.rst').read(),
    author='HDmessaging',
    author_email='support@hdmessaging.com',
    license='BSD',
    url='https://github.com/hdmessaging/couchbase-mapping-python/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['couchbase_mapping', 'couchbase_mapping.tests'],
    **setuptools_options
)
