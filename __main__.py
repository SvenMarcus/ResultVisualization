import sys

from PyQt5.QtWidgets import QApplication

from QtResultVisualization.QtLinearGraphView import QtLinearGraphView

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QtLinearGraphView().getWindow()
    window.show()
    sys.exit(app.exec_())
