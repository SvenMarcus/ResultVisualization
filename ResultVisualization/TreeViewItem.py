from typing import List


class TreeViewItem:
    pass


class TreeViewItem:
    def __init__(self, text: str = None):
        self.__text = text
        self.__children: List[TreeViewItem] = []
        self.__parent = None

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str) -> None:
        self.__text = text

    @property
    def parent(self) -> TreeViewItem:
        return self.__parent

    @parent.setter
    def parent(self, parent: TreeViewItem) -> None:
        self.__parent = parent

    def getChildCount(self) -> int:
        return len(self.__children)

    def getPosition(self):
        if self.parent is None:
            return -1

        return self.parent.childPos(self)

    def getChild(self, pos: int) -> TreeViewItem:
        return self.__children[pos]

    def insert(self, child: TreeViewItem, pos: int) -> None:
        self.__children.insert(pos, child)
        child.parent = self

    def remove(self, pos: int) -> None:
        item: TreeViewItem = self.__children.pop(pos)
        item.parent = None

    def childPos(self, child: TreeViewItem) -> int:
        if self.__children.count(child) == 0:
            return -1
        return self.__children.index(child)
