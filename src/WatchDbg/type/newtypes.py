# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import struct

# 타입 클래스의 역할
# - 타입에 적합한 데이터 사이즈 저장
# - 바이너리 데이터를 입력받으면 출력 가능한 형태로 변환


class DataSizeNotMatchError(Exception):
    pass


class WatchType(object):

    @property
    def size(self):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

    def to_str(self, binary_data):
        raise NotImplementedError()

    def _fit_check(self, binary_data):
        if len(binary_data) != self.size:
            raise DataSizeNotMatchError()


class AtomType(WatchType):
    pass


class SequenceType(WatchType):
    @property
    def length(self):
        raise NotImplementedError()


class FloatingPointType(WatchType):
    pass


class SignedInt(AtomType):
    def __init__(self, size):
        super(SignedInt, self).__init__()
        self._size = size

    @property
    def name(self):
        return "Int{}".format(self.size * 8)

    @property
    def size(self):
        return self._size

    def to_str(self, binary_data):
        self._fit_check(binary_data)
        intval = int.from_bytes(binary_data, "little", signed=True)
        return str(intval)


class UnsignedInt(AtomType):
    def __init__(self, size):
        super(UnsignedInt, self).__init__()
        self._size = size

    @property
    def name(self):
        return "UInt{}".format(self.size * 8)

    @property
    def size(self):
        return self._size

    def to_str(self, binary_data):
        self._fit_check(binary_data)
        intval = int.from_bytes(binary_data, "little", signed=False)
        return str(intval)


class Float(FloatingPointType):
    def __init__(self):
        super(Float, self).__init__()

    @property
    def name(self):
        return "Float"

    @property
    def size(self):
        return 4

    def to_str(self, binary_data):
        self._fit_check(binary_data)
        return struct.unpack("<f", binary_data)[0]


class Double(FloatingPointType):
    def __init__(self):
        super(Double, self).__init__()

    @property
    def name(self):
        return "Double"

    @property
    def size(self):
        return 8

    def to_str(self, binary_data):
        self._fit_check(binary_data)
        return struct.unpack("<d", binary_data)[0]


class Array(SequenceType):
    def __init__(self, element_type, length):
        super(Array, self).__init__()
        self._element_type = element_type
        self._length = length

    @property
    def name(self):
        return "Array<{}>".format(self._element_type.name)

    @property
    def size(self):
        return self._element_type.size * self._length

    @property
    def length(self):
        return self._length

    @property
    def element_type(self):
        return self._element_type

    def to_str(self, binary_data):
        self._fit_check(binary_data)
        return "Array(length={})".format(self._length)


class String(Array):
    def __init__(self, length):
        super(String, self).__init__(SignedInt(1), length)

    @property
    def name(self):
        return "String"

    @property
    def size(self):
        return self._length

    def to_str(self, binary_data):
        self._fit_check(binary_data)
        return repr(binary_data)
