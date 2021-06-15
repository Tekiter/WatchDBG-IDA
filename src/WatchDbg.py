from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def PLUGIN_ENTRY():
    from WatchDbg.plugin import WatchDbgPlugin
    import WatchDbg.ida as ida_api

    plugin = ida_api.Plugin.create_plugin(
        WatchDbgPlugin(ida_api=ida_api), name="WatchDbg")
    return plugin
