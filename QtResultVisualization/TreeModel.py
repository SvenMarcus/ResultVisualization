from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt, QVariant

from ResultVisualization.TreeNodes import TreeItem


class TreeModel(QAbstractItemModel):
    def __init__(self):
        super().__init__()
        self.__root: TreeItem = TreeItem()

    def insertItem(self, child: TreeItem, index: QModelIndex, pos: int) -> None:
        self.beginInsertRows(index, pos, pos)
        self.__getItem(index).insert(child, pos)
        self.endInsertRows()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if parent.column() > 0:
            return 0

        item = None
        if not parent.isValid():
            item = self.__root
        else:
            item = parent.internalPointer()

        return item.getChildCount()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 1

    def index(self, row, column, parent: QModelIndex = ...) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        parent_item = None
        if not parent.isValid():
            parent_item = self.__root
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.getChild(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def data(self, index: QModelIndex, role: int = ...):
        if role == Qt.DisplayRole and index.column() == 0:
            return self.__getItem(index).text

        return QVariant()

    def parent(self, childindex):

        if not childindex.isValid():
            return QModelIndex()

        child_item = childindex.internalPointer()
        if not child_item:
            return QModelIndex()

        parent_item = child_item.parent

        if parent_item == self.__root:
            return QModelIndex()

        return self.createIndex(parent_item.getPosition(), 0, parent_item)

    def __getItem(self, index: QModelIndex) -> TreeItem:
        if not index.isValid():
            return self.__root

        return index.internalPointer()

