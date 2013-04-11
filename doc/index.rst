.. -*- mode: rst; encoding: utf-8 -*-

Introduction
============

``couchbase_mapping`` is Python package for mapping Couchbase_ documents to
Python objects. It makes use of the official Couchbase Python client and adds
a higher level interface on top of it.
The package consists of the following main modules:

* ``couchbase_mapping.mapping``: This module provides advanced mapping between
  Couchbase JSON documents and Python objects.

* ``couchbase_mapping.design``: This module includes an abstraction for
  Couchbase views that can be used to create and execute views.

The source code is hosted at Github.

.. _Couchbase: http://www.couchbase.com/
.. _Couchbase Python client: https://github.com/couchbase/couchbase-python-client/
.. _Github: http://code.google.com/p/couchdb-python

Documentation
=============

.. toctree::
   :maxdepth: 2
   :numbered:

   mapping.rst
   changes.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
