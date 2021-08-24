from WatchDbg.common import EventHandler

NEXT_ID = 0


def get_next_id():
    global NEXT_ID
    ret = NEXT_ID
    NEXT_ID += 1
    return ret


class WatchListItem():
    nextid = 0

    def __init__(self, address, wtype):
        self.address = address
        self.type = wtype
        self.name = ""
        self._id = get_next_id()

    @property
    def id(self):
        return self._id


class WatchList:

    def __init__(self):
        self._watches = []
        self.on_change = EventHandler()

    def __iter__(self):
        return iter(self._watches)

    def __len__(self):
        return len(self._watches)

    def add(self, address, name, type):
        item = WatchListItem(address, type)
        item.name = name

        self._watches.append(item)
        self.on_change.notify()
        return item.id

    def clear(self):
        self._watches = []
        self.on_change.notify()

    def exists(self, address):
        i = self._indexByAddress(address)
        return i != None

    def delete(self, address):
        i = self._indexByAddress(address)
        if i != None:
            item = self._watches.pop(i)
            self.on_change.notify()
            return item
        return None

    def get(self, address):
        idx = self._indexByAddress(address)
        if idx != None:
            return self._watches[idx]
        return None

    def _indexByAddress(self, address):
        for idx, watch in enumerate(self._watches):
            if watch.address == address:
                return idx
        return None
