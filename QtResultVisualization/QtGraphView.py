from typing import Iterable

from PyQt5.QtWidgets import (QHeaderView,
                             QSplitter, QTableWidget,
                             QTableWidgetItem, QWidget)

from QtResultVisualization.QtGraph import QtGraph
from ResultVisualization.GraphView import GraphView
from ResultVisualization.Plot import Graph, Series


class QtGraphView(GraphView):

    def __init__(self, initialSeries: Iterable[Series]):
        self.__splitter: QSplitter = QSplitter()
        self.__splitter.setMinimumWidth(1200)
        self.__splitter.setMinimumHeight(800)

        self.__seriesTable: QTableWidget = QTableWidget()
        self.__seriesTable.setMaximumWidth(500)
        self.__seriesTable.setSelectionBehavior(QTableWidget.SelectItems)
        self.__seriesTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.__seriesTable.setColumnCount(1)
        self.__seriesTable.setHorizontalHeaderLabels(["Series"])
        self.__seriesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        super(QtGraphView, self).__init__(initialSeries)

        self.__splitter.addWidget(self.__seriesTable)
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
