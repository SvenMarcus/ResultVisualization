
from typing import Dict, List, Set, Tuple

from PyQt5.QtWidgets import QDialog, QFileDialog, QGridLayout, QHBoxLayout, \
    QLabel, QLineEdit, QMessageBox, QPushButton, QTableWidget, \
    QTableWidgetSelectionRange, QWidget
from matplotlib.pyplot import show

from QtResultVisualization.QtSpreadsheet import QtSpreadsheet
from ResultVisualization.Dialogs import ChooseFileDialog, ChooseFolderDialog, \
    DataChooserDialog, DialogFactory, DialogResult, LineSeriesDialog
from ResultVisualization.Spreadsheet import Spreadsheet, SpreadsheetView


class QtChooseFolderDialog(ChooseFolderDialog):
    """Qt Implementation of ChooseFolderDialog"""

    def __init__(self, parent: QWidget = None):
        self.__selectedFolder: str = ""
        self.__parent: QWidget = parent

    def setStartingFolder(self, path: str) -> None:
        pass

    def getSelectedFolder(self) -> str:
        return self.__selectedFolder

    def show(self) -> DialogResult:
        self.__selectedFolder = str(QFileDialog.getExistingDirectory(
            self.__parent, "Select Folder", options=QFileDialog.ShowDirsOnly))
        if self.__selectedFolder:
            return DialogResult.Ok

        return DialogResult.Cancel


class QtChooseFileDialog(ChooseFileDialog):
    """Qt Implementation of ChooseFolderDialog"""

    def __init__(self, parent: QWidget = None):
        self.__selectedFile: str = ""
        self.__parent: QWidget = parent

    def setStartingFolder(self, path: str) -> None:
        pass

    def getSelectedFile(self) -> str:
        return self.__selectedFile

    def show(self) -> DialogResult:
        self.__selectedFile = QFileDialog.getOpenFileName(
            self.__parent, "Select File", filter="*.csv")[0]
        print(self.__selectedFile)
        if self.__selectedFile and isinstance(self.__selectedFile, str):
            return DialogResult.Ok

        return DialogResult.Cancel

class QtLineSeriesDialog(LineSeriesDialog):
    """Qt implementation of LineSeriesDialog"""

    def __init__(self, parent: QWidget = None):
        super(QtLineSeriesDialog, self).__init__()
        self.__dialog: QDialog = QDialog(parent)
        self.__layout: QGridLayout = QGridLayout(self.__dialog)
        self.__dialog.setLayout(self.__layout)

        self.__loadFileButton: QPushButton = QPushButton("Load csv file")
        self.__loadFileButton.clicked.connect(self._handleLoadFile)
        self.__layout.addWidget(self.__loadFileButton, 0, 0, 1, 2)

        self.__xValuesButton: QPushButton = QPushButton("Select x values")
        self.__yValuesButton: QPushButton = QPushButton("Select y values")
        self.__layout.addWidget(self.__xValuesButton, 1, 0)
        self.__layout.addWidget(self.__yValuesButton, 1, 1)

        self.__layout.addWidget(QLabel("Confidence Interval:"), 0, 2)

        self.__confidenceBandInput: QLineEdit = QLineEdit()
        self.__layout.addWidget(self.__confidenceBandInput, 1, 2)

        self.__okButton: QPushButton = QPushButton("Ok")
        self.__okButton.clicked.connect(self._confirm)
        self.__okButton.setMinimumWidth(150)
        self.__cancelButton: QPushButton = QPushButton("Cancel")
        self.__cancelButton.clicked.connect(lambda: self.__dialog.close())

        self.__layout.addWidget(self.__okButton, 2, 0)
        self.__layout.addWidget(self.__cancelButton, 2, 1)

        self.__layout.addWidget(self._spreadsheetView.getTableWidget(), 3, 0, -1, -1)

        self.__inEditMode: bool = False
        self.__editState: Dict[str, bool] = {"x": False, "y": False}
        self.__buttonDict: Dict[str, QPushButton] = {"x": self.__xValuesButton, "y": self.__yValuesButton}
        self.__xValuesButton.clicked.connect(
            lambda: self.__handleDataSelectionButton(self.__xValuesButton, "x"))
        self.__yValuesButton.clicked.connect(
            lambda: self.__handleDataSelectionButton(self.__yValuesButton, "y"))

    def show(self) -> DialogResult:
        self.__dialog.setModal(True)
        self.__dialog.exec()

        return self._result

    def _close(self) -> None:
        self.__dialog.done(0)

    def _getConfidenceBand(self) -> float:
        return self._tryConvertToFloat(self.__confidenceBandInput.text())

    def _highlight(self, cells: List[Tuple[int, int]]) -> None:
        if len(cells) == 0:
            return

        print(cells)

        tableWidget: QTableWidget = self._spreadsheetView.getTableWidget()
        tableWidget.selectionModel().clearSelection()

        minRow: int = tableWidget.rowCount() + 1
        minColumn: int = tableWidget.columnCount() + 1
        maxRow: int = -1
        maxColumn: int = -1

        for cell in cells:
            if cell[0] < minRow:
                minRow = cell[0]
            if cell[0] > maxRow:
                maxRow = cell[0]

            if cell[1] < minColumn:
                minColumn = cell[1]
            if cell[1] > maxColumn:
                maxColumn = cell[1]

        selectionRange: QTableWidgetSelectionRange = QTableWidgetSelectionRange(minRow, minColumn, maxRow, maxColumn)
        tableWidget.setRangeSelected(selectionRange, True)

    def _makeChooseFileDialog(self) -> ChooseFileDialog:
        return QtChooseFileDialog(self.__dialog)

    def _makeSpreadsheetView(self) -> SpreadsheetView:
        qtSpreadsheet: QtSpreadsheet = QtSpreadsheet()
        return qtSpreadsheet

    def _showMessage(self, msg: str) -> None:
        QMessageBox.information(self.__dialog, "Error", msg)

    def __handleDataSelectionButton(self, button: QPushButton, coordinate: str) -> None:
        inEditMode: bool = self.__editState[coordinate]
        otherCoordinate: str = self.__getOtherCoordinate(coordinate)
        self.__turnOffEditMode(otherCoordinate)
        if not inEditMode:
            self.__turnOnEditMode(coordinate)
        else:
            self.__turnOffEditMode(coordinate)

    def __turnOnEditMode(self, coordinate: str) -> None:
        self.__editState[coordinate] = True
        button: QPushButton = self.__buttonDict[coordinate]
        button.setText("Confirm Data Selection")
        self._startListeningForDataSelection(coordinate)

    def __turnOffEditMode(self, coordinate: str) -> None:
        self.__editState[coordinate] = False
        button: QPushButton = self.__buttonDict[coordinate]
        button.setText("Select " + coordinate + " values")
        self._stopListeningForDataSelection()

    @staticmethod
    def __getOtherCoordinate(coordinate: str) -> str:
        return "x" if coordinate == "y" else "y"

class QtDialogFactory(DialogFactory):
    """Qt Implementation of DialogFactory. Creates Qt implementations of Dialogs."""

    def __init__(self, parent: QWidget = None):
        self.__parent: QWidget = parent

    def setParent(self, parent: QWidget):
        """Sets the parent widget for created dialogs"""
        self.__parent = parent

    def makeChooseFolderDialog(self) -> ChooseFolderDialog:
        return QtChooseFolderDialog(self.__parent)

    def makeDataChooserDialog(self) -> DataChooserDialog:
        pass
