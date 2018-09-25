from abc import ABC, abstractmethod
from typing import Any, List, Tuple

from ResultVisualization.Events import Event, InvokableEvent


class SpreadsheetView(ABC):

    @abstractmethod
    def setSpreadsheet(self, spreadsheet) -> None:
        raise NotImplementedError()

    @abstractmethod
    def setColumnCount(self, columns: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def setRowCount(self, rows: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def addRow(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def addColumn(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def setCell(self, row: int, column: int, value: Any) -> None:
        raise NotImplementedError()

    @abstractmethod
    def highlight(self, cells: List[Tuple[int, int]]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def setColumnVisible(self, column: int, visible: bool) -> None:
        raise NotImplementedError()


class Spreadsheet:

    def __init__(self, view: SpreadsheetView):
        self.__columns: int = 0
        self.__rows: int = 0
        self.__onCellSelectionChanged: InvokableEvent = InvokableEvent()
        self.__view: SpreadsheetView = view

        self.__data: List[List[Any]] = []
        self.__selectedCells: List[Tuple[int, int]] = list()

    @property
    def onCellSelectionChanged(self) -> Event:
        return self.__onCellSelectionChanged

    def setData(self, data: List[List[Any]]) -> None:
        self.__data = data
        self.__rows = len(self.__data)
        self.__view.setRowCount(self.__rows)

        self.__columns: int = 0
        for rowIndex in range(0, self.__rows):
            row = self.__data[rowIndex]
            if len(row) > self.__columns:
                self.__columns = len(row)
                self.__view.setColumnCount(self.__columns)

            for columnIndex in range(0, len(row)):
                columnItem: Any = row[columnIndex]
                self.__view.setCell(rowIndex, columnIndex, columnItem)

    def filterByColumnHeader(self, value: str) -> None:
        if len(self.__data) == 0:
            return

        columnHeaders: List[Any] = self.__data[0]

        for columnIndex in range(0, len(columnHeaders)):
            column: Any = columnHeaders[columnIndex]
            strHeader: str = str(column)

            visible: bool = False
            if value.lower() in strHeader.lower():
                visible = True

            self.__view.setColumnVisible(columnIndex, visible)

    def highlight(self, cells: List[Tuple[int, int]]) -> None:
        self.__view.highlight(cells)

    def rows(self) -> int:
        return self.__rows

    def columns(self) -> int:
        return self.__columns

    def cell(self, row: int, column: int) -> Any:
        return self.__data[row][column]

    def setCell(self, row: int, column: int, value: Any) -> None:
        self.__data[row][column] = value
        self.__view.setCell(row, column, value)

    def selectedCells(self) -> List[Tuple[int, int]]:
        return list(self.__selectedCells)

    def handleCellSelectionChanged(self, selectedIndeces: List[Tuple[int, int]]) -> None:
        self.__selectedCells = selectedIndeces
        self.__onCellSelectionChanged(self)
