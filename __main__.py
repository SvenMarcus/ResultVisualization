import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from QtResultVisualization.QtGraphViewFactory import QtGraphViewFactory

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setApplicationName("Simple Graphs")

    factory = QtGraphViewFactory()
    window = factory.makeGraphView("linear").getWindow()
    window.show()
    sys.exit(app.exec_())
