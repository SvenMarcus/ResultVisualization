from ResultVisualization.Event import Event
from ResultVisualization.TreeItem import TreeItem


class TreeIndex:
    pass


class TreeIndex:

    def __init__(self, parent: TreeIndex = None, index: int = 0):
        self.__index: int = index
        self.__parent: TreeIndex = parent

    def getParent(self) -> TreeIndex:
        return self.__parent

    def getRow(self) -> int:
        return self.__index


class TreeView:

    def __init__(self):
        self.itemChecked: Event = Event()

    def insertItem(self, item: TreeItem, index: TreeIndex, childPos: int) -> None:
        raise NotImplementedError("TreeView operation insertItem not implemented")

    def deleteItem(self, index: TreeIndex):
        raise NotImplementedError("TreeView operation deleteItem not implemented")
