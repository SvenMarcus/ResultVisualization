from typing import Iterable

from PyQt5.QtWidgets import (QHBoxLayout, QHeaderView,
                             QPushButton, QSplitter, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)

from QtResultVisualization.QtGraph import QtGraph
from ResultVisualization.GraphView import GraphView
from ResultVisualization.Plot import Graph, Series


class QtGraphView(GraphView):

    def __init__(self, initialSeries: Iterable[Series]):
        self.__splitter: QSplitter = QSplitter()
        self.__splitter.setMinimumWidth(1200)
        self.__splitter.setMinimumHeight(800)

        self.__leftWidget: QWidget = QWidget(self.__splitter)
        layout: QVBoxLayout = QVBoxLayout()
        self.__leftWidget.setMaximumWidth(500)
        self.__leftWidget.setLayout(layout)

        self.__seriesTable: QTableWidget = QTableWidget()
        self.__seriesTable.setSelectionBehavior(QTableWidget.SelectItems)
        self.__seriesTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.__seriesTable.setColumnCount(1)
        self.__seriesTable.setHorizontalHeaderLabels(["Series"])
        self.__seriesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        layout.addWidget(self.__seriesTable)

        hLayout: QHBoxLayout = QHBoxLayout()

        self.__saveGraphButton: QPushButton = QPushButton("Save Graph View")
        self.__saveGraphButton.clicked.connect(lambda: self.saveCommand.execute())

        self.__newSeriesButton: QPushButton = QPushButton("Add")
        self.__newSeriesButton.setDefault(True)
        self.__newSeriesButton.clicked.connect(lambda: self.addSeriesCommand.execute())

        self.__editSeriesButton: QPushButton = QPushButton("Edit")
        self.__editSeriesButton.clicked.connect(lambda: self.editSeriesCommand.execute())

        self.__removeSeriesButton: QPushButton = QPushButton("Remove")
        self.__removeSeriesButton.clicked.connect(lambda: self.removeSeriesCommand.execute())

        self.__duplicateSeriesButton: QPushButton = QPushButton("Duplicate")
        self.__duplicateSeriesButton.clicked.connect(lambda: self.duplicateCommand.execute())

        self.__fillAreaButton: QPushButton = QPushButton("Fill Area")
        self.__fillAreaButton.clicked.connect(lambda: self.fillAreaCommand.execute())

        self.__editFiltersButton: QPushButton = QPushButton("Edit Series Filters")
        self.__editFiltersButton.clicked.connect(lambda: self.editSeriesFilterCommand.execute())

        self.__createFiltersButton: QPushButton = QPushButton("Manage Filters")
        self.__createFiltersButton.clicked.connect(lambda: self.createFilterCommand.execute())

        hLayout.addWidget(self.__newSeriesButton)
        hLayout.addWidget(self.__editSeriesButton)
        hLayout.addWidget(self.__removeSeriesButton)

        layout.addLayout(hLayout)

        layout.addWidget(self.__duplicateSeriesButton)
        layout.addWidget(self.__fillAreaButton)
        layout.addWidget(self.__editFiltersButton)
        layout.addWidget(self.__createFiltersButton)

        super(QtGraphView, self).__init__(initialSeries)

        self.__splitter.addWidget(self.__leftWidget)
        self.__splitter.addWidget(self._graph.getWidget())

    def show(self):
        self.__splitter.show()

    def _makeGraph(self) -> Graph:
        return QtGraph()

    def _addEntryToListView(self, title: str) -> None:
        rows: int = self.__seriesTable.rowCount()
        self.__seriesTable.setRowCount(rows + 1)
        self.__seriesTable.setItem(rows, 0, QTableWidgetItem(title))

    def _setEntryInListView(self, index: int, value: str) -> None:
        self.__seriesTable.setItem(index, 0, QTableWidgetItem(value))

    def _removeEntryFromListView(self, index: int) -> None:
        self.__seriesTable.removeRow(index)
        self.__seriesTable.clearSelection()

    def _getSelectedRow(self) -> int:
        indexes = self.__seriesTable.selectedIndexes()
        if len(indexes) == 0:
            return -1

        row: int = indexes[0].row()
        return row

    def getWidget(self) -> QWidget:
        return self.__splitter
