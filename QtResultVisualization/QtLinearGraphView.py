from PyQt5.QtWidgets import QHBoxLayout, QHeaderView, \
    QMainWindow, QPushButton, QSplitter, QTableWidget, QTableWidgetItem, \
    QVBoxLayout, QWidget

from QtResultVisualization.Dialogs import QtLineSeriesDialog
from QtResultVisualization.QtGraph import QtGraph
from ResultVisualization.Dialogs import LineSeriesDialog
from ResultVisualization.Graph import Graph, PlotConfig
from ResultVisualization.LinearGraphView import LinearGraphView


class QtLinearGraphView(LinearGraphView):

    def __init__(self):
        super(QtLinearGraphView, self).__init__()
        self.__window: QMainWindow = QMainWindow()
        self.__window.setMinimumWidth(300)
        self.__window.setMinimumHeight(300)
        self.__splitter: QSplitter = QSplitter(self.__window)
        self.__leftWidget: QWidget = QWidget(self.__splitter)
        layout: QVBoxLayout = QVBoxLayout()
        self.__leftWidget.setLayout(layout)

        self.__seriesTable: QTableWidget = QTableWidget()
        self.__seriesTable.setSelectionBehavior(QTableWidget.SelectItems)
        self.__seriesTable.setColumnCount(1)
        self.__seriesTable.setHorizontalHeaderLabels(["Series"])
        self.__seriesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        layout.addWidget(self.__seriesTable)

        hLayout: QHBoxLayout = QHBoxLayout()

        self.__newSeriesButton: QPushButton = QPushButton("Add")
        self.__newSeriesButton.clicked.connect(lambda: self._addSeries())

        self.__editSeriesButton: QPushButton = QPushButton("Edit")
        self.__editSeriesButton.clicked.connect(self.__onEditClicked)

        self.__removeSeriesButton: QPushButton = QPushButton("Remove")
        self.__removeSeriesButton.clicked.connect(self.__onRemoveClicked)

        hLayout.addWidget(self.__newSeriesButton)
        hLayout.addWidget(self.__editSeriesButton)
        hLayout.addWidget(self.__removeSeriesButton)

        layout.addLayout(hLayout)

        self.__window.setCentralWidget(self.__splitter)
        self.__splitter.addWidget(self.__leftWidget)
        self.__splitter.addWidget(self._graph.getWidget())

    def _makeGraph(self) -> Graph:
        return QtGraph()

    def _makeLineSeriesDialog(self, config: PlotConfig=PlotConfig()) -> LineSeriesDialog:
        return QtLineSeriesDialog(config, self.__window)

    def _addEntryToListView(self, title: str) -> None:
        rows: int = self.__seriesTable.rowCount()
        self.__seriesTable.setRowCount(rows + 1)
        self.__seriesTable.setItem(rows, 0, QTableWidgetItem(title))

    def _setEntryInListView(self, index: int, value: str) -> None:
        self.__seriesTable.setItem(index, 0, QTableWidgetItem(value))

    def _removeEntryFromListView(self, index: int) -> None:
        self.__seriesTable.removeRow(index)

    def __onEditClicked(self) -> None:
        row = self.__getSelectedRow()
        if row > -1:
            self._editSeries(row)

    def __onRemoveClicked(self) -> None:
        row: int = self.__getSelectedRow()
        if row > -1:
            self._removeSeries(row)

    def __getSelectedRow(self) -> int:
        indexes = self.__seriesTable.selectedIndexes()
        if len(indexes) == 0:
            return -1

        row: int = indexes[0].row()
        return row

    def getWindow(self) -> QMainWindow:
        return self.__window