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
