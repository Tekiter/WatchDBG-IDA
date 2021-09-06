from __future__ import absolute_import, division, print_function

import unittest
from utils import import_src

module = import_src('WatchDbg.core.watchtree')

WatchTree = module.WatchTree
WatchList = import_src('WatchDbg.core.watch').WatchList
types = import_src('WatchDbg.type.newtypes')


class DummyMemFetcher:
    dummybytes = b'\x12\x34\x56\x78\xde\xad\xbe\xef'

    @staticmethod
    def getdummy(size):
        return DummyMemFetcher.dummybytes[:size]

    def fetch(self, address, size):

        return DummyMemFetcher.getdummy(size)


class TestWatchTreeApply(unittest.TestCase):
    def test_clean_apply(self):
        wl = WatchList()
        wl.add(0x10, 'item1', types.SignedInt(4))
        wl.add(0x14, 'item2', types.SignedInt(4))
        wl.add(0x18, 'item3', types.SignedInt(2))

        wt = WatchTree(DummyMemFetcher())
        wt.apply_watch_list(wl)

        self.assertEqual(len(wt.children), 3)

    def test_duplicate_apply(self):
        wl = WatchList()
        wl.add(0x10, 'item1', types.SignedInt(4))
        wl.add(0x14, 'item2', types.SignedInt(4))
        wl.add(0x18, 'item3', types.SignedInt(2))

        wt = WatchTree(DummyMemFetcher())
        wt.apply_watch_list(wl)
        wt.apply_watch_list(wl)

        self.assertEqual(len(wt.children), 3)
        self.assertEqual(wt.children[0].name, 'item1')

    def test_increment_apply(self):
        wl = WatchList()
        wl.add(0x10, 'item1', types.SignedInt(4))

        wt = WatchTree(DummyMemFetcher())
        wt.apply_watch_list(wl)

        self.assertEqual(len(wt.children), 1)

        wl.add(0x14, 'item2', types.SignedInt(4))
        wl.add(0x18, 'item3', types.SignedInt(2))
        wt.apply_watch_list(wl)

        self.assertEqual(len(wt.children), 3)

    def test_decrement_apply(self):
        wl = WatchList()
        wl.add(0x10, 'item1', types.SignedInt(4))
        todel = wl.add(0x14, 'item2', types.SignedInt(4))
        wl.add(0x18, 'item3', types.SignedInt(2))

        wt = WatchTree(DummyMemFetcher())
        wt.apply_watch_list(wl)

        wl.delete(todel)
        wt.apply_watch_list(wl)

        self.assertEqual(len(wt.children), 2)
        self.assertEqual(wt.children[0].name, 'item1')


class TestWatchTreeRefetch(unittest.TestCase):
    def reset_watch_list(self):
        self.wl = WatchList()

    def add_watch_list_int(self, address):
        return self.wl.add(address, 'item_{}'.format(address), types.SignedInt(4))

    def add_watch_list_array(self, address):
        return self.wl.add(address, 'item_{}'.format(address), types.Array(types.SignedInt(4), 10))

    def create_watch_tree(self):
        wt = WatchTree(DummyMemFetcher())
        wt.apply_watch_list(self.wl)
        return wt

    def test_fetch_int(self):
        self.reset_watch_list()
        self.add_watch_list_int(0x100)

        wt = self.create_watch_tree()
        wt.refetch()

        self.assertEqual(wt.children[0].value, DummyMemFetcher.getdummy(4))

    def test_fetch_array(self):
        self.reset_watch_list()
        self.add_watch_list_array(0x100)

        wt = self.create_watch_tree()
        wt.refetch()

        self.assertEqual(len(wt.children[0].children), 10)
        self.assertEqual(
            wt.children[0].children[0].value, DummyMemFetcher.getdummy(4))
