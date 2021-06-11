import idaapi

ID_PREFIX = "WATCHDBG_PLUGIN:"


class Action:
    @staticmethod
    def register_action(id, text, callback, shortcut=None):
        uid = _prefixed_id(id)
        action = idaapi.action_desc_t(
            uid, text, _ActionHandler(uid, callback), shortcut, None, -1)
        idaapi.register_action(action)

    @staticmethod
    def unregister_action(id):
        uid = _prefixed_id(id)
        idaapi.unregister_action(uid)

    @staticmethod
    def add_action_to_menu(id, menu_path):
        uid = _prefixed_id(id)
        idaapi.attach_action_to_menu(menu_path, uid, idaapi.SETMENU_APP)


def _prefixed_id(id):
    return ID_PREFIX + id


class _ActionHandler(idaapi.action_handler_t):
    def __init__(self, id, callback):
        idaapi.action_handler_t.__init__(self)
        self.callback = callback
        self.id = id

    def activate(self, ctx):
        return self.callback()

    def update(self, ctx):
        return idaapi.AST_ENABLE_ALWAYS
