from __future__ import absolute_import
from __future__ import division

from PyQt5.QtCore import *
from WatchDbg.util import WORD_SIZE, debugline
from WatchDbg.core.types import *
from WatchDbg.core.watch import WatchItem


class TreeNode:
    columns = {"name": 0, "address": 1, "value": 2, "type": 3}

    def __init__(self):
        self._parent = None
        self.children = []
        self.canchangetype = False

    def row(self):
        if self._parent != None:
            return self._parent.children.index(self)
        return 0

    def childCount(self):
        return len(self.children)

    def child(self, row):
        if row < self.childCount():
            return self.children[row]
        return None

    def addChild(self, child):
        child._parent = self
        self.children.append(child)

    def parent(self):
        return self._parent

    def data(self, col):
        raise NotImplementedError()


class WatchNode(TreeNode):
    def __init__(self, watchitem, mem_reader):
        TreeNode.__init__(self)
        self.mem_reader = mem_reader

        self._watchitem = watchitem
        self.canchangetype = True

    def watchItem(self):
        return self._watchitem

    def watchId(self):
        return self._watchitem.id()

    def name(self):
        return self._watchitem.name()

    def setName(self, name):
        self._watchitem.setName(name)

    def address(self):
        return self._watchitem.address()

    def value(self):
        address = self._watchitem.address()
        typ = self._watchitem.type()
        size = typ.size
        data = self.mem_reader.read(address, size)

        if data == None:
            return None

        typ.fromraw(data)

        return typ

    def type(self):
        return self._watchitem.type()

    def typeStr(self):
        return self._watchitem.type().typerepr()

    def data(self, col):
        if col == self.columns["name"]:
            return str(self.name())
        if col == self.columns["address"]:
            return str("0x%X" % self.address())
        if col == self.columns["value"]:
            val = self.value()
            if val == None:
                return "<Cannot Access>"
            return str(val)
        if col == self.columns["type"]:
            return str(self.typeStr())
        debugline("No column matching...")
        return ""

    def canHasChildren(self):
        if self.type().typeequals(WPtr):
            val = self.value()
            return val != None
        if self.type().typeequals(WArray):
            return True
        return False


class WatchModel(QAbstractItemModel):

    def __init__(self, watch, mem_reader):
        QAbstractItemModel.__init__(self, None)
        self.mem_reader = mem_reader
        self.watch = watch
        self._root = TreeNode()

    def update(self):

        try:

            newc = []
            for i in self._root.children:
                if i.watchItem() in self.watch:

                    newc.append(i)
            self._root.children = newc

            vitems = {i.watchId(): i for i in self._root.children}

            for i in self.watch:
                if i.id() not in vitems:
                    self._root.addChild(self._create_watch_node(i))

        except Exception as e:
            debugline(e.message)
        finally:
            self.layoutChanged.emit()

    def canFetchMore(self, parent):
        if self.hasChildren(parent):
            if not parent.isValid():
                return True
            pitem = parent.internalPointer()

            if pitem.childCount() > 0:
                return False
            return True
        return False

    def fetchMore(self, parent):
        if not self.canFetchMore(parent):
            return

        if not parent.isValid():
            return

        cnodes = []

        pitem = parent.internalPointer()

        if pitem.type().typeequals(WPtr):

            val = pitem.value()
            if val == None:
                return
            rval = val.int(False)
            newitem = WatchItem(rval, WPtr())
            newitem.setName("")

            pointer_value = self.mem_reader.read(rval, WORD_SIZE)

            if self.mem_reader.read(pointer_value, WORD_SIZE) == None:
                newitem.setType(WInt())

            newnode = self._create_watch_node(newitem)

            self.beginInsertRows(parent, 0, 0)
            pitem.addChild(newnode)
            self.endInsertRows()
            return

        elif pitem.type().typeequals(WString):
            val = pitem.value()
            if val == None:
                return

            baseaddr = pitem.address()
            newnodes = []
            for i in range(val.elementcount()):
                newnode = WatchItem(
                    baseaddr + val.calcindex(i), val.elementtype())

                newnode.setName("[%d]" % i)
                newnode.canchangetype = False
                newnodes.append(self._create_watch_node(newnode))
                if newnode.value().int() == 0:
                    break

            self.beginInsertRows(parent, 0, len(newnodes)-1)
            for i in newnodes:
                pitem.addChild(i)
            self.endInsertRows()
            return

        elif pitem.type().typeequals(WArray):

            val = pitem.value()
            if val == None:
                return

            baseaddr = pitem.address()

            self.beginInsertRows(parent, 0, val.elementcount())
            for i in range(val.elementcount()):
                newnode = WatchItem(
                    baseaddr + val.calcindex(i), val.elementtype())
                newnode.setName("[%d]" % i)
                newnode.canchangetype = False
                pitem.addChild(self._create_watch_node(newnode))
            self.endInsertRows()

            return

    def hasChildren(self, parent):
        if not parent.isValid():
            return True

        pitem = parent.internalPointer()

        return pitem.canHasChildren()

    def columnCount(self, parent):
        return len(self._root.columns)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._root.columns.keys()[self._root.columns.values().index(section)]

        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if parent.isValid():
            pitem = parent.internalPointer()
        else:
            pitem = self._root

        citem = pitem.child(row)
        if citem:
            return self.createIndex(row, column, citem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        citem = index.internalPointer()
        pitem = citem.parent()

        if pitem == self._root:
            return QModelIndex()

        return self.createIndex(pitem.row(), 0, pitem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if parent.isValid():
            pitem = parent.internalPointer()
        else:
            pitem = self._root

        return pitem.childCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()
        return item.data(index.column())

    def changeType(self, index, wtype):
        item = index.internalPointer()
        item.children = []
        item.watchItem().setType(wtype)

    def isTopLevel(self, item):
        return item.parent() == self._root

    def _create_watch_node(self, watchitem):
        return WatchNode(watchitem, mem_reader=self.mem_reader)
