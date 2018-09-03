import sys

from PyQt5.QtWidgets import QApplication, QComboBox, QLabel, QVBoxLayout, \
    QWidget


class PlotConfig:

    def __init__(self):
        app: QApplication = QApplication(sys.argv)

        mainWidget: QWidget = QWidget()
        self.layout = QVBoxLayout(mainWidget)

        mainWidget.setLayout(self.layout)

        comboBox: QComboBox = QComboBox()
        comboBox.addItem("Line Plot")
        comboBox.addItem("Box Plot")

        lineLabel = QLabel("Lines!")
        boxLabel = QLabel("Boxes!")

        self.layout.addWidget(comboBox)
        self.layout.addWidget(QLabel("Lines!"))

        self.widgets = ["Lines!", "Boxes!"]

        comboBox.currentIndexChanged.connect(self.addWidget)

        mainWidget.show()

        sys.exit(app.exec())

    def addWidget(self, i):
        self.layout.takeAt(1).widget().deleteLater()
        self.layout.addWidget(QLabel(self.widgets[i]))


PlotConfig()
