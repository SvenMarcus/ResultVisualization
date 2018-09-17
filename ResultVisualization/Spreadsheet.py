from abc import ABC, abstractmethod
from typing import Any, List, Set, Tuple

from ResultVisualization.Events import Event, InvokableEvent


class SpreadsheetView(ABC):

    @abstractmethod
    def setSpreadsheet(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def setColumnCount(self, count: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def setRowCount(self, count: int) -> None:
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
