from typing import Dict

from PyQt5.QtWidgets import QDialog, QGridLayout, \
    QLabel, QLineEdit, QMessageBox, QPushButton, \
    QWidget

from QtResultVisualization.Dialogs import QtChooseFileDialog
from QtResultVisualization.QtSpreadsheet import QtSpreadsheet

from ResultVisualization.Dialogs import ChooseFileDialog, DialogResult
from ResultVisualization.LineSeriesDialog import LineSeriesDialog
from ResultVisualization.Plot import LineSeries
from ResultVisualization.Spreadsheet import SpreadsheetView
from ResultVisualization.util import tryConvertToFloat


class QtLineSeriesDialog(LineSeriesDialog):
    """Qt implementation of LineSeriesDialog"""

    def __init__(self, series: LineSeries = None, parent: QWidget = None):
        self.__dialog: QDialog = None
        self.__loadFileButton: QPushButton = None
        self.__xValuesButton: QPushButton = None
        self.__yValuesButton: QPushButton = None
        self.__metaColumnButton: QPushButton = None
        self.__okButton: QPushButton = None
        self.__cancelButton: QPushButton = None
        self.__confidenceBandInput: QLineEdit = None
        self.__titleInput: QLineEdit = None
        self.__quickStyleInput: QLineEdit = None

        self.__initUI(parent)

        super(QtLineSeriesDialog, self).__init__(series)

        self.__dialog.layout().addWidget(
            self._spreadsheetView.getTableWidget(), 5, 0, -1, -1)

        self.__editState: Dict[str, bool] = {
            "x": False,
            "y": False,
            "meta": False
        }

        self.__buttonTitles: Dict[str, str] = {
            "x": "Select X values",
            "y": "Select Y values",
            "meta": "Select Meta Column"
        }

        self.__buttonDict: Dict[str, QPushButton] = {
            "x": self.__xValuesButton,
            "y": self.__yValuesButton,
            "meta": self.__metaColumnButton
        }

    def __initUI(self, parent: QWidget) -> None:
        self.__dialog = QDialog(parent)
        self.__dialog.setBaseSize(800, 600)

        self.__titleInput = QLineEdit()
        self.__confidenceBandInput = QLineEdit()
        self.__quickStyleInput = QLineEdit()

        self.__loadFileButton = QPushButton("Load csv file")
        self.__loadFileButton.clicked.connect(self._handleLoadFile)

        self.__xValuesButton = QPushButton("Select x values")
        self.__yValuesButton = QPushButton("Select y values")
        self.__xValuesButton.clicked.connect(
            lambda: self.__handleDataSelectionButton("x"))
        self.__yValuesButton.clicked.connect(
            lambda: self.__handleDataSelectionButton("y"))

        self.__metaColumnButton = QPushButton("Select Meta Column")
        self.__metaColumnButton.clicked.connect(lambda: self.__handleDataSelectionButton("meta"))

        self.__okButton = QPushButton("Ok")
        self.__okButton.clicked.connect(self._confirm)
        self.__okButton.setMinimumWidth(150)
        self.__okButton.setDefault(True)

        self.__cancelButton = QPushButton("Cancel")
        self.__cancelButton.clicked.connect(self.__dialog.close)

        searchColumnHeaderInput: QLineEdit = QLineEdit()
        searchColumnHeaderInput.setPlaceholderText("Search Column Headers...")
        searchColumnHeaderInput.textChanged.connect(self._applyFilter)

        layout: QGridLayout = QGridLayout(self.__dialog)
        self.__dialog.setLayout(layout)

        layout.addWidget(self.__loadFileButton, 0, 0, 1, 2)
        layout.addWidget(self.__metaColumnButton, 1, 0, 1, 2)

        layout.addWidget(self.__xValuesButton, 2, 0)
        layout.addWidget(self.__yValuesButton, 2, 1)

        layout.addWidget(QLabel("Title"), 0, 2)
        layout.addWidget(self.__titleInput, 0, 3)

        layout.addWidget(QLabel("Confidence Interval:"), 1, 2)
        layout.addWidget(self.__confidenceBandInput, 1, 3)

        layout.addWidget(QLabel("Quick Style:"), 2, 2)
        layout.addWidget(self.__quickStyleInput, 2, 3)

        layout.addWidget(searchColumnHeaderInput, 4, 2, 1, 2)

        layout.addWidget(self.__okButton, 4, 0)
        layout.addWidget(self.__cancelButton, 4, 1)

    def getWidget(self) -> QWidget:
        return self.__dialog

    def show(self) -> DialogResult:
        self.__dialog.setModal(True)
        self.__dialog.exec()

        return self._result

    def _close(self) -> None:
        self.__dialog.done(0)

    def _getConfidenceBandFromView(self) -> float:
        return tryConvertToFloat(self.__confidenceBandInput.text())

    def _setConfidenceBandInView(self, value: float) -> None:
        self.__confidenceBandInput.setText(str(value))

    def _getTitleFromView(self) -> str:
        return self.__titleInput.text()

    def _setTitleInView(self, value: str) -> None:
        self.__titleInput.setText(value)

    def _getQuickStyleFromView(self) -> str:
        return self.__quickStyleInput.text()

    def _setQuickStyleInView(self, value: str) -> None:
        self.__quickStyleInput.setText(value)

    def _makeChooseFileDialog(self) -> ChooseFileDialog:
        return QtChooseFileDialog("*.csv", self.__dialog)

    def _makeSpreadsheetView(self) -> SpreadsheetView:
        qtSpreadsheet: QtSpreadsheet = QtSpreadsheet()
        return qtSpreadsheet

    def _showMessage(self, msg: str) -> None:
        QMessageBox.information(self.__dialog, "Error", msg)

    def _setWindowTitle(self, value: str) -> None:
        self.__dialog.setWindowTitle(value)

    def __handleDataSelectionButton(self, coordinate: str) -> None:
        inEditMode: bool = self.__editState[coordinate]
        if not inEditMode:
            self.__turnOnEditMode(coordinate)
        else:
            self.__turnOffEditMode(coordinate)

    def __turnOnEditMode(self, coordinate: str) -> None:
        self.__editState[coordinate] = True
        button: QPushButton = self.__buttonDict[coordinate]
        button.setText("Confirm Selection")
        self._toggleEditMode(coordinate)
        button.setEnabled(True)
        button.repaint()

    def __turnOffEditMode(self, coordinate: str) -> None:
        self.__editState[coordinate] = False
        button: QPushButton = self.__buttonDict[coordinate]
        button.setText(self.__buttonTitles[coordinate])
        self._toggleEditMode(coordinate)

    def _setUnneededInputWidgetsEnabled(self, value: bool) -> None:
        self.__loadFileButton.setEnabled(value)
        self.__okButton.setEnabled(value)
        self.__cancelButton.setEnabled(value)
        self.__xValuesButton.setEnabled(value)
        self.__yValuesButton.setEnabled(value)
        self.__confidenceBandInput.setEnabled(value)
        self.__metaColumnButton.setEnabled(value)
        self.__loadFileButton.repaint()
        self.__okButton.repaint()
        self.__cancelButton.repaint()
        self.__xValuesButton.repaint()
        self.__yValuesButton.repaint()
        self.__confidenceBandInput.repaint()
        self.__metaColumnButton.repaint()
