from typing import Dict, List

from PyQt5.QtWidgets import QAbstractItemView, QDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QWidget

from QtResultVisualization.Dialogs import QtChooseFileDialog
from QtResultVisualization.QtSpreadsheet import QtSpreadsheet

from ResultVisualization.BoxSeriesDialog import BoxSeriesDialog
from ResultVisualization.Dialogs import DialogResult, ChooseFileDialog, SeriesDialog, SeriesDialogFactory
from ResultVisualization.Plot import Series
from ResultVisualization.Spreadsheet import Spreadsheet, SpreadsheetView


class QtBoxSeriesDialog(BoxSeriesDialog):

    def __init__(self, series: Series = None, parent: QWidget = None):
        self.__dialog: QDialog = None
        self.__loadFileButton: QPushButton = None
        self.__selectColumnsButton: QPushButton = None
        self.__okButton: QPushButton = None
        self.__cancelButton: QPushButton = None
        self.__titleInput: QLineEdit = None

        self.__initUI(parent)

        super(QtBoxSeriesDialog, self).__init__(series)

        tableWidget: QTableWidget = self._spreadsheetView.getTableWidget()
        tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.__dialog.layout().addWidget(
            self._spreadsheetView.getTableWidget(), 4, 0, -1, -1)

        self.__inEditMode: bool = False

        self.__editState: Dict[str, bool] = {
            "data": False
        }

        self.__buttonTitles: Dict[str, str] = {
            "data": "Select Data Columns"
        }

        self.__buttonDict: Dict[str, QPushButton] = {
            "data": self.__selectColumnsButton
        }

    def __initUI(self, parent: QWidget) -> None:
        self.__dialog = QDialog(parent)
        self.__dialog.setBaseSize(800, 600)

        self.__titleInput = QLineEdit()

        self.__loadFileButton = QPushButton("Load csv file")
        self.__loadFileButton.clicked.connect(self._handleLoadFile)

        self.__selectColumnsButton = QPushButton("Select Data Columns")
        self.__selectColumnsButton.clicked.connect(
            lambda: self.__handleDataSelectionButton())

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
        layout.addWidget(searchColumnHeaderInput, 1, 0, 1, 2)

        layout.addWidget(self.__selectColumnsButton, 2, 0, 1, 2)

        layout.addWidget(QLabel("Title"), 0, 2)
        layout.addWidget(self.__titleInput, 1, 2)

        layout.addWidget(self.__okButton, 3, 0)
        layout.addWidget(self.__cancelButton, 3, 1)

    def getWidget(self) -> QWidget:
        return self.__dialog

    def show(self) -> DialogResult:
        self.__dialog.setModal(True)
        self.__dialog.exec()

        return self._result

    def _close(self) -> None:
        self.__dialog.done(0)

    def _getTitleFromView(self) -> str:
        return self.__titleInput.text()

    def _setTitleInView(self, value: str) -> None:
        self.__titleInput.setText(value)

    def _makeChooseFileDialog(self) -> ChooseFileDialog:
        return QtChooseFileDialog(self.__dialog)

    def _makeSpreadsheetView(self) -> SpreadsheetView:
        qtSpreadsheet: QtSpreadsheet = QtSpreadsheet()
        return qtSpreadsheet

    def _setUnneededInputWidgetsEnabled(self, value: bool) -> None:
        self.__loadFileButton.setEnabled(value)
        self.__okButton.setEnabled(value)
        self.__cancelButton.setEnabled(value)
        self.__loadFileButton.repaint()
        self.__okButton.repaint()
        self.__cancelButton.repaint()
        self.__selectColumnsButton.repaint()

    def _showMessage(self, msg: str) -> None:
        QMessageBox.information(self.__dialog, "Error", msg)

    def _setWindowTitle(self, value: str) -> None:
        self.__dialog.setWindowTitle(value)

    def __handleDataSelectionButton(self) -> None:
        self.__inEditMode: bool = not self.__inEditMode
        self._toggleSelectData()
        if self.__inEditMode:
            self.__selectColumnsButton.setText("Confirm Selection")
        else:
            self.__selectColumnsButton.setText("Select Data Columns")


class QtBoxSeriesDialogFactory(SeriesDialogFactory):

    def makeSeriesDialog(self, initialSeries: Series = None) -> SeriesDialog:
        dialog = QtBoxSeriesDialog(initialSeries)
        dialog.getWidget().setMinimumSize(1000, 800)
        return dialog