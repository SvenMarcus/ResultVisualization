from typing import List

from ResultVisualization.Event import Event
from ResultVisualization.TreeItem import CategoryItem, TreeItem
from ResultVisualization.TreeView import TreeView, TreeIndex


class NonCategoryItemInPathError(Exception):

    def __init__(self):
        super().__init__()


class TreeViewController:

    def __init__(self, treeView: TreeView):
        self.itemChecked = Event()
        self.__treeView = treeView
        self.__treeView.itemChecked.append(self.__onItemChecked)
        self.__root: CategoryItem = CategoryItem()

    def insertItem(self, item: TreeItem, parentIndex: TreeIndex) -> None:
        parentItem: CategoryItem = self.__getParentItem(parentIndex)
        parentItem.addChild(item)
        self.__treeView.insertItem(item, parentIndex, parentIndex.getRow())

    def deleteItem(self, index: TreeIndex) -> None:
        self.__treeView.deleteItem(index)
        parentItem: CategoryItem = self.__getParentItem(index)
        parentItem.deleteChild(index.getRow())

    @staticmethod
    def __createPath(index: TreeIndex):
        path: List[TreeIndex] = []
        parent: TreeIndex = index.getParent()
        while parent is not None:
            path.insert(0, parent)
            parent = parent.getParent()
        return path

    def __getParentItem(self, index: TreeIndex):
        path = self.__createPath(index)
        currentItem: CategoryItem = self.__root
        for treeIndex in path:
            if type(currentItem) is not CategoryItem:
                raise NonCategoryItemInPathError()
            currentItem = currentItem.getChild(treeIndex.getRow())
        return currentItem

    def __onItemChecked(self, sender, args):
        print(self)
        print(sender)
        print(args)
