import Reader.CsvReader as csvReader

from abc import ABC, abstractmethod
from typing import Any, List, Tuple

from ResultVisualization.Dialogs import SeriesDialog, DialogResult
from ResultVisualization.Plot import BoxSeries, Series
from ResultVisualization.Spreadsheet import Spreadsheet, SpreadsheetView
from ResultVisualization.util import isNumber, tryConvertToFloat


class BoxSeriesDialog(SeriesDialog, ABC):

    def __init__(self, initialSeries: BoxSeries = None):
        self._spreadsheetView: SpreadsheetView = self._makeSpreadsheetView()
        self.__spreadsheet: Spreadsheet = Spreadsheet(self._spreadsheetView)
        self._spreadsheetView.setSpreadsheet(self.__spreadsheet)

        self.__series: BoxSeries = initialSeries or BoxSeries()

        self.__selectedData: List[List[Any]] = list()
        self.__inEditMode: bool = False
        self._result: DialogResult = DialogResult.Cancel

    def getSeries(self) -> Series:
        return self.__series

    def _applyFilter(self, columnFilter: str) -> None:
        self.__spreadsheet.filterByColumnHeader(columnFilter)

    def _confirm(self) -> None:
        self.__series.title = self._getTitleFromView()

        if len(self.__series.data) == 0:
            return

        self._result = DialogResult.Ok
        self._close()

    def _handleLoadFile(self) -> None:
        """Shows a ChooseFileDialog and loads the selected csv file.
        The data from the file gets inserted into the spreadsheet."""

        dialog: ChooseFileDialog = self._makeChooseFileDialog()
        result: DialogResult = dialog.show()
        if result == DialogResult.Ok:
            file: str = dialog.getSelectedFile()
            self._setWindowTitle(file)
            data: List[List[Any]] = csvReader.readFile(file)
            self.__spreadsheet.setData(data)

    def _toggleSelectData(self) -> None:
        self.__inEditMode = not self.__inEditMode
        self._setUnneededInputWidgetsEnabled(not self.__inEditMode)
        if not self.__inEditMode:
            self.__assignDataToSeries()

    @abstractmethod
    def _close(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _setUnneededInputWidgetsEnabled(self, value: bool) -> None:
        raise NotImplementedError()

    def __assignDataToSeries(self) -> None:
        selectedItems: List[List[Any]] = self.__getSelectedDataItems()

        if len(selectedItems) == 0:
            return

        meta: List[str] = self.__getMetaItems(self.__spreadsheet.selectedCells())
        self.__series.data = selectedItems
        self.__series.metaData = meta

    def __getMetaItems(self, selectedCells: List[Tuple[int, int]]) -> List[str]:
        meta: List[str] = list()
        for cell in selectedCells:
            isFirstRow = cell[0] == 0
            if isFirstRow:
                item: Any = self.__spreadsheet.cell(cell[0], cell[1])
                meta.append(str(item))

        return meta

    def __getSelectedDataItems(self) -> List[List[Any]]:
        """Returns the items based on the selected Spreadsheet cells."""

        selectedCells: List[Tuple[int, int]] = list(sorted(self.__spreadsheet.selectedCells(), key=lambda cell: cell[1]))

        if len(selectedCells) == 0:
            return list()

        columns: List[List[Any]] = list()

        currentColumn: int = selectedCells[0][1]
        column: List[Any] = list()
        for cell in selectedCells:
            if cell[1] > currentColumn:
                currentColumn = cell[1]
                columns.append(column)
                column = list()

            item: Any = self.__spreadsheet.cell(cell[0], cell[1])
            num: float = tryConvertToFloat(item)
            if isNumber(num):
                column.append(num)
            # else:
            #     column.append(str(item))

        columns.append(column)

        return columns
