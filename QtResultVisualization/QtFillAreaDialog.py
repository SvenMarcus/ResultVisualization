from PyQt5.QtWidgets import QDialog, QGridLayout, QLineEdit, QPushButton, QRadioButton, QWidget


class QtFillAreaDialog:

    def __init__(self, parent: QWidget=None):
        self.__dialog: QDialog = QDialog(parent)
        layout: QGridLayout = QGridLayout(self.__dialog)
        self.__dialog.setLayout(layout)

        fillBetweenXRadio: QRadioButton = QRadioButton("Fill between x")
        fillBetweenYRadio: QRadioButton = QRadioButton("Fill between y")
        fillRectangleRadio: QRadioButton = QRadioButton("Fill Rectangle")

        minXInput: QLineEdit = QLineEdit()
        minXInput.setPlaceholderText("Min X")
        maxXInput: QLineEdit = QLineEdit()
        maxXInput.setPlaceholderText("Max X")

        minYInput: QLineEdit = QLineEdit()
        minYInput.setPlaceholderText("Min Y")
        maxYInput: QLineEdit = QLineEdit()
        maxYInput.setPlaceholderText("Max Y")

        okButton: QPushButton = QPushButton("Ok")
        cancelButton: QPushButton = QPushButton("Cancel")

        layout.addWidget(fillBetweenXRadio, 0, 0)
        layout.addWidget(fillBetweenYRadio, 1, 0)
        layout.addWidget(fillRectangleRadio, 2, 0)

        layout.addWidget(minXInput, 0, 1)
        layout.addWidget(maxXInput, 0, 2)

        layout.addWidget(minYInput, 1, 1)
        layout.addWidget(maxYInput, 1, 2)

        layout.addWidget(okButton, 3, 0)
        layout.addWidget(cancelButton, 3, 1)

    def show(self) -> None:
        self.__dialog.setModal(True)
        self.__dialog.show()


from PyQt5.QtWidgets import QApplication, QMainWindow


app = QApplication([])
window = QMainWindow()
window.show()

QtFillAreaDialog(window).show()

app.exec_()