from abc import ABC, abstractmethod
from typing import List, Set

from ResultVisualization.Action import Action


class Menu(ABC):

    def __init__(self, title: str):
        self.__title: str = title
        self.__actions: Set[Action] = set()
        self.__children: List[Menu] = list()

    def addAction(self, action: Action) -> None:
        self.__actions.add(action)
        self._addActionInView(action)

    def removeAction(self, action: Action) -> bool:
        if action not in self.__actions:
            return False

        self.__actions.remove(action)
        self._removeActionFromView(action)
        return True

    def addChild(self, menu: 'Menu') -> None:
        self.__children.append(menu)
        self._addMenuToView(menu)

    def getChildren(self) -> List['Menu']:
        return list(self.__children)

    def getTitle(self) -> str:
        return self.__title

    @abstractmethod
    def _addMenuToView(self, menu) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _addActionInView(self, action: Action) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _removeActionFromView(self, action) -> None:
        raise NotImplementedError()


class MenuBar(ABC):

    def __init__(self):
        self.__menus = list()

    def addMenu(self, menu: Menu) -> None:
        self.__menus.append(menu)
        self._addMenuToView(menu)

    def addAction(self, action: Action) -> None:
        added = self.__addToMatchingMenu(action, self.__menus)
        if not added:
            menu = self._makeMenu(action.parentMenu)
            menu.addAction(action)
            self.addMenu(menu)

    def removeAction(self, action: Action) -> None:
        menus = self.__menus
        self.__removeActionFromMenu(action, menus)

    def __removeActionFromMenu(self, action, menus) -> bool:
        removed: bool = False
        for menu in menus:
            if menu.getTitle() == action.parentMenu:
                removed = menu.removeAction(action)
                if removed:
                    break

            removed = self.__removeActionFromMenu(action, menu.getChildren())
            if removed:
                break

        return removed

    def __addToMatchingMenu(self, action, menus) -> bool:
        for menu in menus:
            if menu.getTitle() == action.parentMenu:
                menu.addAction(action)
                return True

            added = self.__addToMatchingMenu(action, menu.getChildren())
            if added:
                return True

        return False

    def getMenus(self) -> List[Menu]:
        return list(self.__menus)

    @abstractmethod
    def _addMenuToView(self, menu) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _removeMenuFromView(self, menu) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _makeMenu(self, title: str) -> Menu:
        raise NotImplementedError()
