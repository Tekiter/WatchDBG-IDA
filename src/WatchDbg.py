from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def PLUGIN_ENTRY():
    from WatchDbg.plugin import WatchDbgPlugin
    return WatchDbgPlugin()
