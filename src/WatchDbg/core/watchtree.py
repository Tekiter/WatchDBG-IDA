# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from WatchDbg.core.watch import WatchList
from WatchDbg.type.newtypes import Array


class IMemFetcher(object):
    def read(self, address, size):
        raise NotImplementedError


class Node(object):
    def __init__(self):
        self.children = []
        self.name = ""
        self.address = None
        self.value = None
        self.can_open = False
        self.is_open = False

    def append_child(self, child):
        self.children.append(child)


class ArrayNode(object):
    def __init__(self):
        super(Node, self)

    @property
    def can_open(self):
        if self.address == None:
            return False

        if self.value == None:
            return False

        return True


class PointerNode(object):
    def __init__(self):
        super(Node, self)

    @property
    def can_open(self):
        if self.address == None:
            return False

        if self.value == None:
            return False

        return True


class NodeFactory(object):
    def __init__(self):
        pass

    def watch_list_item(self, item):
        node = Node()

        node.address = item.address
        node.name = item.name

        return node

    def variable(self, type):
        if isinstance(type, Array):
            return ArrayNode()


class WatchTree(Node):
    def __init__(self, mem_fetcher):
        super(Node, self)
        self.mem_fetcher = IMemFetcher()
        self.watch_list = WatchList()
        self.mem_fetcher = mem_fetcher
        self.node_factory = NodeFactory()

    def apply_watch_list(self, watch_list):
        new_children = []
        for item in watch_list:
            found = [ch for ch in self.children if ch.id == item.id]
            if len(found) > 0:
                new_children.append(found[0])
            else:
                new_children.append(self.node_factory.watch_list_item(item))
        self.children = new_children

    def refetch(self):
        def f(node):
            value = self.mem_fetcher.fetch(node.address, node.size)
            node.value = value

        for ch in self.children:
            f(ch)


class VariableNode(Node):
    def __init__(self):
        super(Node, self)


class ConstantNode(Node):
    def __init__(self):
        super(Node, self)
