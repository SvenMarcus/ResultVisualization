import sys
from typing import List

from PyQt5.QtWidgets import QApplication, QComboBox, QLabel, QPushButton, \
    QVBoxLayout, QWidget


class PlotConfigFactory:

    def __init__(self):
        self.__availablePlots: List[str] = [
            "Line Plot",
            "Box Plot"
        ]

        self.__configWidgets = [
            QPushButton,
            QComboBox
        ]

        self.__parent: QWidget = None

    def setParent(self, parent: QWidget) -> None: 
        self.__parent = parent

    def makePlotConfigWidget(self, index: int) -> QWidget:
        return self.__configWidgets[index](parent=self.__parent)

class PlotConfig:

    def __init__(self):
        self.__factory = PlotConfigFactory()

        app: QApplication = QApplication(sys.argv)

        mainWidget: QWidget = QWidget()
        self.__factory.setParent(mainWidget)

        self.layout = QVBoxLayout(mainWidget)

        mainWidget.setLayout(self.layout)

        comboBox: QComboBox = QComboBox()
        comboBox.addItem("Line Plot")
        comboBox.addItem("Box Plot")

        lineLabel = QLabel("Lines!")
        boxLabel = QLabel("Boxes!")

        self.layout.addWidget(comboBox)
        self.layout.addWidget(self.__factory.makePlotConfigWidget(0))

        self.widgets = ["Lines!", "Boxes!"]

        comboBox.currentIndexChanged.connect(self.addWidget)

        mainWidget.show()

        sys.exit(app.exec())

    def addWidget(self, i):
        self.layout.takeAt(1).widget().deleteLater()
        self.layout.addWidget(self.__factory.makePlotConfigWidget(i))


PlotConfig()
