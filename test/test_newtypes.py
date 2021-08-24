# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import unittest
from utils import import_src

types = import_src('WatchDbg.type.newtypes')


class SignedIntTest(unittest.TestCase):
    def test_name_is_valid(self):
        signed = types.SignedInt(1)
        self.assertEqual(signed.name, "Int8")

        signed = types.SignedInt(4)
        self.assertEqual(signed.name, "Int32")
