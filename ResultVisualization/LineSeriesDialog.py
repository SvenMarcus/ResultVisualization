import Reader.CsvReader as csvReader

from abc import ABC, abstractmethod
from numbers import Number
from typing import Any, Dict, List, Tuple

from ResultVisualization.Dialogs import ChooseFileDialog, DialogResult, SeriesDialog
from ResultVisualization.Spreadsheet import Spreadsheet, SpreadsheetView
from ResultVisualization.Plot import LineSeries, Series
from ResultVisualization.util import isNumber, tryConvertToFloat


class LineSeriesDialog(SeriesDialog, ABC):
    """Abstract class for a Dialog to select data for a line series using a Spreadsheet"""

    def __init__(self, series: LineSeries = None):
        self._result: DialogResult = DialogResult.Cancel

        self._spreadsheetView: SpreadsheetView = self._makeSpreadsheetView()
        self.__spreadsheet: Spreadsheet = Spreadsheet(self._spreadsheetView)
        self._spreadsheetView.setSpreadsheet(self.__spreadsheet)

        self.__selectedCells: Dict[str, List[Tuple[int, int]]] = {
            "x": list(),
            "y": list(),
            "meta": list()
        }

        self.__editedCoordinate: str = ""
        self.__series: LineSeries = series or LineSeries()
        self.__setInitialSeries(self.__series)

    def getSeries(self) -> Series:
        """Returns a Series object based on the data entered and selected by the user."""

        return self.__series

    def _confirm(self) -> None:
        """Called when the 'Ok' button is clicked. Displays an error message when the entered data is not valid.
        Closes the dialog if data is valid."""

        if not self.__isValidData():
            self._showMessage(
                "Invalid Data. Select same amount of x and y values. Must be at least one.")
            return

        self.__series.title = self._getTitleFromView()
        self.__series.style = self._getQuickStyleFromView()
        self.__series.confidenceBand = self._getConfidenceBandFromView() if self._getConfidenceBandFromView() else 0

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
            data: List[List[str]] = csvReader.readFile(file)
            self.__spreadsheet.setData(data)

    def _toggleEditMode(self, coordinate: str) -> None:
        """Toggles edit mode for a coordinate."""

        if not self.__editedCoordinate:
            self.__editedCoordinate = coordinate
        else:
            self.__saveSelectedCellIndices(coordinate)

            label: str = self.__tryDeterminingHeaderForCoordinate(self.__editedCoordinate)
            self.__assignLabelForCoordinate(self.__editedCoordinate, label)

            items: List[Number] = self.__getSelectedItemsForCoordinate(self.__editedCoordinate)
            self.__assignItemsForCoordinate(self.__editedCoordinate, items)

            self.__editedCoordinate = ""

        self._setUnneededInputWidgetsEnabled(not bool(self.__editedCoordinate))

    def _applyFilter(self, columnFilter: str) -> None:
        self.__spreadsheet.filterByColumnHeader(columnFilter)

    def __assignItemsForCoordinate(self, coordinate: str, items: List[Number]) -> None:
        items: List[Any] = self.__getSelectedItemsForCoordinate(coordinate)
        if coordinate == "x":
            self.__series.xValues = items
        elif coordinate == "y":
            self.__series.yValues = items
        elif coordinate == "meta":
            self.__series.metaData = items

    def __assignLabelForCoordinate(self, coordinate: str, label: str) -> None:
        if coordinate == "x":
            self.__series.xLabel = label
        elif coordinate == "y":
            self.__series.yLabel = label

    def __highlightSelectedCells(self, coordinate):
        """Highlights selected cells in the Spreadsheet."""

        if len(self.__selectedCells[coordinate]) > 0:
            self.__spreadsheet.highlight(self.__selectedCells[coordinate])

    @abstractmethod
    def _close(self) -> None:
        """Closes the Dialog."""

        raise NotImplementedError()

    @abstractmethod
    def _setUnneededInputWidgetsEnabled(self, value: bool) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getConfidenceBandFromView(self) -> float:
        """Requests the entered confidence band value from the view."""

        raise NotImplementedError()

    @abstractmethod
    def _setConfidenceBandInView(self, value: float) -> None:
        """Sets the given confidence band value in the view."""

        raise NotImplementedError()

    @abstractmethod
    def _getTitleFromView(self) -> str:
        """Requests the entered series title from the view."""

        raise NotImplementedError()

    @abstractmethod
    def _setTitleInView(self, value: str):
        """Sets the given series title in the view."""

        raise NotImplementedError()

    @abstractmethod
    def _getQuickStyleFromView(self) -> str:
        """Requests the entered quick style from the view."""

        raise NotImplementedError()

    @abstractmethod
    def _setQuickStyleInView(self, value: str):
        """Sets the given series quick style in the view."""

        raise NotImplementedError()

    @abstractmethod
    def _makeSpreadsheetView(self) -> SpreadsheetView:
        """Creates and returns a SpreadsheetView."""

        raise NotImplementedError()

    @abstractmethod
    def _makeChooseFileDialog(self) -> ChooseFileDialog:
        """Creates and returns a ChooseFileDialog."""

        raise NotImplementedError()

    @abstractmethod
    def _showMessage(self, msg: str) -> None:
        """Shows a message box with the given message."""

        raise NotImplementedError()

    @abstractmethod
    def _setWindowTitle(self, value: str) -> None:
        """Sets the Window title to the given value."""

        raise NotImplementedError()

    def __isValidData(self) -> bool:
        """Checks if the data selected by the user is valid.
        The number of x and y values must be equal and greater than 0."""

        numXValues = len(self.__selectedCells["x"])
        numYValues = len(self.__selectedCells["y"])
        return numXValues == numYValues and numXValues > 0

    def __saveSelectedCellIndices(self, coordinate) -> None:
        """Saves the indices of cells selected by the user."""

        self.__selectedCells[coordinate] = self.__spreadsheet.selectedCells()

    def __tryDeterminingHeaderForCoordinate(self, coordinate: str) -> str:
        """Tries to determine the header for a column. If first row is not a number assumes it is a column header."""

        for cell in self.__selectedCells[coordinate]:
            isFirstRow: bool = cell[0] == 0
            cellContent: Any = self.__spreadsheet.cell(cell[0], cell[1])
            if isFirstRow:
                if not isNumber(cellContent):
                    return str(cellContent)
                return ""

    def __getSelectedItemsForCoordinate(self, coordinate: str) -> List[Number]:
        """Returns the items for the given coordinate based on the selected Spreadsheet cells."""

        items: List = list()
        for cell in self.__selectedCells[coordinate]:
            item: Any = self.__spreadsheet.cell(cell[0], cell[1])
            if coordinate == "meta":
                items.append(str(item))
                continue

            num: float = tryConvertToFloat(item)
            if isNumber(num):
                items.append(num)
            else:
                items.append(str(item))

        return items

    def __setInitialSeries(self, series: LineSeries) -> None:
        """Sets data from a given PlotConfig in the view."""

        if len(series.xValues) == 0:
            return

        self._setTitleInView(series.title)
        self._setConfidenceBandInView(series.confidenceBand)
        self._setQuickStyleInView(series.style)
        values: List[List] = self.__transposePlotConfigData(series)
        self.__spreadsheet.setData(values)
        self.__setSelectedIndices(values)

    def __setSelectedIndices(self, values):
        """Sets the selected indices based on a list of lists, which each inner list representing a row."""

        for rowIndex in range(0, len(values)):
            self.__selectedCells["x"].append((rowIndex, 0))
            self.__selectedCells["y"].append((rowIndex, 1))

    @staticmethod
    def __transposePlotConfigData(series: LineSeries) -> List[List]:
        """Transposes x and y values from a PlotConfig into column format."""

        data: List[List] = [series.xValues, series.yValues]
        if len(series.metaData) > 0:
            data.append(series.metaData)

        return list(map(list, zip(*data)))
