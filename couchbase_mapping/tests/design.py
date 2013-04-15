# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 Christopher Lenz
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

import doctest
import unittest

from couchbase_mapping import design
from couchbase_mapping.tests import testutil


class DesignTestCase(testutil.TempDatabaseMixin, unittest.TestCase):

    def test_options(self):
        options = {'collation': 'raw'}
        view = design.ViewDefinition(
            'foo', 'foo',
            'function(doc) {emit(doc._id, doc._rev)}',
            options=options)
        _, db = self.temp_db()
        view.sync(db)
        design_doc = db['_design/foo'].ddoc
        self.assertTrue(design_doc['views']['foo']['options'] == options)

    def test_multiple_views(self):
        map_by_name = 'function(doc, meta) {emit(doc.name, null)}'
        view1 = design.ViewDefinition(
            'test_multiple_views',
            'by_name',
            map_by_name)
        map_by_id = 'function(doc, meta) {emit(meta.id, null)}'
        view2 = design.ViewDefinition(
            'test_multiple_views',
            'by_id',
            map_by_id)
        _, db = self.temp_db()
        view1.sync(db)
        view2.sync(db)
        design_doc = db['_design/test_multiple_views'].ddoc
        self.assertEqual(design_doc['views']['by_name']['map'], map_by_name)
        self.assertEqual(design_doc['views']['by_id']['map'], map_by_id)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DesignTestCase))
    suite.addTest(doctest.DocTestSuite(design))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
