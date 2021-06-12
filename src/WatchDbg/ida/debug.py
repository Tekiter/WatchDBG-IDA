import idaapi


debug_hooks = []


class Debug:
    @staticmethod
    def set_hook_on_process_pause(callback):
        hook = WatchDbgHook()
        hook.dbg_suspend_process = callback
        hook.hook()
        debug_hooks.append(hook)

    @staticmethod
    def remove_all_hooks():
        for hook in debug_hooks:
            hook.unhook()

        del debug_hooks[:]

    @staticmethod
    def read_memory(address, size):
        if idaapi.dbg_can_query():
            val = idaapi.dbg_read_memory(address, size)
            if val == None:
                return None
            return val
        return None


class WatchDbgHook(idaapi.DBG_Hooks):
    pass
