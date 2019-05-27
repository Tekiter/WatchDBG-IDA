
class WatchModel(QStandardItemModel):
    columns = {"name":0, "address":1, "value":2, "type":3}
    
    def __init__(self, watch):
        QStandardItemModel.__init__(self)
        self.watch = watch
        self.viewitems = {}
        self.maxdepth = 5

        self.createHeader()


    def refresh(self):
               

        for i in self.watch._watches:
            self.appendItem(i)

    def createHeader(self):
        self.setColumnCount(4)
        self.setHeaderData(self.columns['address'], Qt.Horizontal, "Address")
        self.setHeaderData(self.columns['name'], Qt.Horizontal, "Name")
        self.setHeaderData(self.columns['value'], Qt.Horizontal, "Value")
        self.setHeaderData(self.columns['type'], Qt.Horizontal, "Type")

    def appendItem(self, watchitem):
        val = watchitem.value()

        row = [0 for _ in range(len(self.columns))]
        row[self.columns["name"]] = QStandardItem(watchitem.name())
        row[self.columns["address"]] = QStandardItem(hex(watchitem.address()))
        row[self.columns["value"]] = QStandardItem(str(val))
        row[self.columns["type"]] = QStandardItem(val.typerepr())
        self.appendRow(row)
        return row
        

class WatchWrapper():
    def __init__(self, watchitem=WatchItem(0), rowindex=0, parent=None):
        self._watchitem = watchitem
        self._parent = parent
        self._rowindex = rowindex

    def __repr__(self):
        return "0x%x : %s" % (self._watchitem.address(), self._watchitem.value())

    def address(self):
        return self._watchitem.address()

    def parent(self):
        return self._parent

    def children(self):
        signiture = self._watchitem.typeSigniture()
        if signiture == "raw" or signiture == "int":
            return None
        return None

    def rowindex(self):
        return self._rowindex

    def rowcount(self):
        return 1
    

    
class WatchViewerModel(QAbstractItemModel):
    columns = {"name":0, "address":1, "value":2, "type":3}

    def __init__(self, watcher, parent=None):
        QAbstractItemModel.__init__(self, parent)
        self._items = []
        self._watcher = watcher

    def update(self):
        self._items = [WatchWrapper(x) for x in self._watcher._watches]
        debugline(self._items)
        self.dataChanged.emit(QModelIndex(), QModelIndex())


    def rowCount(self, parent):
        if parent.column() > 0:
            debugline("col: %d" % parent.column())
            debugline("row: 0 (ff)")
            return 0

        debugline("prow: %d, pcol: %d" %(parent.row(), parent.column()))
        if not parent.isValid():
            debugline("row: %d (notvalid parent)" % len(self._items))
            return len(self._items)

        item = parent.internalPointer()

        debugline("row: %d" % item.rowcount())
        return item.rowcount()


    def columnCount(self, parent):
        return len(self.columns)

    def data(self, index):
        debugline("data(%d, %d)" %(index.row(), index.column()))
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.InternalPointer()
        col = index.column()
        
        if col == self.columns["name"]:
            return str(item.name())
        elif col == self.columns["address"]:
            return str(item.address())
        elif col == self.columns["value"]:
            return str(item.value())
        elif col == self.columns["type"]:
            return str(item.typestr())
        else:
            return "<ERROR>"

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columns.keys()[self.columns.values().index(section)]

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            return QModelIndex()

        debugline("%s %s : %s" %(str(row), str(column), str(self._items[row].address())))
        if not parent.isValid():
            
            return self.createIndex(row, column, self._items[row])


        pitem = parent.internalPointer()

        items = pitem.children()
        
        if items:
            return self.createIndex(row, column, items[row])
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        item = index.internalPointer()
        parent = item.parent()

        if parent:
            return self.createIndex(parent.rowindex(), 0, parent)
        return QModelIndex()

    