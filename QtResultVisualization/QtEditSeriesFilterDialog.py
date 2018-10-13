from typing import List

from PyQt5.QtWidgets import (QDialog, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)

from QtResultVisualization.QtTransferWidget import QtTransferWidget
from ResultVisualization.Commands import FilterCommandFactory
from ResultVisualization.Dialogs import DialogResult
from ResultVisualization.EditSeriesFilterDialog import EditSeriesFilterDialog
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.Plot import Series
from ResultVisualization.TransferWidget import TransferWidget


class QtEditSeriesFilterDialog(EditSeriesFilterDialog):

    def __init__(self, series: Series, filterRepo: FilterRepository, commandFactory: FilterCommandFactory, parent: QWidget = None):
        self.__parent: QWidget = parent
        super(QtEditSeriesFilterDialog, self).__init__(series, filterRepo, commandFactory)

    def getWidget(self) -> QWidget:
        return self.__dialog

    def _initUI(self) -> None:
        self.__dialog: QDialog = QDialog(self.__parent)
        self.__dialog.setMinimumSize(1000, 600)
        self.__transferWidget: QtTransferWidget = QtTransferWidget()

        self.__okButton: QPushButton = QPushButton("Ok")
        self.__okButton.setDefault(True)
        self.__okButton.clicked.connect(lambda: self._confirm())
        self.__cancelButton: QPushButton = QPushButton("Cancel")
        self.__cancelButton.clicked.connect(lambda: self._cancel())

        self.__buttonLayout: QHBoxLayout = QHBoxLayout()
        self.__buttonLayout.addWidget(self.__okButton)
        self.__buttonLayout.addWidget(self.__cancelButton)

        self.__dialog.setLayout(QVBoxLayout())

        self.__dialog.layout().addWidget(self.__transferWidget.getWidget())
        self.__dialog.layout().addLayout(self.__buttonLayout)

    def _getTransferWidget(self) -> TransferWidget:
        return self.__transferWidget

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
