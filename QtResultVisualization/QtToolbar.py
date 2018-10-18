from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QToolBar, QWidget

from ResultVisualization.Action import Action
from ResultVisualization.Toolbar import Toolbar


class QtToolbar(Toolbar):

    def __init__(self, parent: QWidget = None):
        self.__widget: QToolBar = QToolBar(parent)
        super().__init__()

    def getWidget(self) -> QWidget:
        return self.__widget

    def _addActionToView(self, action: Action) -> None:
        print("Adding action", action.text, "to toolbar")
        icon: QIcon = QIcon(action.icon)
        toolBarAction: QAction = QAction(icon, action.text)
        toolBarAction.triggered.connect(action.trigger)
        self.__widget.addAction(toolBarAction)

    def _clearActionsInView(self) -> None:
        print("Clearing actions")
        self.__widget.clear()
