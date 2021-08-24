from __future__ import absolute_import
from __future__ import division
from WatchDbg.common import EventHandler

import idaapi


def nop_function(*args, **kwargs): pass


class View:
    @staticmethod
    def create_form():

        on_create = EventHandler()
        on_close = EventHandler()

        class PluginViewInner(idaapi.PluginForm):

            def __init__(self):
                idaapi.PluginForm.__init__(self)

            def OnCreate(self, form):
                self.widget = self.FormToPyQtWidget(form)
                on_create.notify(self.widget)

            def OnClose(self, form):
                on_close.notify()

        view = PluginViewInner()

        class PluginView(object):
            def __init__(self):
                self.title = ''
                self.on_create = on_create
                self.on_close = on_close

            def show(self):
                view.Show(self.title)

        return PluginView()
