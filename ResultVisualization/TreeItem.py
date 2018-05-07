from typing import Dict, List, Set


class TreeItem:

    def __init__(self, text: str = None, tag: str = None):
        self.__text = text
        self.__tag = tag

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text: str) -> None:
        self.__text = text

    @property
    def tag(self) -> str:
        return self.__tag

    @tag.setter
    def tag(self, tag: str) -> None:
        self.__tag = tag


class CategoryItem(TreeItem):

    def __init__(self, text: str = None, tag: str = None):
        super().__init__(text, tag)
        self.__children: List[TreeItem] = []

    def addChild(self, item: TreeItem) -> None:
        self.__children.append(item)

    def deleteChild(self, index: int) -> None:
        self.__children.pop(index)

    def getChild(self, index: int) -> TreeItem:
        return self.__children[index]


class ResultTreeItem(TreeItem):

    def __init__(self, text: str = None, tag: str = None):
        super().__init__(text, tag)
        self.__results: Dict[str, float] = {}

    @property
    def results(self) -> Dict[str, float]:
        return self.__results
