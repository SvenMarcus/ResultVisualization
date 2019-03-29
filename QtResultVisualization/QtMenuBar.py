from PyQt5.QtWidgets import QMenu, QMenuBar, QAction

from ResultVisualization.Action import Action
from ResultVisualization.MenuBar import Menu, MenuBar


class QtMenu(Menu):

    def __init__(self, title: str):
        super().__init__(title)
        self.__qMenu = QMenu(title)
        self.__actionQActionMap: dict = dict()

    def getQMenu(self) -> QMenu:
        return self.__qMenu

    def _addMenuToView(self, menu: Menu) -> None:
        self.__qMenu.addMenu(menu.getQMenu())

    def _addActionInView(self, action: Action):
        menuAction: QAction = QAction(action.text, self.__qMenu)
        menuAction.triggered.connect(action.trigger)
        self.__actionQActionMap[action] = menuAction
        self.__qMenu.addAction(menuAction)

    def _removeActionFromView(self, action) -> None:
        qAction: QAction = self.__actionQActionMap[action]
        self.__qMenu.removeAction(qAction)


class QtMenuBar(MenuBar):

    def __init__(self):
        super().__init__()
        self.__qMenuBar = QMenuBar()

    def getQMenuBar(self) -> QMenuBar:
        return self.__qMenuBar

    def _makeMenu(self, title: str) -> Menu:
        return QtMenu(title)

    def _addMenuToView(self, menu: Menu) -> None:
        self.__qMenuBar.addMenu(menu.getQMenu())

    def _removeMenuFromView(self, menu) -> None:
        pass