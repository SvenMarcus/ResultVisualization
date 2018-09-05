from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QLabel, QListWidget, \
    QPushButton, QSpacerItem, QVBoxLayout, QWidget


class QtPlotConfig:

    def __init__(self, parent: QWidget = None):
        self.__widget: QWidget = QWidget(parent)
        self.__layout: QVBoxLayout = QVBoxLayout(self.__widget)
        self.__widget.setLayout(self.__layout)
        
        self.__layout.addWidget(QLabel("Plot Type"))

        self.__plotTypeChooser: QComboBox = QComboBox()
        self.__plotTypeChooser.addItem("Line")
        self.__plotTypeChooser.addItem("Box")

        self.__layout.addWidget(self.__plotTypeChooser)
        self.__layout.addWidget(QtLinePlotConfig().getWidget())

    def getWidget(self) -> QWidget:
            return self.__widget


class QtLinePlotConfig:

    def __init__(self, parent: QWidget = None):
        self.__widget: QWidget = QWidget(parent)
        self.__layout: QVBoxLayout = QVBoxLayout(self.__widget)
        self.__widget.setLayout(self.__layout)

        self.__layout.addSpacerItem(QSpacerItem(400, 30))
        self.__layout.addWidget(QLabel("Series"))

        self.__seriesList: QListWidget = QListWidget()
        self.__seriesList.addItem("Hello")
        self.__layout.addWidget(self.__seriesList)

        self.__buttonBar: QHBoxLayout = QHBoxLayout()
        self.__layout.addLayout(self.__buttonBar)

        self.__buttonBar.addWidget(QPushButton("Add Series"))
        self.__buttonBar.addWidget(QPushButton("Remove Series"))
        self.__buttonBar.addWidget(QPushButton("Clear"))

    def getWidget(self) -> QWidget:
        return self.__widget
