# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import idaapi
import ida_kernwin
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox, QTreeView, QMenu,
                             QHBoxLayout, QShortcut)
from PyQt5.QtCore import *
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QKeySequence
from WatchDbg.util import *
from WatchDbg.core.types import *
from WatchDbg.core.watch import WatchItem


def convertVarName(varstr):
    addr = ida_kernwin.str2ea(varstr)
    if addr != idaapi.BADADDR:
        return addr

    return 0


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


class ConstantNode(TreeNode):
    def __init__(self, *data):
        TreeNode.__init__(self)
        self._data = data

    def data(self, col):
        return self._data[col]


class WatchNode(TreeNode):
    def __init__(self, watchitem):
        TreeNode.__init__(self)
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
        return self._watchitem.value()

    def type(self):
        return self._watchitem.type()

    def typeStr(self):
        return self._watchitem.typeStr()

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

    def __init__(self, watch):
        QAbstractItemModel.__init__(self, None)
        self.watch = watch
        self._root = TreeNode()

    def update(self):

        try:
            watch = self.watch.getList()

            newc = []
            for i in self._root.children:
                if i.watchItem() in watch:

                    newc.append(i)
            self._root.children = newc

            vitems = {i.watchId(): i for i in self._root.children}

            for i in watch:
                if i.id() not in vitems:
                    self._root.addChild(WatchNode(i))

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

        if isinstance(pitem, ConstantNode):
            return
        elif pitem.type().typeequals(WPtr):

            val = pitem.value()
            if val == None:
                return
            rval = val.int(False)
            newitem = WatchItem(rval, WPtr())
            newitem.setName("")

            if readMemory(readMemory(rval, WORD_SIZE), WORD_SIZE) == None:
                newitem.setType(WInt())

            newnode = WatchNode(newitem)

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
                newnodes.append(WatchNode(newnode))
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
                pitem.addChild(WatchNode(newnode))
            self.endInsertRows()

            return

    def hasChildren(self, parent):
        if not parent.isValid():
            return True

        pitem = parent.internalPointer()
        if isinstance(pitem, ConstantNode):
            return False

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


class WatchViewer(idaapi.PluginForm):

    def __init__(self, watch):
        idaapi.PluginForm.__init__(self)
        self.watch = watch
        self.isclosed = False
        self.callbacks = {}

    def OnCreate(self, form):

        self.parent = self.FormToPyQtWidget(form)
        self.CreateForm()

    def CreateForm(self):

        layout = QVBoxLayout()

        tree = QTreeView()
        model = WatchModel(self.watch)
        model.update()
        tree.setModel(model)
        self.tree = tree
        self.model = model
        self.tree.setColumnWidth(TreeNode.columns["value"], 350)
        self.tree.setColumnWidth(TreeNode.columns["address"], 180)

        layout.addWidget(self.tree)

        toolbar = QHBoxLayout()
        toolbar.addStretch()

        addbtn = QPushButton("+")
        addbtn.setToolTip("Add an address to watch")
        addbtn.clicked.connect(self.add)
        toolbar.addWidget(addbtn)

        typebtn = QPushButton("T")
        typebtn.setToolTip("Change type")
        typebtn.clicked.connect(self.changeType)
        toolbar.addWidget(typebtn)

        removebtn = QPushButton("-")
        removebtn.setToolTip("Remove a watch item")
        removebtn.clicked.connect(self.removeSelected)
        # toolbar.addWidget(removebtn)

        removeallbtn = QPushButton("X")
        removeallbtn.setToolTip("Remove ALL items")
        removeallbtn.clicked.connect(self.removeAll)
        toolbar.addWidget(removeallbtn)

        layout.addLayout(toolbar)

        tkeyshortcut = QShortcut(Qt.Key_T, self.tree)
        tkeyshortcut.activated.connect(self.changeType)

        nkeyshortcut = QShortcut(Qt.Key_N, self.tree)
        nkeyshortcut.activated.connect(self.changeName)

        akeyshortcut = QShortcut(Qt.Key_A, self.tree)
        akeyshortcut.activated.connect(self.add)

        # dkeyshortcut = QShortcut(Qt.Key_D, self.tree)
        # dkeyshortcut.activated.connect(self.removeSelected)

        debugline("View Created!")
        self.parent.setLayout(layout)

    def OnClose(self, form):
        self.isclosed = True

    def add(self):
        name = ida_kernwin.ask_str("", 0, "Target address")
        addr = convertVarName(name)
        if addr > 0:
            self.watch.add(addr, name)
            self.model.update()
            debugline("Watch %d added: 0x%X" % (self.watch.count(), addr))

    def removeSelected(self):

        if len(self.tree.selectedIndexes()) <= 0:
            return
        idx = self.tree.selectedIndexes()[0]
        item = idx.internalPointer()
        if not self.model.isTopLevel(item):
            return

        self.model.beginRemoveRows(
            self.model.parent(idx), item.row(), item.row())
        self.watch.removeById(item.watchId())
        self.model.endRemoveRows()
        print(item.watchId())
        # self.watch.removeById(item.watchId())
        # self.model.update()

    def removeAll(self):

        self.model = WatchModel(self.watch)
        self.watch.clear()
        self.update()
        self.tree.setModel(self.model)

    def changeType(self):
        if len(self.tree.selectedIndexes()) <= 0:
            return

        index = self.tree.selectedIndexes()[0]
        if not index.internalPointer().canchangetype:
            return

        inp = ida_kernwin.ask_str("", 0, "New Type")

        if inp != None and inp.rstrip() != "":
            typ = parseType(inp)
            if typ == None:
                return

            debugline("change type to %s" % typ.typerepr())

            self.model.changeType(index, typ)

        self.update()

    def changeName(self):
        if len(self.tree.selectedIndexes()) <= 0:
            return

        index = self.tree.selectedIndexes()[0]
        item = index.internalPointer()

        inp = ida_kernwin.ask_str("", 0, "New Name")

        if inp != None and inp.rstrip() != "":

            item.setName(inp)
            self.update()

    def update(self):
        self.model.update()
