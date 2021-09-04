from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest
from utils import import_src

watch = import_src('WatchDbg.core.watch')

WatchList = watch.WatchList
WatchListItem = watch.WatchListItem


def dummyType(): return None


class TestWatcher(unittest.TestCase):
    def testAdd(self):
        watch = create_watch()
        self.assertEqual(len(watch), 2)

    def testClear(self):
        watch = create_watch()
        watch.clear()
        self.assertEqual(len(watch), 0)

    def testExists(self):
        watch = create_watch()
        self.assertTrue(watch.exists(0x1234))
        self.assertFalse(watch.exists(0xffff))

    def testDelete(self):
        watch = create_watch()
        item = watch.delete(0x1234)
        self.assertEqual(item.address, 0x1234)
        self.assertEqual(len(watch), 1)

        watch = create_watch()
        self.assertIsNone(watch.delete(0xffff))
        self.assertEqual(len(watch), 2)

    def testIter(self):
        watch = create_watch()
        arr = list(watch)
        self.assertEqual(len(arr), 2)
        self.assertIn(watch.get(0x1234), arr)
        self.assertIn(watch.get(0x5678), arr)
        self.assertIsNone(watch.get(0xffff), arr)


def create_watch():
    watch = WatchList()
    watch.add(0x1234, 'test1', dummyType())
    watch.add(0x5678, 'test2', dummyType())
    return watch
