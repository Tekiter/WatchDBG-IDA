import idaapi


class Plugin:
    @staticmethod
    def create_plugin(app, comment="", help="", name="", hotkey=""):

        plugin = PluginBase(app)

        plugin.comment = comment
        plugin.help = help
        plugin.name = name
        plugin.hotkey = hotkey

        return plugin


def nop_function(*args, **kwargs):
    pass


class PluginBase(idaapi.plugin_t):
    flags = idaapi.PLUGIN_HIDE
    comment = ""
    help = ""
    wanted_name = "WatchDbg"
    wanted_hotkey = ""

    def __init__(self, app):
        idaapi.plugin_t.__init__(self)
        self._app = app

    def init(self):
        self._app.on_init()
        return idaapi.PLUGIN_KEEP

    def run(self, arg):
        if hasattr(self._app, 'on_run'):
            self._app.on_run()
        pass

    def term(self):
        self._app.on_term()
        pass
