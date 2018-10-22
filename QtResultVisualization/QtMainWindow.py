from PyQt5.QtWidgets import QMainWindow, QTabWidget, QToolBar, QWidget

from QtResultVisualization.QtGraphViewFactory import QtGraphViewFactory
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

    def __init__(self, toolbar: QtToolbar, graphViewFactory: QtGraphViewFactory):
        self.__window: QMainWindow = CustomMainWindow()
        self.__toolbar: QToolBar = toolbar.getWidget()

        self.__window.addToolBar(self.__toolbar)

        self.__widget: QTabWidget = QTabWidget()
        self.__widget.currentChanged.connect(lambda index: self._setActiveIndex(index))

        self.__window.setCentralWidget(self.__widget)
        self.__window.onClose().append(lambda x, y: self._onClose(self))

        super().__init__(toolbar, graphViewFactory)

    def getWidget(self) -> QWidget:
        return self.__window

    def show(self) -> None:
        self.__window.show()

    def _appendGraphView(self, graphView: GraphView, title: str) -> None:
        self.__widget.addTab(graphView.getWidget(), title)

    def _selectGraphViewAt(self, index):
        self.__widget.setCurrentIndex(index)

    def _removeGraphView(self, index: int):
        self.__widget.removeTab(index)
