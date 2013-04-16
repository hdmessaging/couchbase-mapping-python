# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2009 Christopher Lenz
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

from decimal import Decimal
import doctest
import time
import unittest

from couchbase_mapping import design, mapping
from couchbase_mapping.tests import testutil


class DocumentTestCase(testutil.TempDatabaseMixin, unittest.TestCase):

    def test_mutable_fields(self):
        class Test(mapping.Document):
            d = mapping.DictField()
        a = Test()
        b = Test()
        a.d['x'] = True
        self.assertTrue(a.d.get('x'))
        self.assertFalse(b.d.get('x'))

    def test_automatic_id(self):
        class Post(mapping.Document):
            title = mapping.TextField()
        post = Post(title='Foo bar')
        assert post.id is None
        post.store(self.db)
        assert post.id is not None
        self.assertEqual('Foo bar', Post.load(self.db, post.id).title)

    def test_explicit_id_via_init(self):
        class Post(mapping.Document):
            title = mapping.TextField()
        post = Post(id='foo_bar', title='Foo bar')
        self.assertEqual('foo_bar', post.id)
        post.store(self.db)
        self.assertEqual('Foo bar', Post.load(self.db, 'foo_bar').title)

    def test_explicit_id_via_setter(self):
        class Post(mapping.Document):
            title = mapping.TextField()
        post = Post(title='Foo bar')
        post.id = 'foo_bar'
        self.assertEqual('foo_bar', post.id)
        post.store(self.db)
        self.assertEqual('Foo bar', Post.load(self.db, 'foo_bar').title)

    def test_store_existing(self):
        class Post(mapping.Document):
            title = mapping.TextField()
        post = Post(title='Foo bar')
        post.store(self.db)
        id = post.id
        post.store(self.db)
        self.assertEqual(id, post.id)

    def test_old_datetime(self):
        dt = mapping.DateTimeField()
        assert dt._to_python('1880-01-01T00:00:00Z')

    def test_get_has_default(self):
        doc = mapping.Document()
        doc.get('foo')
        doc.get('foo', None)


class ListFieldTestCase(testutil.TempDatabaseMixin, unittest.TestCase):

    def test_to_json(self):
        # See <http://code.google.com/p/couchdb-python/issues/detail?id=14>
        class Post(mapping.Document):
            title = mapping.TextField()
            comments = mapping.ListField(mapping.DictField(
                mapping.Mapping.build(
                    author=mapping.TextField(),
                    content=mapping.TextField(),
                )
            ))
        post = Post(title='Foo bar')
        post.comments.append(author='myself', content='Bla bla')
        post.comments = post.comments
        self.assertEqual([{'content': 'Bla bla', 'author': 'myself'}],
                         post.comments)

    def test_proxy_append(self):
        class Thing(mapping.Document):
            numbers = mapping.ListField(mapping.DecimalField)
        thing = Thing(numbers=[Decimal('1.0'), Decimal('2.0')])
        thing.numbers.append(Decimal('3.0'))
        self.assertEqual(3, len(thing.numbers))
        self.assertEqual(Decimal('3.0'), thing.numbers[2])

    def test_proxy_append_kwargs(self):
        class Thing(mapping.Document):
            numbers = mapping.ListField(mapping.DecimalField)
        thing = Thing()
        self.assertRaises(TypeError, thing.numbers.append, foo='bar')

    def test_proxy_contains(self):
        class Thing(mapping.Document):
            numbers = mapping.ListField(mapping.DecimalField)
        thing = Thing(numbers=[Decimal('1.0'), Decimal('2.0')])
        assert isinstance(thing.numbers, mapping.ListField.Proxy)
        assert '1.0' not in thing.numbers
        assert Decimal('1.0') in thing.numbers

    def test_proxy_count(self):
        class Thing(mapping.Document):
            numbers = mapping.ListField(mapping.DecimalField)
        thing = Thing(numbers=[Decimal('1.0'), Decimal('2.0')])
        self.assertEqual(1, thing.numbers.count(Decimal('1.0')))
        self.assertEqual(0, thing.numbers.count('1.0'))

    def test_proxy_index(self):
        class Thing(mapping.Document):
            numbers = mapping.ListField(mapping.DecimalField)
        thing = Thing(numbers=[Decimal('1.0'), Decimal('2.0')])
        self.assertEqual(0, thing.numbers.index(Decimal('1.0')))
        self.assertRaises(ValueError, thing.numbers.index, '3.0')

    def test_proxy_insert(self):
        class Thing(mapping.Document):
            numbers = mapping.ListField(mapping.DecimalField)
        thing = Thing(numbers=[Decimal('1.0'), Decimal('2.0')])
        thing.numbers.insert(0, Decimal('0.0'))
        self.assertEqual(3, len(thing.numbers))
        self.assertEqual(Decimal('0.0'), thing.numbers[0])

    def test_proxy_insert_kwargs(self):
        class Thing(mapping.Document):
            numbers = mapping.ListField(mapping.DecimalField)
        thing = Thing()
        self.assertRaises(TypeError, thing.numbers.insert, 0, foo='bar')

    def test_proxy_remove(self):
        class Thing(mapping.Document):
            numbers = mapping.ListField(mapping.DecimalField)
        thing = Thing()
        thing.numbers.append(Decimal('1.0'))
        thing.numbers.remove(Decimal('1.0'))

    def test_proxy_iter(self):
        class Thing(mapping.Document):
            numbers = mapping.ListField(mapping.DecimalField)
        self.db['test'] = {'numbers': ['1.0', '2.0']}
        thing = Thing.load(self.db, 'test')
        assert isinstance(thing.numbers[0], Decimal)

    def test_proxy_iter_dict(self):
        class Post(mapping.Document):
            comments = mapping.ListField(mapping.DictField)
        self.db['test'] = {'comments': [{'author': 'Joe', 'content': 'Hey'}]}
        post = Post.load(self.db, 'test')
        assert isinstance(post.comments[0], dict)

    def test_proxy_pop(self):
        class Thing(mapping.Document):
            numbers = mapping.ListField(mapping.DecimalField)
        thing = Thing()
        thing.numbers = [Decimal('%d' % i) for i in range(3)]
        self.assertEqual(thing.numbers.pop(), Decimal('2.0'))
        self.assertEqual(len(thing.numbers), 2)
        self.assertEqual(thing.numbers.pop(0), Decimal('0.0'))

    def test_proxy_slices(self):
        class Thing(mapping.Document):
            numbers = mapping.ListField(mapping.DecimalField)
        thing = Thing()
        thing.numbers = [Decimal('%d' % i) for i in range(5)]
        ll = thing.numbers[1:3]
        self.assertEqual(len(ll), 2)
        self.assertEqual(ll[0], Decimal('1.0'))
        thing.numbers[2:4] = [Decimal('%d' % i) for i in range(6, 8)]
        self.assertEqual(thing.numbers[2], Decimal('6.0'))
        self.assertEqual(thing.numbers[4], Decimal('4.0'))
        self.assertEqual(len(thing.numbers), 5)
        del thing.numbers[3:]
        self.assertEquals(len(thing.numbers), 3)

    def test_mutable_fields(self):
        class Thing(mapping.Document):
            numbers = mapping.ListField(mapping.DecimalField)
        thing = Thing.wrap({'_id': 'foo', '_rev': 1})  # no numbers
        thing.numbers.append('1.0')
        thing2 = Thing(id='thing2')
        self.assertEqual([i for i in thing2.numbers], [])


all_map_func = 'function(doc) { emit(doc._id, null); }'


class WrappingTestCase(testutil.TempDatabaseMixin, unittest.TestCase):

    class Item(mapping.Document):
        name = mapping.TextField()
        with_include_docs = mapping.ViewField('test', all_map_func,
                                              include_docs=True)
        without_include_docs = mapping.ViewField('test', all_map_func)

    def setUp(self):
        super(WrappingTestCase, self).setUp()
        design.ViewDefinition.sync_many(
            self.db, [self.Item.with_include_docs,
                      self.Item.without_include_docs])
        time.sleep(10)  # Wait for the new view to be defined and indexed.

    def test_viewfield_property(self):
        self.Item(id='1', name='item #1').store(self.db)
        time.sleep(10)
        results = self.Item.with_include_docs(self.db,
                                              connection_timeout=60000,
                                              stale=False)
        self.assertEquals(type(results[0]), self.Item)
        item = [result for result in results if result.id == '1'][0]
        self.assertEquals(item.name, 'item #1')

        results = self.Item.without_include_docs(self.db,
                                                 connection_timeout=60000,
                                                 stale=False)
        self.assertEquals(type(results[0]), self.Item)

    def test_view(self):
        self.Item(id='2', name='item #2').store(self.db)
        time.sleep(10)
        results = self.Item.view(self.db,
                                 '_design/test/_view/without_include_docs',
                                 connection_timeout=60000,
                                 stale=False)
        self.assertEquals(type(results[0]), self.Item)
        results = self.Item.view(self.db,
                                 '_design/test/_view/without_include_docs',
                                 connection_timeout=60000,
                                 stale=False,
                                 include_docs=True)
        self.assertEquals(type(results[0]), self.Item)
        item = [result for result in results if result.id == '2'][0]
        self.assertEquals(item.name, 'item #2')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocTestSuite(mapping))
    suite.addTest(unittest.makeSuite(DocumentTestCase, 'test'))
    suite.addTest(unittest.makeSuite(ListFieldTestCase, 'test'))
    suite.addTest(unittest.makeSuite(WrappingTestCase, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
