from typing import Any

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

    def deleteIndex(self, parent: QModelIndex, pos: int) -> None:
        self.beginRemoveRows(parent, pos, pos)
        self.__getItem(parent).remove(pos)
        self.endRemoveRows()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if parent.column() > 0:
            return 0

        return self.__getItem(parent).getChildCount()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 1

    def data(self, index: QModelIndex, role: int = ...) -> QVariant:
        if index.column() != 0:
            return QVariant()

        item = self.__getItem(index)
        if role == Qt.DisplayRole:
            return QVariant(item.text)
        elif role == Qt.CheckStateRole:
            return QVariant(self.__getCheckState(item))

        return QVariant()

    def __getCheckState(self, item: TreeViewItem) -> Qt.CheckState:
        if item.checked:
            return Qt.Checked
        else:
            return Qt.Unchecked

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        defaultFlags = QAbstractItemModel.flags(self, index)
        if index.isValid() and index.column() == 0:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | defaultFlags
        return defaultFlags

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

    def setData(self, index: QModelIndex, value: Any, role: int = ...) -> bool:
        if not index.isValid():
            return False

        if role == Qt.CheckStateRole:
            self.__getItem(index).checked = self.__getBoolFromCheckState(value)
            self.dataChanged.emit(QModelIndex(), index)
            return True
        
        return super(TreeModel, self).setData(index, value)

    def __getBoolFromCheckState(self, value) -> bool:
        if value == Qt.Checked:
            return True
        else:
            return False

    def __getItem(self, index: QModelIndex) -> TreeViewItem:
        if not index.isValid():
            return self.__root

        return index.internalPointer()
