from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest
from utils import import_src

types = import_src('WatchDbg.core.types').core.types


class WTypeTest(unittest.TestCase):
    def testSize(self):
        for size in range(1, 33):
            wtype = types.WType(size=size)
            self.assertTrue(wtype.size == size)
            self.assertEqual(wtype.raw(), b'\x00' * size)

    def testFromRawOfFitSize(self):
        wtype = types.WType(size=4)

        wtype.fromraw(b'\x01\x02\x03\x04')
        self.assertEqual(wtype.raw(), b'\x01\x02\x03\x04')

    def testFromRawOfLargerSize(self):
        wtype = types.WType(size=4)

        wtype.fromraw(b'\x01\x02\x03\x04\x05\x06')

        self.assertEqual(wtype.raw(), b'\x01\x02\x03\x04')

    def testFromRawOfSmallerSize(self):
        wtype = types.WType(size=4)

        wtype.fromraw(b'\x01\x02')
        self.assertEqual(wtype.raw(), b'\x01\x02\x00\x00')

    def testString(self):
        wtype = types.WType(size=4)

        wtype.fromraw(b'\x01\x02\x03\x04')
        self.assertEqual(wtype.__repr__(), '01020304')


class WIntTest(unittest.TestCase):
    def testMaxValue(self):
        wint = types.WInt(size=1)
        self.assertEqual(wint.maxval(), 255)

        wint = types.WInt(size=2)
        self.assertEqual(wint.maxval(), 65535)

        wint = types.WInt(size=4)
        self.assertEqual(wint.maxval(), 4294967295)

    def testToIntUnsigned(self):
        wint = types.WInt(size=4)
        wint.fromraw(b'\x78\x56\x34\x12')

        self.assertEqual(wint.int(signed=False), 0x12345678)

    def testToIntSigned(self):
        wint = types.WInt(size=4)
        wint.fromraw(b'\xfd\xff\xff\xff')
        self.assertEqual(wint.int(signed=True), -3)

        wint = types.WInt(size=4)
        wint.fromraw(b'\xfd\x00\x00\x00')
        self.assertEqual(wint.int(signed=True), 0xfd)

        wint = types.WInt(size=1)
        wint.fromraw(b'\xfe')
        self.assertEqual(wint.int(signed=True), -2)

        wint = types.WInt(size=1)
        wint.fromraw(b'\x1c')
        self.assertEqual(wint.int(signed=True), 0x1c)

    def testFromInt(self):
        self.allTestFromInt([
            [2, 0, b'\x00\x00'],
            [2, 0x13, b'\x13\x00'],
            [2, -2, b'\xfe\xff'],
        ])

    def allTestFromInt(self, data):
        for size, fromint, tohex in data:
            wint = types.WInt(size=size)
            wint.fromint(fromint)
            self.assertEqual(wint.raw(), tohex)


class WCharTest(unittest.TestCase):
    def testChar(self):
        wchar = types.WChar()
        wchar.fromraw('\x41')
        self.assertEqual(wchar.char(), 'A')


if __name__ == '__main__':
    unittest.main()
