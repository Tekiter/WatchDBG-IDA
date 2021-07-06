# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import idaapi

UTIL_VERSION = 100

PLUGIN_NAME = "WatchDbg"
PLUGIN_VERSION = [1, 0, 1]


inf = idaapi.get_inf_structure()
WORD_SIZE = 2
if inf.is_32bit():
    WORD_SIZE = 4
elif inf.is_64bit():
    WORD_SIZE = 8


def debug_callback(): return False


def set_debug_flag_getter(fn):
    global debug_callback
    debug_callback = fn


def check_debug_flag():
    return debug_callback()


def debugline(msg):
    if check_debug_flag():
        print("[DEBUG:%s] %s" % (PLUGIN_NAME, msg))


def writeline(msg):
    print("[%s] %s" % (PLUGIN_NAME, msg))
