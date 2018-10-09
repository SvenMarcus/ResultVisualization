from PyQt5.QtWidgets import (QHBoxLayout, QHeaderView, QMainWindow,
                             QPushButton, QSplitter, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)

from QtResultVisualization.QtCreateFilterDialog import (QtCreateFilterDialog,
                                                        QtCreateFilterDialogSubViewFactory)

from QtResultVisualization.QtGraph import QtGraph
from ResultVisualization.Dialogs import SeriesDialogFactory
from ResultVisualization.FilterDialogFactory import FilterDialogFactory
from ResultVisualization.GraphView import GraphView
from ResultVisualization.plot import Graph
from ResultVisualization.SeriesRepository import SeriesRepository


class QtGraphView(GraphView):

    def __init__(self, seriesDialogFactory: SeriesDialogFactory, seriesRepository: SeriesRepository, filterDialogFactory: FilterDialogFactory):
        super(QtGraphView, self).__init__(seriesDialogFactory, seriesRepository, filterDialogFactory)
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
        self.__newSeriesButton.setDefault(True)
        self.__newSeriesButton.clicked.connect(lambda: self._addSeries())

        self.__editSeriesButton: QPushButton = QPushButton("Edit")
        self.__editSeriesButton.clicked.connect(self.__onEditClicked)

        self.__removeSeriesButton: QPushButton = QPushButton("Remove")
        self.__removeSeriesButton.clicked.connect(self.__onRemoveClicked)

        self.__editFiltersButton: QPushButton = QPushButton("Edit Series Filters")
        self.__editFiltersButton.clicked.connect(self.__onEditFiltersClicked)
        
        self.__createFiltersButton: QPushButton = QPushButton("Manage Filters")
        self.__createFiltersButton.clicked.connect(lambda: self._showCreateFilterView())

        hLayout.addWidget(self.__newSeriesButton)
        hLayout.addWidget(self.__editSeriesButton)
        hLayout.addWidget(self.__removeSeriesButton)

        layout.addLayout(hLayout)

        layout.addWidget(self.__editFiltersButton)
        layout.addWidget(self.__createFiltersButton)

        self.__window.setCentralWidget(self.__splitter)
        self.__splitter.addWidget(self.__leftWidget)
        self.__splitter.addWidget(self._graph.getWidget())

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

    def __onEditClicked(self) -> None:
        row = self.__getSelectedRow()
        if row > -1:
            self._editSeries(row)

    def __onRemoveClicked(self) -> None:
        row: int = self.__getSelectedRow()
        if row > -1:
            self._removeSeries(row)

    def __onEditFiltersClicked(self) -> None:
        row: int = self.__getSelectedRow()
        if row > -1:
            self._showEditFilterView(row)

    def __getSelectedRow(self) -> int:
        indexes = self.__seriesTable.selectedIndexes()
        if len(indexes) == 0:
            return -1

        row: int = indexes[0].row()
        return row

    def getWindow(self) -> QMainWindow:
        return self.__window
