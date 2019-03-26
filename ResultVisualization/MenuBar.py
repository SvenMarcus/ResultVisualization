from abc import ABC, abstractmethod
from typing import List

from ResultVisualization.Action import Action


class Menu(ABC):

    def __init__(self, title: str):
        self.__title: str = title
        self.__action: Action = None
        self.__children: List[Menu] = list()

    def addAction(self, action: Action) -> None:
        self.__action = action
        self._addActionInView(action)

    def addChild(self, menu: 'Menu') -> None:
        self.__children.append(menu)
        self._addMenuToView(menu)

    def getChildren(self) -> List['Menu']:
        return list(self.__children)

    @abstractmethod
    def _addMenuToView(self, menu) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _addActionInView(self, action: Action):
        raise NotImplementedError()


class MenuBar(ABC):

    def __init__(self):
        self.__menus = list()

    def addMenu(self, menu: Menu) -> None:
        self.__menus.append(menu)
        self._addMenuToView(menu)

    def getMenus(self) -> List[Menu]:
        return list(self.__menus)

    @abstractmethod
    def _addMenuToView(self, menu) -> None:
        raise NotImplementedError()
