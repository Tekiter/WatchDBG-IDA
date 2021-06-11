# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import idaapi


UTIL_VERSION = 100

PLUGIN_NAME = "WatchDbg"
PLUGIN_VERSION = [1, 0, 1]
IS_DEBUG = False


inf = idaapi.get_inf_structure()
WORD_SIZE = 2
if inf.is_32bit():
    WORD_SIZE = 4
elif inf.is_64bit():
    WORD_SIZE = 8


def debugline(msg):
    if IS_DEBUG:
        print("[DEBUG:%s] %s" % (PLUGIN_NAME, msg))


def writeline(msg):
    print("[%s] %s" % (PLUGIN_NAME, msg))


def strToHex(string):
    try:
        return ''.join(["%02X" % ord(x) for x in string])
    except:
        return "??"


def readMemory(address, size):
    if idaapi.dbg_can_query():
        val = idaapi.dbg_read_memory(address, size)

        return val
    return None


class UIHook(idaapi.UI_Hooks):
    def __init__(self):
        idaapi.UI_Hooks.__init__(self)

        self.popups = []

    def finish_populating_tform_popup(self, form, popup):
        #formtype = idaapi.get_tform_type(form)

        # if formtype == idaapi.BWN_DISASM or idaapi.BWN_DUMP:

        for action, position, condition in self.popups:
            if condition(form):
                idaapi.attach_action_to_popup(form, popup, action, position)

    def addPopup(self, action, position="", condition=lambda f: True):
        self.popups.append((action, position, condition))


class WatchDbgHook(idaapi.DBG_Hooks):

    def dbg_process_start(self, pid, tid, ea, name, base, size):
        pass

    def dbg_process_exit(self, pid, tid, ea, code):
        pass

    def dbg_library_unload(self, pid, tid, ea, info):

        return 0

    def dbg_process_attach(self, pid, tid, ea, name, base, size):
        pass

    def dbg_process_detach(self, pid, tid, ea):

        return 0

    def dbg_library_load(self, pid, tid, ea, name, base, size):
        pass

    def dbg_bpt(self, tid, ea):

        return 0

    def dbg_suspend_process(self):
        print("Process suspended")

    def dbg_exception(self, pid, tid, ea, exc_code, exc_can_cont, exc_ea, exc_info):

        return 0

    def dbg_trace(self, tid, ea):

        return 0

    def dbg_step_into(self):
        pass

    def dbg_run_to(self, pid, tid=0, ea=0):
        pass

    def dbg_step_over(self):
        pass
