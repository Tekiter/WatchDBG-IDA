from __future__ import print_function
import idaapi



def PLUGIN_ENTRY():
    from WatchDbg.plugin import WatchDbgPlugin
    return WatchDbgPlugin()
	
	
	
