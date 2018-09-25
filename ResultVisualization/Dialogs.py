from abc import ABC, abstractmethod
from enum import Enum
from numbers import Number
from typing import Any, Dict, List, Tuple

import Reader.CsvReader as csvReader
from ResultVisualization.Graph import PlotConfig
from ResultVisualization.Spreadsheet import Spreadsheet, SpreadsheetView
from ResultVisualization.util import isNumber, tryConvertToFloat


class DialogResult(Enum):
    Ok: int = 0
    Cancel: int = 1


class Dialog(ABC):
    """Interface for a dialog window"""

    @abstractmethod
    def show(self) -> DialogResult:
        """Shows the dialog window. Modality depends on implementation."""

        raise NotImplementedError()


class ChooseFolderDialog(Dialog, ABC):
    """Interface for a folder chooser dialog"""

    @abstractmethod
    def setStartingFolder(self, path: str) -> None:
        """Shows the dialog window. Modality depends on implementation."""

        raise NotImplementedError()

    @abstractmethod
    def getSelectedFolder(self) -> str:
        """Returns the folder selected by the user. If the dialog was canceled, returns an empty string."""

        raise NotImplementedError()


class ChooseFileDialog(Dialog, ABC):
    """Interface for a file chooser dialog"""

    @abstractmethod
    def setStartingFolder(self, path: str) -> None:
        """Shows the dialog window. Modality depends on implementation."""

        raise NotImplementedError()

    @abstractmethod
    def getSelectedFile(self) -> str:
        """Returns the file selected by the user. If the dialog was canceled, returns an empty string."""

        raise NotImplementedError()


class LineSeriesDialog(Dialog, ABC):
    """Abstract class for a Dialog to select data for a line series using a Spreadsheet"""

    def __init__(self, config: PlotConfig = None):
        self._result: DialogResult = DialogResult.Cancel

        self._spreadsheetView: SpreadsheetView = self._makeSpreadsheetView()
        self.__spreadsheet: Spreadsheet = Spreadsheet(self._spreadsheetView)
        self._spreadsheetView.setSpreadsheet(self.__spreadsheet)

        self.__selectedCells: Dict[str, List[Tuple[int, int]]] = {
            "x": list(),
            "y": list()
        }

        self.__editedCoordinate: str = ""
        self.__plotConfig: PlotConfig = config or PlotConfig()
        self.__setInitialPlotConfig(self.__plotConfig)

    def getPlotConfig(self) -> PlotConfig:
        """Returns a PlotConfig object based on the data entered and selected by the user."""

        config: PlotConfig = self.__plotConfig
        config.title = self._getTitleFromView()
        config.xLabel = self.__tryDeterminingHeaderForCoordinate("x")
        config.yLabel = self.__tryDeterminingHeaderForCoordinate("y")
        print(config.xLabel, config.yLabel)
        config.xValues = self.__getSelectedItemsForCoordinate("x")
        config.yValues = self.__getSelectedItemsForCoordinate("y")
        config.confidenceBand = self._getConfidenceBandFromView() if self._getConfidenceBandFromView() else 0
        return config

    def _confirm(self) -> None:
        """Called when the 'Ok' button is clicked. Displays an error message when the entered data is not valid.
        Closes the dialog if data is valid."""

        if not self.__isValidData():
            self._showMessage(
                "Invalid Data. Select same amount of x and y values. Must be at least one.")
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
            data: List[List[str]] = csvReader.readFile(
                file, csvReader.semicolon)
            self.__spreadsheet.setData(data)

    def _toggleEditMode(self, coordinate: str) -> None:
        """Toggles edit mode for a coordinate."""

        if not self.__editedCoordinate:
            self.__editedCoordinate = coordinate
            self.__highlightSelectedCells(coordinate)
        else:
            self.__saveSelectedCellIndices(coordinate)
            self.__editedCoordinate = ""

        self._setUnneededInputWidgetsEnabled(not bool(self.__editedCoordinate))

    def _applyFilter(self, columnFilter: str) -> None:
        self.__spreadsheet.filterByColumnHeader(columnFilter)

    @abstractmethod
    def _setUnneededInputWidgetsEnabled(self, value: bool) -> None:
        raise NotImplementedError()

    def __highlightSelectedCells(self, coordinate):
        """Highlights selected cells in the Spreadsheet."""

        if len(self.__selectedCells[coordinate]) > 0:
            self.__spreadsheet.highlight(self.__selectedCells[coordinate])

    @abstractmethod
    def _close(self) -> None:
        """Closes the Dialog."""

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
                    print(cellContent)
                    return str(cellContent)
                return ""

    def __getSelectedItemsForCoordinate(self, coordinate: str) -> List[Number]:
        """Returns the items for the given coordinate based on the selected Spreadsheet cells."""

        items: List = list()
        for cell in self.__selectedCells[coordinate]:
            item: Any = self.__spreadsheet.cell(cell[0], cell[1])
            num: float = tryConvertToFloat(item)
            if isNumber(num):
                items.append(num)
        return items

    def __setInitialPlotConfig(self, config: PlotConfig) -> None:
        """Sets data from a given PlotConfig in the view."""

        if len(config.xValues) == 0:
            return

        self._setTitleInView(config.title)
        self._setConfidenceBandInView(config.confidenceBand)
        firstRow: List[str] = [config.xLabel, config.yLabel]
        values: List[List] = self.__transposePlotConfigData(config)
        values.insert(0, firstRow)
        self.__spreadsheet.setData(values)
        self.__setSelectedIndices(values)

    def __setSelectedIndices(self, values):
        """Sets the selected indices based on a list of lists, which each inner list representing a row."""

        for rowIndex in range(0, len(values)):
            self.__selectedCells["x"].append((rowIndex, 0))
            self.__selectedCells["y"].append((rowIndex, 1))

    @staticmethod
    def __transposePlotConfigData(config: PlotConfig) -> List[List]:
        """Transposes x and y values from a PlotConfig into column format."""

        data: List[List] = [config.xValues, config.yValues]
        return list(map(list, zip(*data)))
