from WatchDbg.common import EventHandler
from WatchDbg.core.types import *
from WatchDbg.util import debugline


class WatchItem():
    nextid = 0

    def __init__(self, address, wtype=WType()):
        self._address = address
        self._type = wtype
        self._name = ""
        self._valid = False
        self._id = WatchItem.nextid
        WatchItem.nextid += 1

    def id(self):
        return self._id

    def address(self):
        return self._address

    def setType(self, typ):
        backup = typ.raw()
        typ.fromraw(backup)

        self._type = typ

    def type(self):
        return self._type

    def setName(self, name):
        self._name = name

    def name(self):
        return self._name

    def typeStr(self):
        return self._type.typerepr()


class Watcher:

    def __init__(self):
        self._watches = []
        self.on_update = EventHandler()

    def add(self, address, name=''):
        item = WatchItem(address, WInt())
        item.setName(name)

        self._watches.append(item)
        self.on_update.notify()
        return item.id()

    def clear(self):
        self._watches = []
        self.on_update.notify()

    def exists(self, address):
        i = self._indexByAddress(address)
        return i != None

    def delete(self, address):
        i = self._indexByAddress(address)
        if i != None:
            self._watches.pop(i)
            self.on_update.notify()
            return True
        return False

    def getList(self):
        return [i for i in self._watches]

    def watches(self):
        return iter(self._watches)

    def count(self):
        return len(self._watches)

    def _indexByAddress(self, address):
        for i in range(len(self._watches)):
            if self._watches[i].address() == address:
                return i
        return None

    def indexById(self, id):
        for i in range(len(self._watches)):
            if self._watches[i].id() == id:
                return i
        return None

    def removeById(self, id):
        idx = self.indexById(id)
        debugline(idx)
        if idx != None:
            self._watches.pop(idx)
            self.on_update.notify()
            debugline("Remove")
