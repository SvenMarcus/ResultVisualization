import sys
from typing import Any, List, Set, Tuple

from PyQt5.QtWidgets import QAbstractItemView, QTableWidget, QTableWidgetItem, \
    QWidget

from ResultVisualization.Spreadsheet import Spreadsheet, SpreadsheetView


class QtSpreadsheet(SpreadsheetView):

    def __init__(self, parent: QWidget = None):
        self.__widget: QTableWidget = QTableWidget(parent)
        self.__widget.setMinimumHeight(400)
        self.__widget.setMinimumWidth(400)
        self.__widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__widget.itemSelectionChanged.connect(self.__onSelectionChanged)
        self.__widget.__spreadsheet: Spreadsheet = None
    
    def setSpreadsheet(self, spreadsheet: Spreadsheet) -> None:
        self.__spreadsheet = spreadsheet

    def setColumnCount(self, columns: int) -> None:
        self.__widget.setColumnCount(columns)

    def setRowCount(self, rows: int) -> None:
        self.__widget.setRowCount(rows)

    def addRow(self) -> None:
        self.__widget.setRowCount(self.__widget.rowCount() + 1)
        for i in range(0, self.__widget.columnCount()):
            self.__widget.setItem(self.__widget.rowCount() - 1, i, QTableWidgetItem())

    def addColumn(self) -> None:
        self.setColumnCount(self.__widget.columnCount() + 1)

    def setCell(self, row: int, column: int, value: Any) -> None:
        self.__widget.setItem(row, column, QTableWidgetItem(str(value)))

    def __onSelectionChanged(self) -> None:
        selectedIndeces: List[Tuple[int, int]] = list()
        for index in self.__widget.selectedIndexes():
            selectedIndeces.append((index.row(), index.column()))

        self.__spreadsheet.handleCellSelectionChanged(selectedIndeces)
    
    def getTableWidget(self) -> QTableWidget:
        return self.__widget
