# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


class IMemFetcher(object):
    def fetch():
        raise NotImplementedError


class WatchTree(object):
    def __init__(self, mem_fetcher=IMemFetcher()):
        self.root = TreeNode()
        self.mem_fetcher = mem_fetcher

    def update_watch_list(self, list):
        pass

    def refetch(self):
        pass


class TreeNode(object):
    def __init__(self):
        self._children = []

    def add_child(self, child):
        self._children.append(child)

    def __iter__(self):
        return iter(self._children)
