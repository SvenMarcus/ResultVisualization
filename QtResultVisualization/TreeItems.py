from typing import List


# class TreeItem:
#     pass

class TreeItem:

    def __init__(self, text: str = None):
        self.__text = text
        self.__children: List = []
        self.__parent = None

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, parent) -> None:
        self.__parent = parent

    def getChildCount(self) -> int:
        return len(self.__children)

    def getRow(self) -> int:
        if self.parent is None:
            return -1

        return self.parent.childPos(self)

    def childPos(self, child) -> int:
        if child not in self.__children:
            return -1

        return self.__children.index(child)

    def insertChild(self, child, pos: int) -> None:
        self.__children.insert(pos, child)
        child.parent = self

    def removeChild(self, pos: int) -> None:
        if pos > len(self.__children) - 1:
            return

        item: TreeItem = self.__children.pop(pos)
        item.parent = None
