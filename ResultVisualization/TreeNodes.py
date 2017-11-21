from typing import List


class TreeItem:
    pass


class TreeItem:
    def __init__(self, text: str = None):
        self.__text = text
        self.__children: List[TreeItem] = []
        self.__parent = None

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str) -> None:
        self.__text = text

    @property
    def parent(self) -> TreeItem:
        return self.__parent

    @parent.setter
    def parent(self, parent: TreeItem) -> None:
        self.__parent = parent

    def getChildCount(self) -> int:
        return len(self.__children)

    def getPosition(self):
        if self.parent is None:
            return -1

        return self.parent.childPos(self)

    def getChild(self, pos: int) -> TreeItem:
        return self.__children[pos]

    def insert(self, child: TreeItem, pos: int) -> None:
        self.__children.insert(pos, child)
        child.parent = self

    def remove(self, pos: int) -> None:
        item: TreeItem = self.__children.pop(pos)
        item.parent = None

    def __childPos(self, child: TreeItem) -> int:
        if self.__children.count(child) == 0:
            return -1
        return self.__children.index(child)
