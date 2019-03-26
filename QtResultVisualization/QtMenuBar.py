from PyQt5.QtWidgets import QMenu, QMenuBar, QAction

from ResultVisualization.Action import Action
from ResultVisualization.MenuBar import Menu, MenuBar


class QtMenu(Menu):

    def __init__(self, title: str):
        super().__init__(title)
        self.__qMenu = QMenu(title)

    def getQMenu(self) -> QMenu:
        return self.__qMenu

    def _addMenuToView(self, menu: Menu) -> None:
        self.__qMenu.addMenu(menu.getQMenu())

    def _addActionInView(self, action: Action):
        menuAction: QAction = QAction(action.text, self.__qMenu)
        menuAction.triggered.connect(action.trigger)
        self.__qMenu.addAction(menuAction)


class QtMenuBar(MenuBar):

    def __init__(self):
        super().__init__()
        self.__qMenuBar = QMenuBar()

    def _addMenuToView(self, menu: Menu) -> None:
        self.__qMenuBar.addMenu(menu.getQMenu())

    def getQMenuBar(self) -> QMenuBar:
        return self.__qMenuBar
