from typing import List

from QtResultVisualization.QtTreeView import QtTreeView
from ResultVisualization.TreeItem import TreeItem


class TreeIndex:

    def __init__(self, parent=None, item: TreeItem = None, index: int = None):
        self.__parent: TreeIndex = parent
        self.__item: TreeItem = item
        self.__index: int = index

    def getParent(self):
        return self.__parent

    def getTreeItem(self) -> TreeItem:
        return self.__item

    def getIndex(self) -> int:
        return self.__index

    def isValid(self) -> bool:
        return self.__parent is not None and self.__index is not None


class TreeViewPresenter:

    def __init__(self, treeView: QtTreeView):
        self.__treeView = treeView
        self.__root: TreeItem = TreeItem()
        self.__children: List[TreeItem] = []

    def insertItem(self, index: TreeIndex):
        self.__treeView.insertItem(index)

    def deleteItem(self, index: TreeIndex):
        self.__treeView.deleteItem(index)
