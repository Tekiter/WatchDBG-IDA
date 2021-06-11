from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def PLUGIN_ENTRY():
    from WatchDbg.plugin import WatchDbgPlugin

    import WatchDbg.ida as ida_api

    return WatchDbgPlugin(ida_api=ida_api)
