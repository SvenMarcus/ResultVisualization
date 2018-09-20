from PyQt5.QtWidgets import QDialog, QFileDialog, QGridLayout, \
    QLabel, QLineEdit, QMessageBox, QPushButton, \
    QWidget
from typing import Dict

from QtResultVisualization.QtSpreadsheet import QtSpreadsheet
from ResultVisualization.Dialogs import ChooseFileDialog, ChooseFolderDialog, \
    DataChooserDialog, DialogFactory, DialogResult, LineSeriesDialog
from ResultVisualization.Spreadsheet import SpreadsheetView


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

        self.__layout.addWidget(QLabel("Title"), 0, 2)
        self.__titleInput = QLineEdit()
        self.__layout.addWidget(self.__titleInput, 1, 2)

        self.__layout.addWidget(QLabel("Confidence Interval:"), 2, 2)

        self.__confidenceBandInput: QLineEdit = QLineEdit()
        self.__layout.addWidget(self.__confidenceBandInput, 3, 2)

        self.__okButton: QPushButton = QPushButton("Ok")
        self.__okButton.clicked.connect(self._confirm)
        self.__okButton.setMinimumWidth(150)
        self.__okButton.setDefault(True)
        self.__cancelButton: QPushButton = QPushButton("Cancel")
        self.__cancelButton.clicked.connect(self.__dialog.close)

        self.__layout.addWidget(self.__okButton, 2, 0)
        self.__layout.addWidget(self.__cancelButton, 2, 1)

        self.__layout.addWidget(
            self._spreadsheetView.getTableWidget(), 3, 0, -1, -1)

        self.__inEditMode: bool = False
        self.__editState: Dict[str, bool] = {"x": False, "y": False}
        self.__buttonDict: Dict[str, QPushButton] = {
            "x": self.__xValuesButton, "y": self.__yValuesButton}
        self.__xValuesButton.clicked.connect(
            lambda: self.__handleDataSelectionButton("x"))
        self.__yValuesButton.clicked.connect(
            lambda: self.__handleDataSelectionButton("y"))

    def show(self) -> DialogResult:
        self.__dialog.setModal(True)
        self.__dialog.exec()

        return self._result

    def _close(self) -> None:
        self.__dialog.done(0)

    def _getConfidenceBand(self) -> float:
        return self._tryConvertToFloat(self.__confidenceBandInput.text())

    def _getTitle(self) -> str:
        return self.__titleInput.text()

    def _makeChooseFileDialog(self) -> ChooseFileDialog:
        return QtChooseFileDialog(self.__dialog)

    def _makeSpreadsheetView(self) -> SpreadsheetView:
        qtSpreadsheet: QtSpreadsheet = QtSpreadsheet()
        return qtSpreadsheet

    def _showMessage(self, msg: str) -> None:
        QMessageBox.information(self.__dialog, "Error", msg)

    def __handleDataSelectionButton(self, coordinate: str) -> None:
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
        self.__setInputWidgetsEnabled(False)
        button.setEnabled(True)
        button.setText("Confirm Selection")
        self._startListeningForDataSelection(coordinate)

    def __turnOffEditMode(self, coordinate: str) -> None:
        self.__editState[coordinate] = False
        button: QPushButton = self.__buttonDict[coordinate]
        self.__setInputWidgetsEnabled(True)
        button.setText("Select " + coordinate + " values")
        self._stopListeningForDataSelection()

    def __setInputWidgetsEnabled(self, value: bool) -> None:
        self.__loadFileButton.setEnabled(value)
        self.__okButton.setEnabled(value)
        self.__cancelButton.setEnabled(value)
        self.__xValuesButton.setEnabled(value)
        self.__yValuesButton.setEnabled(value)
        self.__confidenceBandInput.setEnabled(value)

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
