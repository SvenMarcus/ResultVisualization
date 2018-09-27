import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from QtResultVisualization.QtGraphView import QtGraphView
from QtResultVisualization.Dialogs import QtLineSeriesDialogFactory

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setApplicationName("Simple Graphs")
    window = QtGraphView(QtLineSeriesDialogFactory()).getWindow()
    window.show()
    sys.exit(app.exec_())
