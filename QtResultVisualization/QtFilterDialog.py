import PyQt5
import PyQt5.Qt as Qt
from PyQt5.QtWidgets import (QDialog, QHBoxLayout, QHeaderView, QLabel,
                             QLineEdit, QPushButton, QTableWidget, QVBoxLayout,
                             QWidget)


class QtRowContainsFilterWidget(QDialog):

    def __init__(self, parent: QWidget = None):
        super(QtRowContainsFilterWidget, self).__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.__textBox: QLineEdit = QLineEdit()
        self.__acceptButton: QPushButton = QPushButton("OK")
        self.__cancelButton: QPushButton = QPushButton("Cancel")

        self.layout().addWidget(QLabel("Filter by content:"))
        self.layout().addWidget(self.__textBox)

        buttonBar: QHBoxLayout = QHBoxLayout()
        self.layout().addLayout(buttonBar)
        buttonBar.addWidget(self.__acceptButton)
        buttonBar.addWidget(self.__cancelButton)

        self.setFixedSize(300, 150)
        self.setModal(True)

    def getText(self) -> str:
        return self.__textBox.text()


class QtFilterWidget:

    def __init__(self, parent: QWidget = None):
        self.__widget: QWidget = QWidget(parent)
        self.__currentFilters: QTableWidget = QTableWidget()
        self.__currentFilters.setColumnCount(1)
        self.__currentFilters.setHorizontalHeaderLabels(["Filters"])
        self.__currentFilters.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.__addFilterButton: QPushButton = QPushButton("Add")
        self.__removeFilterButton: QPushButton = QPushButton("Remove")

        self.__widget.setLayout(QVBoxLayout())

        dialogHeader: QLabel = QLabel("Series Title")
        dialogHeader.setFont(PyQt5.QtGui.QFont("Arial", 16))
        dialogHeader.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.__widget.layout().addWidget(dialogHeader)
        self.__widget.layout().addWidget(self.__currentFilters)
        self.__widget.layout().addWidget(self.__addFilterButton)
        self.__widget.layout().addWidget(self.__removeFilterButton)

    def getWidget(self) -> QWidget:
        return self.__widget


app: Qt.QApplication = Qt.QApplication([])

widget = QtFilterWidget().getWidget()
widget.show()

dialog = QtRowContainsFilterWidget(widget)
dialog.show()

app.exec_()
