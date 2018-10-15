import sys
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QAction, QMainWindow, QTabWidget, QToolBar, QWidget

from QtResultVisualization.QtGraphViewFactory import QtGraphViewFactory

from ResultVisualization.GraphView import GraphView
from ResultVisualization.MainWindow import MainWindow


class QtMainWindow(MainWindow):

    def __init__(self, graphViewFactory: QtGraphViewFactory):
        self.__window: QMainWindow = QMainWindow()
        self.__toolbar: QToolBar = QToolBar()

        moduleFolder: str = sys.path[0]
        linearIcon: QtGui.QIcon = QtGui.QIcon(moduleFolder + "/resources/LinePlot2.svg")
        linearAction: QAction = QAction(linearIcon, "New Linear Plot", self.__toolbar)
        linearAction.triggered.connect(lambda: self._newLinearPlot())

        boxIcon: QtGui.QIcon = QtGui.QIcon(moduleFolder + "/resources/BoxPlot2.svg")
        boxAction: QAction = QAction(boxIcon, "New Box Plot", self.__toolbar)
        boxAction.triggered.connect(lambda: self._newBoxPlot())

        closeIcon: QtGui.QIcon = QtGui.QIcon(moduleFolder + "/resources/Close.svg")
        closeAction: QAction = QAction(closeIcon, "Close Active Plot", self.__toolbar)
        closeAction.triggered.connect(lambda: self._closeActiveGraphView())

        saveIcon: QtGui.QIcon = QtGui.QIcon(moduleFolder + "/resources/Save.svg")
        saveAction: QAction = QAction(saveIcon, "Save Active Plot", self.__toolbar)
        saveAction.triggered.connect(lambda: self._save())

        loadIcon: QtGui.QIcon = QtGui.QIcon(moduleFolder + "/resources/Load.svg")
        loadAction: QAction = QAction(loadIcon, "Load Plot", self.__toolbar)
        loadAction.triggered.connect(lambda: self.loadFileCommand.execute())

        self.__toolbar.addAction(linearAction)
        self.__toolbar.addAction(boxAction)
        self.__toolbar.addSeparator()
        self.__toolbar.addAction(closeAction)
        self.__toolbar.addSeparator()
        self.__toolbar.addAction(saveAction)
        self.__toolbar.addAction(loadAction)
        self.__window.addToolBar(self.__toolbar)

        self.__widget: QTabWidget = QTabWidget()
        self.__widget.currentChanged.connect(lambda index: self._setActiveIndex(index))

        self.__window.setCentralWidget(self.__widget)

        super().__init__(graphViewFactory)

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
