from PyQt5.QtWidgets import QHeaderView, QPushButton, QSplitter, QTableWidget, \
    QVBoxLayout, QWidget


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
