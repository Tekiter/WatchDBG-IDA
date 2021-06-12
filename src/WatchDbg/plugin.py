# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import idaapi

from WatchDbg.util import *
from WatchDbg.watch import *


class WatchDbgPlugin(idaapi.plugin_t):
    flags = idaapi.PLUGIN_HIDE
    comment = ""

    help = ""
    wanted_name = "WatchDbg"
    wanted_hotkey = ""

    def __init__(self, ida_api):
        idaapi.plugin_t.__init__(self)
        self.ida = ida_api

    def init(self):
        self.view = None

        # create watcher
        self.watch = Watcher()

        self.ida.Action.register_action(
            "add_watch", "Add Watch", self.addWatchWindow, "Shift-A")
        self.ida.Action.register_action(
            "show_watch_view", "Show WatchDbg List", self.showWatchWindow, "Shift-W")

        self.ida.Action.add_action_to_menu(
            "show_watch_view", "Debugger/WatchDbg")

        self.ida.Debug.set_hook_on_process_pause(self.updateWatchWindow)

        writeline("Successfully loaded! [v.%s]" %
                  '.'.join(map(str, PLUGIN_VERSION)))

        return idaapi.PLUGIN_KEEP

    def run(self, arg):
        pass

    def term(self):

        self.ida.Debug.remove_all_hooks()

        self.ida.Action.unregister_action("add_watch")
        self.ida.Action.unregister_action("show_watch_view")

    def addWatchWindow(self):
        name = self.ida.Modal.request_string("Target address")

        addr = convertVarName(name)
        if addr > 0:
            self.watch.add(addr, name)
            if self.view:
                self.view.model.update()
            debugline("Watch %d added: 0x%X" % (self.watch.count(), addr))

    def showWatchWindow(self):
        if self.view and not self.view.isclosed:
            self.view.model.update()
            debugline("refresh!")
            return

        v = WatchViewer(self.watch)

        v.Show("Watch View")
        self.view = v
        debugline("create view!")

    def updateWatchWindow(self):
        if self.view and not self.view.isclosed:
            self.view.model.update()
            debugline("auto refresh!")

    def showWatch(self):
        lst = self.watch.getList()
        for i in lst:

            val = i.value()
            debugline("%d | %s\t  %s" % (i.id(), i.address(), val))
