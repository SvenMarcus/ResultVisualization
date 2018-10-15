import PyQt5.QtGui as QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QColorDialog, QDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QWidget

from ResultVisualization.Dialogs import DialogResult
from ResultVisualization.FillAreaDialog import FillAreaDialog
from ResultVisualization.Plot import FillAreaSeries, TextPosition


class QtFillAreaDialog(FillAreaDialog):

    def __init__(self, initialSeries: FillAreaSeries = None, parent: QWidget=None):
        self.__dialog: QDialog = QDialog(parent)
        self.__dialog.setWindowTitle("Fill Area Dialog")
        layout: QGridLayout = QGridLayout(self.__dialog)
        self.__dialog.setLayout(layout)

        self.__titleBox: QLineEdit = QLineEdit()
        self.__textBox: QLineEdit = QLineEdit()

        self.__colorPicker: QPushButton = QPushButton("Pick Fill Color")
        self.__colorPicker.clicked.connect(lambda: self.__onColorPicked("fill"))

        self.__textColorPicker: QPushButton = QPushButton("Pick Text Color")
        self.__textColorPicker.clicked.connect(lambda: self.__onColorPicked("text"))

        self.__gText: QLineEdit = QLineEdit()
        self.__bText: QLineEdit = QLineEdit()
        self.__aText: QLineEdit = QLineEdit()

        self.__left: QRadioButton = QRadioButton()
        self.__topLeft: QRadioButton = QRadioButton()
        self.__topCenter: QRadioButton = QRadioButton()
        self.__topRight: QRadioButton = QRadioButton()
        self.__right: QRadioButton = QRadioButton()
        self.__bottomRight: QRadioButton = QRadioButton()
        self.__bottomCenter: QRadioButton = QRadioButton()
        self.__bottomLeft: QRadioButton = QRadioButton()

        self.__positions = [
            self.__left,
            self.__topLeft,
            self.__topCenter,
            self.__topRight,
            self.__right,
            self.__bottomRight,
            self.__bottomCenter,
            self.__bottomLeft,
        ]

        self.__posLayout: QGridLayout = QGridLayout()
        self.__posLayout.setRowMinimumHeight(0, 15)
        self.__posLayout.setRowMinimumHeight(1, 15)
        self.__posLayout.setRowMinimumHeight(2, 15)

        posLabel = QLabel("Text Position")
        posLabel.setAlignment(Qt.AlignCenter)
        self.__posLayout.addWidget(posLabel, 1, 1, 1, 3)

        self.__posLayout.addWidget(self.__left, 1, 0)

        self.__posLayout.addWidget(self.__topLeft, 0, 0)
        self.__posLayout.addWidget(self.__topCenter, 0, 2)
        self.__posLayout.addWidget(self.__topRight, 0, 4)

        self.__posLayout.addWidget(self.__right, 1, 4)

        self.__posLayout.addWidget(self.__bottomLeft, 2, 0)
        self.__posLayout.addWidget(self.__bottomCenter, 2, 2)
        self.__posLayout.addWidget(self.__bottomRight, 2, 4)

        self.__minXInput: QLineEdit = QLineEdit()
        self.__minXInput.setPlaceholderText("Min X")
        self.__maxXInput: QLineEdit = QLineEdit()
        self.__maxXInput.setPlaceholderText("Max X")

        self.__minYInput: QLineEdit = QLineEdit()
        self.__minYInput.setPlaceholderText("Min Y")
        self.__maxYInput: QLineEdit = QLineEdit()
        self.__maxYInput.setPlaceholderText("Max Y")

        self.__alphaInput: QLineEdit = QLineEdit()
        self.__alphaInput.setPlaceholderText("Alpha")

        self.__okButton: QPushButton = QPushButton("Ok")
        self.__okButton.clicked.connect(self._confirm)

        self.__cancelButton: QPushButton = QPushButton("Cancel")
        self.__cancelButton.clicked.connect(self._close)

        layout.addWidget(QLabel("Title:"), 0, 0)
        layout.addWidget(self.__titleBox, 0, 1, 1, 5)

        layout.addWidget(QLabel("Text:"), 1, 0)
        layout.addWidget(self.__textBox, 1, 1, 1, 5)

        layout.addLayout(self.__posLayout, 2, 0, 2, 2)

        layout.addWidget(QLabel("Min X"), 2, 3)
        layout.addWidget(self.__minXInput, 2, 4)
        layout.addWidget(QLabel("Max X"), 2, 5)
        layout.addWidget(self.__maxXInput, 2, 6)

        layout.addWidget(QLabel("Min Y"), 3, 3)
        layout.addWidget(self.__minYInput, 3, 4)
        layout.addWidget(QLabel("Max Y"), 3, 5)
        layout.addWidget(self.__maxYInput, 3, 6)

        layout.addWidget(QLabel("Alpha"), 4, 3)
        layout.addWidget(self.__alphaInput, 4, 4)

        layout.addWidget(self.__okButton, 5, 0)
        layout.addWidget(self.__cancelButton, 5, 1)

        layout.addWidget(self.__colorPicker, 0, 6)
        layout.addWidget(self.__textColorPicker, 1, 6)

        super(QtFillAreaDialog, self).__init__(initialSeries)

    def getWidget(self) -> QWidget:
        return self.__dialog

    def show(self) -> DialogResult:
        self.__dialog.setModal(True)
        self.__dialog.exec()

        return self._result

    def __onColorPicked(self, kind: str) -> None:
        color = QColorDialog.getColor(parent=self.__dialog)
        if kind == "fill":
            self._setColor((color.redF(), color.greenF(), color.blueF(), color.alphaF()))
        elif kind == "text":
            self._setTextColor((color.redF(), color.greenF(), color.blueF(), color.alphaF()))

    def _close(self) -> None:
        self.__dialog.done(0)

    def _getTitleFromView(self) -> str:
        return self.__titleBox.text()

    def _getTextFromView(self) -> str:
        return self.__textBox.text()

    def _getTextPositionFromView(self) -> TextPosition:
        index = 0
        for pos in self.__positions:
            if pos.isChecked():
                index = self.__positions.index(pos)

        return TextPosition(index)

    def _getMinXFromView(self) -> str:
        return self.__minXInput.text()

    def _getMaxXFromView(self) -> str:
        return self.__maxXInput.text()

    def _getMinYFromView(self) -> str:
        return self.__minYInput.text()

    def _getMaxYFromView(self) -> str:
        return self.__maxYInput.text()

    def _getAlphaFromView(self) -> str:
        return self.__alphaInput.text()

    def _setTitleInView(self, title) -> None:
        self.__titleBox.setText(title)

    def _setTextInView(self, title) -> None:
        self.__textBox.setText(title)

    def _setTextPositionInView(self, pos) -> None:
        self.__positions[pos.value].setChecked(True)

    def _setMinXInView(self, value) -> None:
        self.__minXInput.setText(str(value))

    def _setMaxXInView(self, value) -> None:
        self.__maxXInput.setText(str(value))

    def _setMinYInView(self, value) -> None:
        self.__minYInput.setText(str(value))

    def _setMaxYInView(self, value) -> None:
        self.__maxYInput.setText(str(value))

    def _setAlphaInView(self, value) -> None:
        self.__alphaInput.setText(str(value))
