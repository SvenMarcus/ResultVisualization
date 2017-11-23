from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt, QVariant

from ResultVisualization.TreeNodes import TreeItem


class TreeModel(QAbstractItemModel):
    def __init__(self):
        super(TreeModel, self).__init__()
        self.__root: TreeItem = TreeItem()

    def insertItem(self, child: TreeItem, index: QModelIndex, pos: int) -> None:
        self.beginInsertRows(index, pos, pos)
        self.__getItem(index).insert(child, pos)
        self.endInsertRows()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if not parent.isValid():
            return self.__root.getChildCount()
        return self.__getItem(parent).getChildCount()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 1

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        treeItem: TreeItem = self.__getItem(parent)

        if row > treeItem.getChildCount():
            return QModelIndex()

        return self.createIndex(row, column, treeItem)

    def data(self, index: QModelIndex, role: int = ...):
        if role == Qt.DisplayRole and index.column() == 0:
            return self.__getItem(index).text

        return QVariant()

    def parent(self, child: QModelIndex) -> QModelIndex:
        item: TreeItem = self.__getItem(child)
        parentItem: TreeItem = item.parent

        if parentItem is None:
            return QModelIndex()

        self.createIndex(parentItem.getPosition(), 0, parentItem)

    def __getItem(self, index: QModelIndex) -> TreeItem:
        if not index.isValid():
            return self.__root

        return index.internalPointer()

