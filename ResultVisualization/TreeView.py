from typing import List

from ResultVisualization.Filter import Filter


class TreeView(object):
    def __init__(self):
        super().__init__()
        self.__children: List = []
        self.__filteredChildren = []

    def addChild(self, viewTreeNode) -> None:
        self.__children.append(viewTreeNode)
        self._addToView(viewTreeNode)
        viewTreeNode.addTreeNodeChildren()

    def removeChildAt(self, index: int) -> None:
        self.__children.pop(index)
        self._removeFromView(index)

    def removeChild(self, child) -> None:
        index: int = self.__children.index(child)
        self.removeChildAt(index)

    def getChildren(self):
        return self.__children.copy()

    def filter(self, viewFilter: Filter) -> None:
        markedForRemove = []
        for child in self.__children:
            if not viewFilter.appliesTo(child):
                child.checked = False
                index = self.__children.index(child)
                markedForRemove.append(child)
                self.__filteredChildren.append(child)
                self._removeFromView(index)
            else:
                child.filter(viewFilter)

        for child in markedForRemove:
            self.__children.remove(child)

    def resetFilter(self) -> None:
        for child in self.__filteredChildren:
            self.__children.append(child)
            self._addToView(child)

        for child in self.__children:
            child.resetFilter()

    def _addToView(self, viewTreeNode) -> None:
        raise NotImplementedError()

    def _removeFromView(self, index: int) -> None:
        raise NotImplementedError()


