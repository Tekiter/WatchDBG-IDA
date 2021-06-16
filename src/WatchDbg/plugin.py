# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from WatchDbg.util import writeline, debugline, PLUGIN_VERSION
from WatchDbg.watchview import WatchModel, WatchViewer, convertVarName
from WatchDbg.core.watch import Watcher
from WatchDbg.core.types import parseType


class WatchDbgPlugin:

    def __init__(self, ida_api):
        self.ida = ida_api

    def on_init(self):

        self.window = WatchService(ida_api=self.ida)

        self.register_shortcut_and_menu()
        self.register_debug_hook()

        writeline("Successfully loaded! [v.%s]" %
                  '.'.join(map(str, PLUGIN_VERSION)))

    def on_term(self):
        self.cleanup_shortcut_and_menu()
        self.cleanup_debug_hook()

    def register_shortcut_and_menu(self):
        self.ida.Action.register_action(
            "add_watch", "Add Watch", lambda: self.window.show_add_watch(), "Shift-A")
        self.ida.Action.register_action(
            "show_watch_view", "Show WatchDbg List", lambda: self.window.show_watch(), "Shift-W")
        self.ida.Action.add_action_to_menu(
            "show_watch_view", "Debugger/WatchDbg")

    def register_debug_hook(self):
        self.ida.Debug.set_hook_on_process_pause(
            lambda: self.window.update_watch())

    def cleanup_shortcut_and_menu(self):
        self.ida.Action.unregister_action("add_watch")
        self.ida.Action.unregister_action("show_watch_view")

    def cleanup_debug_hook(self):
        self.ida.Debug.remove_all_hooks()


class WatchService:
    def __init__(self, ida_api):
        self.ida = ida_api
        self.watch = Watcher()
        self.view = None

    def show_add_watch(self):
        name = self.ida.Modal.request_string("Target address")

        addr = convertVarName(name)
        if addr > 0:
            self.watch.add(addr, name)
            if self.view:
                self.view.model.update()
            debugline("Watch %d added: 0x%X" % (self.watch.count(), addr))

    def show_change_type(self):
        if len(self.view.tree.selectedIndexes()) <= 0:
            return

        index = self.view.tree.selectedIndexes()[0]
        if not index.internalPointer().canchangetype:
            return

        inp = self.ida.Modal.request_string("New Type")

        if inp != None and inp.rstrip() != "":
            typ = parseType(inp)
            if typ == None:
                return

            debugline("change type to %s" % typ.typerepr())
            self.view.model.changeType(index, typ)
        self.view.model.update()

    def show_change_name(self):
        if len(self.view.tree.selectedIndexes()) <= 0:
            return

        index = self.view.tree.selectedIndexes()[0]
        item = index.internalPointer()

        inp = self.ida.Modal.request_string("New Name")

        if inp != None and inp.rstrip() != "":
            item.setName(inp)
            self.view.model.update()

    def remove_all(self):
        self.view.model = WatchModel(self.watch)
        self.watch.clear()
        self.view.model.update()
        self.view.tree.setModel(self.view.model)

    def show_watch(self):
        debugline("showing view!")
        if self.view and not self.view.isclosed:
            self.view.model.update()
            debugline("refresh!")
            return
        else:
            self.model = WatchModel(self.watch)
            self.model.update()
            self.view = WatchViewer(self.model)
            self.view.on_add_click = self.show_add_watch
            self.view.on_change_type_click = self.show_change_type
            self.view.on_change_name_click = self.show_change_name
            self.view.on_remove_all_click = self.remove_all
            self.view.Show("Watch View")

    def update_watch(self):
        if self.view and not self.view.isclosed:
            self.view.model.update()
            debugline("auto refresh!")

    def print_watch(self):
        lst = self.watch.getList()
        for i in lst:

            val = i.value()
            debugline("%d | %s\t  %s" % (i.id(), i.address(), val))
