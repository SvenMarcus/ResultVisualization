from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt, QVariant

from ResultVisualization.TreeViewItem import TreeViewItem


class TreeModel(QAbstractItemModel):
    def __init__(self):
        super().__init__()
        self.__root: TreeViewItem = TreeViewItem()

    def insertItem(self, child: TreeViewItem, index: QModelIndex, pos: int) -> None:
        self.beginInsertRows(index, pos, pos)
        self.__getItem(index).insert(child, pos)
        self.endInsertRows()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if parent.column() > 0:
            return 0

        return self.__getItem(parent).getChildCount()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 1

    def data(self, index: QModelIndex, role: int = ...) -> QVariant:
        if role == Qt.DisplayRole and index.column() == 0:
            return QVariant(self.__getItem(index).text)

        return QVariant()

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        childItem: TreeViewItem = self.__getItem(parent).getChild(row)

        if childItem is None:
            return QModelIndex()

        return self.createIndex(row, column, childItem)

    def parent(self, childIndex: QModelIndex) -> QModelIndex:
        parentItem: TreeViewItem = self.__getItem(childIndex).parent

        if parentItem is self.__root or parentItem is None:
            return QModelIndex()

        return self.createIndex(parentItem.getPosition(), 0, parentItem)

    def __getItem(self, index: QModelIndex) -> TreeViewItem:
        if not index.isValid():
            return self.__root

        return index.internalPointer()
