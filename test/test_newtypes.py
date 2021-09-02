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

    def test_to_str_invalid_size(self):
        signed = types.SignedInt(2)
        self.assertRaises(types.DataSizeNotMatchError,
                          lambda: signed.to_str(b'\x12\x34\x56'))

    def test_to_str(self):
        signed = types.SignedInt(2)
        self.assertEqual(signed.to_str(b'\x34\x12'), str(0x1234))
