from PyQt5.QtWidgets import QMainWindow, QTabWidget, QToolBar, QWidget, QMenuBar

from QtResultVisualization.QtGraphViewFactory import QtGraphViewFactory
from QtResultVisualization.QtMenuBar import QtMenuBar
from QtResultVisualization.QtToolbar import QtToolbar

from ResultVisualization.Events import Event, InvokableEvent
from ResultVisualization.GraphView import GraphView
from ResultVisualization.MainWindow import MainWindow


class CustomMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__onClose = InvokableEvent()

    def onClose(self) -> Event:
        return self.__onClose

    def closeEvent(self, a0):
        self.__onClose(self)
        return super().closeEvent(a0)


class QtMainWindow(MainWindow):

    def __init__(self, graphViewFactory: QtGraphViewFactory, toolBar: QtToolbar = None, menuBar: QtMenuBar = None):
        self.__window: QMainWindow = CustomMainWindow()
        if toolBar is not None:
            self.__toolbar: QToolBar = toolBar.getWidget()
            self.__window.addToolBar(self.__toolbar)

        if menuBar is not None:
            self.__menuBar: QMenuBar = menuBar.getQMenuBar()
            self.__window.setMenuBar(self.__menuBar)

        self.__widget: QTabWidget = QTabWidget()
        self.__widget.currentChanged.connect(lambda index: self._setActiveIndex(index))

        self.__window.setCentralWidget(self.__widget)
        self.__window.onClose().append(lambda x, y: self._onClose(self))

        super().__init__(graphViewFactory, toolBar, menuBar)

    def getWidget(self) -> QWidget:
        return self.__window

    def show(self) -> None:
        self.__window.show()

    def _appendGraphView(self, graphView: GraphView, title: str) -> None:
        self.__widget.addTab(graphView.getWidget(), title)

    def _setGraphViewTitleAt(self, title: str, index: int) -> None:
        self.__widget.setTabText(index, title)

    def _selectGraphViewAt(self, index):
        self.__widget.setCurrentIndex(index)

    def _removeGraphView(self, index: int):
        self.__widget.removeTab(index)
