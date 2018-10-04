import PyQt5.Qt as Qt
from PyQt5.QtWidgets import (QHeaderView, QLabel, QLineEdit, QPushButton, QSplitter,
                             QTableWidget, QVBoxLayout, QWidget)


class QtRowContainsFilterWidget(QWidget):

    def __init__(self, parent: QWidget = None):
        super(QtRowContainsFilterWidget, self).__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.__textBox: QLineEdit = QLineEdit()
        self.layout().addWidget(QLabel("Filter by content:"))
        self.layout().addWidget(self.__textBox)


class QtFilterWidget:

    def __init__(self, parent: QWidget = None):
        self.__widget: QSplitter = QSplitter(parent)
        self.__currentFilters: QTableWidget = QTableWidget()
        self.__currentFilters.setColumnCount(1)
        self.__currentFilters.setHorizontalHeaderLabels(["Filters"])
        self.__currentFilters.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.__addFilterButton: QPushButton = QPushButton("Add")
        self.__removeFilterButton: QPushButton = QPushButton("Remove")

        leftWidget: QWidget = QWidget()
        leftWidget.setLayout(QVBoxLayout())

        leftWidget.layout().addWidget(self.__currentFilters)
        leftWidget.layout().addWidget(self.__addFilterButton)
        leftWidget.layout().addWidget(self.__removeFilterButton)

        self.__widget.addWidget(leftWidget)
        self.__widget.addWidget(QtRowContainsFilterWidget())

    def getWidget(self) -> QWidget:
        return self.__widget


app: Qt.QApplication = Qt.QApplication([])

widget = QtFilterWidget().getWidget()
widget.show()

app.exec_()
