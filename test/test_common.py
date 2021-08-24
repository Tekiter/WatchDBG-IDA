from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest
from utils import import_src

common = import_src('WatchDbg.common')


class EventHandlerTest(unittest.TestCase):
    def testAttachAndNotify(self):
        handler = common.EventHandler()

        ref = {"notified": False}

        def dummy_handler(e):
            ref["notified"] = True

        handler.attach(dummy_handler)

        handler.notify()

        self.assertEqual(ref["notified"], True)
