from __future__ import absolute_import
from __future__ import division

import idaapi


class Misc(object):
    @staticmethod
    def convert_string_to_address(string):
        address = idaapi.str2ea(string)
        if address != idaapi.BADADDR:
            return address
        return 0
