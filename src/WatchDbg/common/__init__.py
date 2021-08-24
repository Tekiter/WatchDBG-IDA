from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class EventHandler:
    def __init__(self):
        self._handlers = []

    def attach(self, handler):
        self._handlers.append(handler)

    def detach(self, handler):
        try:
            handler_index = self._handlers.index(handler)
            self._handlers.pop(handler_index)
        except ValueError:
            pass

    def notify(self, event_arg=None):
        for handler in self._handlers:
            handler(event_arg)
