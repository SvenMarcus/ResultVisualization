from PyQt5.QtWidgets import QWidget, QDialog, QGridLayout, QLabel, QLineEdit, QPushButton

from ResultVisualization.Dialogs import DialogResult
from ResultVisualization.Plot import PlotSettings
from ResultVisualization.PlotSettingsDialog import PlotSettingsDialog
from ResultVisualization.util import tryConvertToFloat


class QtPlotSettingsDialog(PlotSettingsDialog):

    def __init__(self, plotSettings: PlotSettings = None, parent: QWidget = None):
        super().__init__(plotSettings)
        self.__widget = QDialog(parent)
        self.__layout: QGridLayout = QGridLayout()
        self.__widget.setLayout(self.__layout)

        self.__layout.addWidget(QLabel("Min X"), 0, 0)
        self.__layout.addWidget(QLabel("Max X"), 1, 0)
        self.__layout.addWidget(QLabel("Min Y"), 2, 0)
        self.__layout.addWidget(QLabel("Max Y"), 3, 0)

        self.__minX: QLineEdit = QLineEdit()
        self.__maxX: QLineEdit = QLineEdit()
        self.__minY: QLineEdit = QLineEdit()
        self.__maxY: QLineEdit = QLineEdit()

        self.__layout.addWidget(self.__minX, 0, 1, 1, 2)
        self.__layout.addWidget(self.__maxX, 1, 1, 1, 2)
        self.__layout.addWidget(self.__minY, 2, 1, 1, 2)
        self.__layout.addWidget(self.__maxY, 3, 1, 1, 2)

        confirmButton: QPushButton = QPushButton("Ok")
        confirmButton.clicked.connect(self._confirm)

        cancelButton: QPushButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self._close)

        self.__layout.addWidget(confirmButton, 4, 1)
        self.__layout.addWidget(cancelButton, 4, 2)

    def _close(self) -> None:
        self.__widget.close()

    def _getMinXFromView(self) -> float:
        return tryConvertToFloat(self.__minX.text()) or 0

    def _getMaxXFromView(self) -> float:
        return tryConvertToFloat(self.__maxX.text()) or 0

    def _getMinYFromView(self) -> float:
        return tryConvertToFloat(self.__minY.text()) or 0

    def _getMaxYFromView(self) -> float:
        return tryConvertToFloat(self.__maxY.text()) or 0

    def show(self) -> DialogResult:
        self._result = DialogResult.Cancel
        self.__widget.exec()
        return self._result
