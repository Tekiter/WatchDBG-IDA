#-*- coding: utf-8 -*-

import idaapi
import ida_kernwin

from idc import *
from util import *
from watch import *


class WatchDbgPlugin(idaapi.plugin_t):
    flags = idaapi.PLUGIN_HIDE
    comment = ""

    help = ""
    wanted_name = "WatchDbg"
    wanted_hotkey = ""




    def init(self):
        
        self.view = None

        # create watcher
        self.watch = Watcher()
    

        # setup actions
        self.actions = ActionManager()
        self.actions.register("addmenuwindow", "Add Watch...", self.addWatchWindow, -1, "Shift-A")
        self.actions.register("showview", "Show Watch", self.showWatchWindow, -1, "Shift-W")


        # setup menus
        self.uihook = UIHook()
        self.uihook.addPopup(self.actions.get("addmenuwindow"), "Watch/")
        self.uihook.addPopup(self.actions.get("showview"), "Watch/")
        self.uihook.hook()


        # setup hotkeys
        #self.hotkey = HotKeyManager()
        #self.hotkey.add("Shift-A", self.addWatch)
        #self.hotkey.add("Shift-S", self.addWatchWindow)
        #self.hotkey.add("Shift-X", self.showWatch)
        #self.hotkey.add("F5", sampleHotKey)
        
        self.dbghook = WatchDbgHook()
        self.dbghook.dbg_suspend_process = self.updateWatchWindow
        self.dbghook.hook()

        
        
        writeline("Successfully loaded! [v.%s]" % '.'.join(map(str,PLUGIN_VERSION)))

        return idaapi.PLUGIN_KEEP


    def run(self, arg):
        pass


    def term(self):
        if self.uihook:
            self.uihook.unhook()
        if self.dbghook:
            self.dbghook.unhook()
        self.actions.cleanup()



    def addWatch(self):
        id = self.watch.add(here())
        debugline("Watch %d added: %d -> 0x%X"%(id,self.watch.count(),here()))
    

    def addWatchWindow(self):
        name = ida_kernwin.ask_str("", 0, "Target address")
        addr = convertVarName(name)
        if addr > 0:
            self.watch.add(addr, name)
            if self.view:
                self.view.model.update()
            debugline("Watch %d added: 0x%X"%(self.watch.count(), addr))


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
    


