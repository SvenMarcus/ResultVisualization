import Reader.CsvReader as csvReader

from abc import ABC, abstractmethod
from typing import Any, List, Tuple

from ResultVisualization.Dialogs import ChooseFileDialog, SeriesDialog, DialogResult
from ResultVisualization.Plot import BoxSeries, Series
from ResultVisualization.Spreadsheet import Spreadsheet, SpreadsheetView
from ResultVisualization.util import isNumber, tryConvertToFloat


class BoxSeriesDialog(SeriesDialog, ABC):
    """Abstract class for a Dialog to select data for a box series using a Spreadsheet"""

    def __init__(self, initialSeries: BoxSeries = None):
        self._spreadsheetView: SpreadsheetView = self._makeSpreadsheetView()
        self.__spreadsheet: Spreadsheet = Spreadsheet(self._spreadsheetView)
        self._spreadsheetView.setSpreadsheet(self.__spreadsheet)

        self.__series: BoxSeries = initialSeries or BoxSeries()
        self.__setInitialSeries(self.__series)

        self.__selectedData: List[List[Any]] = list()
        self.__inEditMode: bool = False
        self._result: DialogResult = DialogResult.Cancel

    def getSeries(self) -> Series:
        """Returns a Series object based on the data entered and selected by the user."""

        return self.__series

    def _applyFilter(self, columnFilter: str) -> None:
        self.__spreadsheet.filterByColumnHeader(columnFilter)

    def _confirm(self) -> None:
        """Called when the 'Ok' button is clicked. Displays an error message when the entered data is not valid.
        Closes the dialog if data is valid."""

        self.__series.title = self._getTitleFromView()

        if len(self.__series.data) == 0:
            self._showMessage("Invalid data. No data selected.")
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
    def _getTitleFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _setTitleInView(self, title: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _setUnneededInputWidgetsEnabled(self, value: bool) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _showMessage(self, msg: str) -> None:
        """Shows a message box with the given message."""

        raise NotImplementedError()

    def __setInitialSeries(self, series: BoxSeries) -> None:
        self._setTitleInView(series.title)

        data: List[List] = self.__transposePlotConfigData(series)
        if len(series.metaData) > 0:
            data.insert(0, series.metaData)

        self.__spreadsheet.setData(data)

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

        columns.append(column)

        return columns

    @staticmethod
    def __transposePlotConfigData(series: BoxSeries) -> List[List]:
        """Transposes x and y values from a PlotConfig into column format."""

        data: List[List] = list(series.data)

        return list(map(list, zip(*data)))
