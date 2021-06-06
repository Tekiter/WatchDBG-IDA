from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest
from utils import import_src

types = import_src('WatchDbg.types').types


class WTypeSizeTest(unittest.TestCase):
    def testSize(self):
        for size in range(1, 33):
            wtype = types.WType(size=size)
            self.assertTrue(wtype.size == size)
            self.assertEqual(wtype.rawvalue, b'\x00' * size)

    def testFromRawOfFitSize(self):
        wtype = types.WType(size=4)

        wtype.fromraw(b'\x01\x02\x03\x04')
        self.assertEqual(wtype.rawvalue, b'\x01\x02\x03\x04')

    def testFromRawOfLargerSize(self):
        wtype = types.WType(size=4)

        wtype.fromraw(b'\x01\x02\x03\x04\x05\x06')
        self.assertEqual(wtype.rawvalue, b'\x01\x02\x03\x04')

    def testFromRawOfSmallerSize(self):
        wtype = types.WType(size=4)

        wtype.fromraw(b'\x01\x02')
        self.assertEqual(wtype.rawvalue, b'\x01\x02\x00\x00')


if __name__ == '__main__':
    unittest.main()
