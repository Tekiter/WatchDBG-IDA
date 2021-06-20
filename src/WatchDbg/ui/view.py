# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PyQt5.QtWidgets import (QPushButton,  QVBoxLayout,  QTreeView,
                             QHBoxLayout, QShortcut)
from PyQt5.QtCore import Qt
from WatchDbg.common import EventHandler
from WatchDbg.util import debugline
from WatchDbg.ui.model import TreeNode


class WatchViewer(object):

    def __init__(self, form, model):
        self.isclosed = False
        self.model = model
        self.tree = None
        self.form = form
        form.title = "Watch View"
        form.on_create.attach(self.OnCreate)
        form.on_close.attach(self.OnClose)

        self.on_add = EventHandler()
        self.on_change_name = EventHandler()
        self.on_change_type = EventHandler()
        self.on_remove_all = EventHandler()
        self.on_remove_selected = EventHandler()

    def OnCreate(self, widget):
        self.parent = widget
        self.CreateForm()

    def CreateForm(self):
        self._set_treeview()
        self._draw_layout()
        self._connect_shortcuts()

        # dkeyshortcut = QShortcut(Qt.Key_D, self.tree)
        # dkeyshortcut.activated.connect(self.removeSelected)

        debugline("View Created!")

    def show(self):
        self.form.show()

    def set_new_model(self, model):
        self.model = model
        if self.tree:
            self.tree.setModel(model)
        model.update()

    def is_selected(self):
        return len(self.tree.selectedIndexes()) > 0

    def get_selected_index(self):
        index = self.tree.selectedIndexes()[0]
        return index

    def get_selected_item(self):
        index = self.get_selected_index()
        return index.internalPointer()

    def OnClose(self, e):
        self.isclosed = True

    def _set_treeview(self):
        tree = QTreeView()

        tree.setModel(self.model)
        self.model.update()
        self.tree = tree
        self.tree.setColumnWidth(TreeNode.columns["value"], 350)
        self.tree.setColumnWidth(TreeNode.columns["address"], 180)

    def _draw_layout(self):

        layout = QVBoxLayout()

        layout.addWidget(self.tree)

        toolbar = QHBoxLayout()
        toolbar.addStretch()

        toolbar.addWidget(create_button(
            content="+",
            tooltip="Add an address to watch",
            onclick=self.on_add.notify))

        toolbar.addWidget(create_button(
            content="T",
            tooltip="Change type",
            onclick=self.on_change_type.notify))

        # toolbar.addWidget(create_button(
        #     content="-",
        #     tooltip="Remove a watch item",
        #     onclick=self.on_remove_selected_click))

        toolbar.addWidget(create_button(
            content="X",
            tooltip="Remove ALL items",
            onclick=self.on_remove_all.notify))

        layout.addLayout(toolbar)

        self.parent.setLayout(layout)

    def _connect_shortcuts(self):
        tkeyshortcut = QShortcut(Qt.Key_T, self.tree)
        tkeyshortcut.activated.connect(self.on_change_name.notify)

        nkeyshortcut = QShortcut(Qt.Key_N, self.tree)
        nkeyshortcut.activated.connect(self.on_change_name.notify)

        akeyshortcut = QShortcut(Qt.Key_A, self.tree)
        akeyshortcut.activated.connect(self.on_add.notify)


def nop_function(*args, **kwargs):
    pass


def create_button(content="", tooltip="", onclick=nop_function):
    btn = QPushButton(content)
    btn.setToolTip(tooltip)
    btn.clicked.connect(onclick)
    return btn
