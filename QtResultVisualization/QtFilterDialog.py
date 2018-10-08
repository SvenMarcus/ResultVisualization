from typing import List

from PyQt5.QtWidgets import (QDialog, QGridLayout, QHBoxLayout, QHeaderView,
                             QLabel, QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)

from ResultVisualization.Dialogs import DialogResult
from ResultVisualization.FilterDialog import FilterDialog
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.plot import Series


class QtFilterWidget(FilterDialog):

    def __init__(self, series: Series, filterRepo: FilterRepository, parent: QWidget = None):
        self.__parent: QWidget = parent
        super(QtFilterWidget, self).__init__(series, filterRepo)

    def getWidget(self) -> QWidget:
        return self.__dialog

    def _initUI(self):
        self.__dialog: QDialog = QDialog(self.__parent)
        self.__activeFilters: QTableWidget = QTableWidget()
        self.__activeFilters.setEditTriggers(QTableWidget.NoEditTriggers)
        self.__activeFilters.setColumnCount(1)
        self.__activeFilters.setHorizontalHeaderLabels(["Active Filters"])
        self.__activeFilters.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.__availableFilters: QTableWidget = QTableWidget()
        self.__availableFilters.setEditTriggers(QTableWidget.NoEditTriggers)
        self.__availableFilters.setColumnCount(1)
        self.__availableFilters.setHorizontalHeaderLabels(["Available Filters"])
        self.__availableFilters.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.__addFilterButton: QPushButton = QPushButton("<<")
        self.__removeFilterButton: QPushButton = QPushButton(">>")

        self.__addFilterButton.clicked.connect(lambda: self.__onAddButtonClicked())
        self.__removeFilterButton.clicked.connect(lambda: self.__onRemoveButtonClicked())

        self.__dialog.setLayout(QGridLayout())

        self.__dialog.layout().addWidget(self.__activeFilters, 0, 0, 4, 1)
        self.__dialog.layout().addWidget(self.__addFilterButton, 1, 1)
        self.__dialog.layout().addWidget(self.__removeFilterButton, 2, 1)
        self.__dialog.layout().addWidget(self.__availableFilters, 0, 2, 4, 1)

    def show(self) -> DialogResult:
        self.__dialog.setModal(True)
        self.__dialog.exec()

        return self._result

    def _close(self) -> None:
        self.__dialog.done(0)

    def _addFilterToActiveFiltersTable(self, filterName) -> None:
        rows: int = self.__activeFilters.rowCount()
        self.__activeFilters.setRowCount(rows + 1)
        self.__activeFilters.setItem(rows, 0, QTableWidgetItem(filterName))

    def _addFilterToAvailableFiltersTable(self, filterName) -> None:
        rows: int = self.__availableFilters.rowCount()
        self.__availableFilters.setRowCount(rows + 1)
        self.__availableFilters.setItem(rows, 0, QTableWidgetItem(filterName))

    def _removeFilterFromActiveFiltersTable(self, index):
        self.__activeFilters.removeRow(index)
        self.__activeFilters.clearSelection()

    def _removeFilterFromAvailableFiltersTable(self, index):
        self.__availableFilters.removeRow(index)
        self.__availableFilters.clearSelection()

    def __onAddButtonClicked(self) -> None:
        rows: List[int] = self.__getSelectedRows(self.__availableFilters)
        if len(rows) > 0:
            self._addToActiveFilters(rows)

    def __onRemoveButtonClicked(self) -> None:
        rows: List[int] = self.__getSelectedRows(self.__activeFilters)
        if len(rows) > 0:
            self._removeFromActiveFilters(rows)

    def __getSelectedRows(self, table: QTableWidget) -> List[int]:
        indexes = table.selectedIndexes()
        if len(indexes) == 0:
            return list()

        return [index.row() for index in indexes]
