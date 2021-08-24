# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from WatchDbg.core.types import WInt, parseType
from WatchDbg.core.watch import WatchList
from WatchDbg.ui.model import WatchModel
from WatchDbg.ui.view import WatchView
from WatchDbg.util import (PLUGIN_VERSION, debugline, set_debug_flag_getter,
                           writeline)


class WatchDbgPlugin:

    def __init__(self, flags, ida_api):
        self.flags = flags
        self.ida = ida_api

        set_debug_flag_getter(lambda: flags['debug'])

    def on_init(self):

        self.service = WatchService(ida_api=self.ida)

        self.register_shortcut_and_menu()
        self.register_debug_hook()

        writeline("Successfully loaded! [v.%s]" %
                  '.'.join(map(str, PLUGIN_VERSION)))

    def on_term(self):
        self.cleanup_shortcut_and_menu()
        self.cleanup_debug_hook()

    def register_shortcut_and_menu(self):
        self.ida.Action.register_action(
            "add_watch", "Add Watch", lambda: self.service.show_add_watch(None), "Shift-A")
        self.ida.Action.register_action(
            "show_watch_view", "Show WatchDbg List", lambda: self.service.show_watch(), "Shift-W")
        self.ida.Action.add_action_to_menu(
            "show_watch_view", "Debugger/WatchDbg")

    def register_debug_hook(self):
        self.ida.Debug.set_hook_on_process_pause(
            lambda: self.service.update_model())

    def cleanup_shortcut_and_menu(self):
        self.ida.Action.unregister_action("add_watch")
        self.ida.Action.unregister_action("show_watch_view")

    def cleanup_debug_hook(self):
        self.ida.Debug.remove_all_hooks()


class WatchService:
    def __init__(self, ida_api):
        self.ida = ida_api
        self.watch = WatchList()
        self.view = None

    def show_watch(self):
        if self.view_is_showing():
            self.update_model()
            return
        else:
            self.set_new_model()
            self.show_new_view()

    def set_new_model(self):
        model = WatchModel(
            self.watch, mem_reader=MemoryReader(ida_api=self.ida))
        model.update()
        self.model = model
        return model

    def show_new_view(self):
        view = WatchView(form=self.ida.View.create_form(), model=self.model)
        view.on_add.attach(self.show_add_watch)
        view.on_change_name.attach(self.show_change_name)
        view.on_change_type.attach(self.show_change_type)
        view.on_remove_all.attach(self.remove_all)
        view.show()

        self.view = view

    def show_add_watch(self, e):
        name = self.ida.Modal.request_string("Target address")
        addr = self.ida.Misc.convert_string_to_address(name)
        if addr > 0:
            self.watch.add(addr, name, WInt())
            self.update_model()
            debugline("Watch %d added: 0x%X" % (len(self.watch), addr))

    def show_change_type(self, e):
        if not self.view.is_selected():
            return

        index = self.view.get_selected_index()
        if not self.view.get_selected_item().canchangetype:
            return

        inp = self.ida.Modal.request_string("New Type")
        if string_not_null_or_empty(inp):
            typ = parseType(inp)
            if typ == None:
                return

            debugline("change type to %s" % typ.typerepr())
            self.model.changeType(index, typ)
            self.update_model()

    def show_change_name(self, e):
        if not self.view.is_selected():
            return

        item = self.view.get_selected_item()

        inp = self.ida.Modal.request_string("New Name")
        if string_not_null_or_empty(inp):
            item.name = inp
            self.update_model()

    def remove_all(self, e):
        self.watch.clear()
        self.model = WatchModel(
            self.watch, mem_reader=MemoryReader(ida_api=self.ida))
        self.view.set_new_model(self.model)

    def update_model(self):
        if self.view_is_showing():
            self.model.update()

    def view_is_showing(self):
        return self.view and not self.view.isclosed


def string_not_null_or_empty(string):
    return string != None and string.rstrip() != ""


class MemoryReader:
    def __init__(self, ida_api):
        self.ida = ida_api

    def read(self, address, size):
        data = self.ida.Debug.read_memory(address, size)
        return data
