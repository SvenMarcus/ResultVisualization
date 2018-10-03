import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from QtResultVisualization.Dialogs import QtLineSeriesDialogFactory
from QtResultVisualization.QtGraphView import QtGraphView


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setApplicationName("Simple Graphs")
    window = QtGraphView(QtLineSeriesDialogFactory()).getWindow()
    window.show()
    sys.exit(app.exec_())

# from QtResultVisualization.QtGraph import QtGraph
# from ResultVisualization.plot import LineSeries
# from ResultVisualization.Filter import RowMetaDataContainsFilter, ExactMetaDataMatchesInAllSeriesFilter

# app = QApplication([])

# graph = QtGraph()
# widget = graph.getWidget()

# series = LineSeries()
# series.xValues = [1, 2, 3, 4, 5]
# series.yValues = [3, 4, 6, 8, 15]
# series.metaData = ["a", "a_b", "b", "d", "fb"]

# series2 = LineSeries()
# series2.metaData = ["a", "a_b", "b", "d", "fdb"]

# series3 = LineSeries()
# series3.metaData = ["a", "a_b", "b", "d", "fsb"]

# series.addFilter(ExactMetaDataMatchesInAllSeriesFilter([series, series2, series3]))

# widget.show()
# graph.addPlot(series)

# app.exec_()
