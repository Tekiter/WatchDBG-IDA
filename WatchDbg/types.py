import binascii
import string

WORD_SIZE = 8

def setGlobalWordSize(size):
    global WORD_SIZE
    WORD_SIZE = size

def getGlobalWordSize(size):
    global WORD_SIZE
    return WORD_SIZE


typeconverttable = {"byte":"uint8","short":"int16","long":"int64","ushort":"uint16","ulong":"uint64",
                    "word":"int16", "dword":"int32", "qword":"int64"}
def parseType(typestr):
    if not isinstance(typestr, str):
        return None
    typestr = typestr.lower()

    for k,v in typeconverttable.items():
        type = typestr.replace(k,v)

    spstr = typestr.split()
    if len(spstr) > 1:
        childtype = parseType(' '.join(spstr[:-1]))
        if childtype == None:
            return None
        try:
            count = int(spstr[-1])
        except ValueError:
            return None
        
        return WArray(count, childtype)


    if typestr == "raw":
        return WType()
    if typestr == "ptr" or typestr == "pointer":
        return WPtr()
    if typestr == "char":
        return WChar()
    if typestr == "str" or typestr == "string":
        return WString()

    signed = True
    if typestr.startswith("uint"):
        typestr = typestr[1:]
        signed = False
    if typestr.startswith("int"):
        if len(typestr) == 3:
            return WInt(4, signed)
        try:
            size = int(typestr[3:])
        except ValueError:
            return None
        
        return WInt(size//8, signed)
    return None


class WType():

    def __init__(self, size=WORD_SIZE):
        self.size = size
        self.rawvalue = b"".ljust(self.size, b'\x00')

    def __repr__(self):
        dat = self.hexstring()
        return "%s" % (dat)

    def fromhex(self, string):
        if string.startswith('0x'):
            string=string[2:]

        hx = binascii.unhexlify(string)
        if len(hx) > self.size:
            hx=hx[:self.size]
        else:
            hx = hx.ljust(self.size, b'\x00')

        self.rawvalue = hx
        

    def fromraw(self, data):
        if len(data) > self.size:
            self.fromraw = data[:self.size]
        else:
            self.rawvalue = data.ljust(self.size, b'\x00')

    
    def value(self):
        return self.rawvalue

    def hexstring(self):
        dat = binascii.hexlify(self.rawvalue)
        if bytes != str:
            dat = dat.decode()
        return dat

    def raw(self):
        return self.rawvalue

    def typeequals(self, typ):
        return isinstance(self, typ)

    def typerepr(self):
        return "Raw (size: %d)" % self.size
    

    
    
   


class WInt(WType):

    def __init__(self, size=4, signed=True):
        WType.__init__(self, size)
        self.signed = signed

    def __repr__(self):
        return "%-30d(0x%X)" % (self.int(), self.int(False))

    def fromint(self, value):
        hx=""
        
        if value < 0:
            c = self.maxval() + value + 1
        else:
            c = value

        while c != 0:
            hx += chr(c & 0xff)
            c >>= 8

        self.fromraw(hx)

    def int(self, signed=None):
        if signed==None:
            signed = self.signed

        val = 0
        c = 0
        for i in self.rawvalue:
            val += ord(i) << (c * 8)
            c+=1
        msb = 1 << (self.size * 8 - 1)
        if signed:
            if (val & msb) != 0:
                val = -(self.maxval() - val) - 1

        return val

    def maxval(self):
        o=0
        for i in range(self.size):
            o += 0xff << (i * 8)
        return o

    def typerepr(self):
        o = "Int%d" % (self.size * 8)
        if not self.signed:
            o = "U" + o
        return o


class WChar(WInt):
    def __init__(self):
        WInt.__init__(self, 1, False)

    def __repr__(self):
        return "'%s'\t(0x%X)" % (self.char(), self.int())

    def char(self):
        if self.int() >= 0x20 and self.int() <= 0x7e:
            return chr(self.int())
        else:
            return "\\x%02X" % self.int()

    def typerepr(self):
        return "Char"


class WPtr(WInt):

    def __init__(self):
        WInt.__init__(self, WORD_SIZE, False)
        
    
    def __repr__(self):
        return "0x%X" % (self.address())

    def address(self):
        return self.int(False)

    def typerepr(self):
        return "Pointer"




class WArray(WType):

    def __init__(self, elementcount = 1, elementtype = WType()):
        WType.__init__(self, elementtype.size * elementcount)
        self._elementcount = elementcount
        self._elementtype = elementtype
        #self.size = elementtype.size * elementcount

    def __repr__(self):
        
        return "%s Array [%d] (size: %d)" % (self.elementtype().typerepr(), self.elementcount(), self.size)
        


    def elementcount(self):
        return self._elementcount

    def elementtype(self):
        return self._elementtype

    def elementsize(self):
        return self._elementtype.size

    def setelementtype(self, newtype):
        self._elementtype = newtype
        self.size = newtype.size * self.elementcount()

    def calcindex(self, index):
        return self.elementsize() * index

    def typerepr(self):
        return "Array"



class WStruct(WType):
    pass
    

class WString(WArray):
    def __init__(self, bufsize = 100):
        WArray.__init__(self, bufsize, WChar())
    
    def __repr__(self):
        
        o=self.raw()
        
        return o

    def typerepr(self):
        return "String"



