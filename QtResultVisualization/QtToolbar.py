from typing import Dict

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QToolBar, QWidget

from ResultVisualization.Action import Action
from ResultVisualization.Toolbar import Toolbar


class QtToolbar(Toolbar):

    def __init__(self, parent: QWidget = None):
        self.__widget: QToolBar = QToolBar(parent)
        self.__actionToQActionDict: Dict[Action, QAction] = dict()
        super().__init__()

    def getWidget(self) -> QWidget:
        return self.__widget

    def _addActionToView(self, action: Action) -> None:
        icon: QIcon = QIcon(action.icon)
        toolBarAction: QAction = QAction(icon, action.text, self.__widget)
        toolBarAction.triggered.connect(action.trigger)
        self.__actionToQActionDict[action] = toolBarAction
        self.__widget.addAction(toolBarAction)

    def _removeActionFromView(self, action):
        actionToRemove: QAction = self.__actionToQActionDict[action]
        self.__widget.removeAction(actionToRemove)

    def _clearActionsInView(self) -> None:
        self.__widget.clear()
