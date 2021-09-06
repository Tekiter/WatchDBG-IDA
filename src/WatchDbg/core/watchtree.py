# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import WatchDbg.type.newtypes as types


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

    def update_children(self):
        pass

    def fetch(self):
        pass


class VariableNode(Node):
    def __init__(self, mem_fetcher, name, address, type):
        super(VariableNode, self).__init__()
        self.mem_fetcher = mem_fetcher
        self.name = name
        self.address = address
        self.type = type

    def fetch(self):
        self.value = self.mem_fetcher.fetch(self.address, self.type.size)


class ArrayNode(VariableNode):
    def __init__(self, factory, mem_fetcher, name, address, type):
        super(ArrayNode, self).__init__(mem_fetcher, name, address, type)
        self.factory = factory

    def update_children(self):
        new_children = []
        element_type = self.type.element_type

        for i in range(self.type.length):
            index_str = "[{}]".format(i)
            next_address = self.address + element_type.size * i

            node = self.factory.variable(
                name=index_str, address=next_address, type=element_type)

            new_children.append(node)

        self.children = new_children

    def fetch(self):
        self.value = self.mem_fetcher.fetch(self.address, self.type.size)


class PointerNode(VariableNode):
    def __init__(self, mem_fetcher, *args, **kwargs):
        super(PointerNode, self).__init__(mem_fetcher, *args, **kwargs)

    @property
    def can_open(self):
        if self.address == None:
            return False

        if self.value == None:
            return False

        return True


class NodeFactory(object):
    def __init__(self, mem_fetcher):
        self.mem_fetcher = mem_fetcher

    def watch_list_item(self, item):
        node = self.variable(item.name, item.address, item.type)
        setattr(node, 'id', item.id)
        return node

    def variable(self, name, address, type):
        if isinstance(type, types.Array):
            return ArrayNode(self, self.mem_fetcher, name, address, type)
        return VariableNode(self.mem_fetcher, name, address, type)


class WatchTree(Node):
    def __init__(self, mem_fetcher):
        super(WatchTree, self).__init__()
        self.mem_fetcher = IMemFetcher()
        self.mem_fetcher = mem_fetcher
        self.node_factory = NodeFactory(mem_fetcher)

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
            value = self.mem_fetcher.fetch(node.address, node.type.size)
            node.value = value
            node.update_children()
            for ch in node.children:
                f(ch)

        for ch in self.children:
            f(ch)


class ConstantNode(Node):
    def __init__(self):
        super(Node, self)
