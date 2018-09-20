from abc import ABC, abstractmethod
from enum import Enum
from numbers import Number
from typing import Any, Dict, List, Tuple

import Reader.CsvReader as csvReader
from ResultVisualization.Graph import PlotConfig
from ResultVisualization.Spreadsheet import Spreadsheet, SpreadsheetView


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

    def __init__(self, config: PlotConfig = PlotConfig()):
        self._result: DialogResult = DialogResult.Cancel

        self._spreadsheetView: SpreadsheetView = self._makeSpreadsheetView()
        self.__spreadsheet: Spreadsheet = Spreadsheet(self._spreadsheetView)
        self._spreadsheetView.setSpreadsheet(self.__spreadsheet)

        self.__selectedCells: Dict[str, List[Tuple[int, int]]] = {
            "x": list(),
            "y": list()
        }

        self.__editedCoordinate: str = ""
        self.__plotConfig: PlotConfig = config
        self.__setInitialPlotConfig(config)

    def getPlotConfig(self) -> PlotConfig:
        config: PlotConfig = self.__plotConfig
        config.title = self._getTitleFromView()
        config.xValues = self.__getSelectedItemsForCoordinate("x")
        config.yValues = self.__getSelectedItemsForCoordinate("y")
        config.confidenceBand = self._getConfidenceBandFromView() if self._getConfidenceBandFromView() else 0
        return config

    def _confirm(self) -> None:
        if not self.__isValidData():
            self._showMessage(
                "Invalid Data. Select same amount of x and y values. Must be at least one.")
            return

        self._result = DialogResult.Ok
        self._close()

    def _handleLoadFile(self) -> None:
        dialog: ChooseFileDialog = self._makeChooseFileDialog()
        result: DialogResult = dialog.show()
        if result == DialogResult.Ok:
            file: str = dialog.getSelectedFile()
            data: List[List[str]] = csvReader.readFile(
                file, csvReader.semicolon)
            self.__spreadsheet.setData(data)

    def _startListeningForDataSelection(self, coordinate: str) -> None:
        self.__editedCoordinate = coordinate

        if len(self.__selectedCells[coordinate]) > 0:
            self.__spreadsheet.highlight(self.__selectedCells[coordinate])

    def _stopListeningForDataSelection(self) -> None:
        if self.__editedCoordinate:
            self.__getSelectedCells()
            self.__editedCoordinate = ""

    @staticmethod
    def _tryConvertToFloat(obj: Any) -> float:
        try:
            return float(obj)
        except:
            return None

    @abstractmethod
    def _close(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getConfidenceBandFromView(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def _setConfidenceBandInView(self, value: float) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getTitleFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _setTitleInView(self, value: str):
        raise NotImplementedError()

    @abstractmethod
    def _makeSpreadsheetView(self) -> SpreadsheetView:
        raise NotImplementedError()

    @abstractmethod
    def _makeChooseFileDialog(self) -> ChooseFileDialog:
        raise NotImplementedError()

    @abstractmethod
    def _showMessage(self, msg: str) -> None:
        raise NotImplementedError()

    def __isValidData(self) -> bool:
        numXValues = len(self.__selectedCells["x"])
        numYValues = len(self.__selectedCells["y"])
        return numXValues == numYValues and numXValues > 0

    def __getSelectedCells(self) -> None:
        self.__selectedCells[self.__editedCoordinate] = list(
            self.__spreadsheet.selectedCells())

    def __getSelectedItemsForCoordinate(self, coordinate: str) -> List[Number]:
        items: List = list()
        for cell in self.__selectedCells[coordinate]:
            item: Any = self.__spreadsheet.cell(cell[0], cell[1])
            num: float = self._tryConvertToFloat(item)
            if self.__isNumber(num):
                items.append(num)
        return items

    @staticmethod
    def __isNumber(obj: Any) -> bool:
        return isinstance(obj, (int, float))

    def __setInitialPlotConfig(self, config: PlotConfig) -> None:
        self._setTitleInView(config.title)
        self._setConfidenceBandInView(config.confidenceBand)
        values: List[List] = self.__transposePlotConfigData(config)
        self.__spreadsheet.setData(values)

    @staticmethod
    def __transposePlotConfigData(config: PlotConfig) -> List[List]:
        data: List[List] = [config.xValues, config.yValues]
        return list(map(list, zip(*data)))


class DataChooserDialog(Dialog, ABC):
    """Interface for a dialog to choose data"""

    @abstractmethod
    def getChosenData(self) -> Dict[str, float]:
        """Returns the data chosen in the dialog as dictionary of strings and floats."""

        raise NotImplementedError()


class DialogFactory(ABC):
    """Interface for a factory to create dialogs"""

    @abstractmethod
    def makeChooseFolderDialog(self) -> ChooseFolderDialog:
        """Creates and returns a ChooseFolderDialog."""

        raise NotImplementedError()

    @abstractmethod
    def makeDataChooserDialog(self) -> DataChooserDialog:
        """Creates and returns a DataChooserDialog."""

        raise NotImplementedError()
