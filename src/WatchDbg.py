from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


WATCHDBG_FLAGS = {
    'debug': False
}


def PLUGIN_ENTRY():
    from WatchDbg.plugin import WatchDbgPlugin
    import WatchDbg.ida as ida_api

    plugin = ida_api.Plugin.create_plugin(
        WatchDbgPlugin(flags=WATCHDBG_FLAGS, ida_api=ida_api), name="WatchDbg")
    return plugin
