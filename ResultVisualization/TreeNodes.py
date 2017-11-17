from typing import List


class TreeNode(object):
    def __init__(self, text: str):
        self.__text = text

    def get_text(self) -> str:
        return self.__text

    def set_text(self, text) -> None:
        self.__text = text

    def __str__(self):
        return self.__text

    def __repr__(self):
        return self.__text


class CategoryNode(TreeNode):

    def __init__(self, text):
        super().__init__(text)
        self.__children: List[TreeNode] = []

    def add_child(self, child: TreeNode) -> None:
        self.__children.append(child)

    def remove_child(self, child: TreeNode) -> None:
        self.__children.remove(child)

    def get_children(self) -> List[TreeNode]:
        return self.__children.copy()


class FloatNode(TreeNode):

    def __init__(self, text: str, value: float):
        super().__init__(text)
        self.__value = value

    def get_value(self) -> float:
        return self.__value

    def set_value(self, value: float) -> None:
        self.__value = value