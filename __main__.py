import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from ResultVisualization.FilterRepository import FilterRepository

from QtResultVisualization.Dialogs import QtLineSeriesDialogFactory
from QtResultVisualization.QtGraphView import QtGraphView
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

# from ResultVisualization.Filter import RowMetaDataContainsFilter
# from ResultVisualization.plot import LineSeries

# from QtResultVisualization.QtFilterDialog import QtFilterWidget
# from QtResultVisualization.QtCreateFilterDialog import QtCreateFilterDialog, QtCreateFilterDialogSubViewFactory

# f1 = RowMetaDataContainsFilter("")
# f1.title = "F1"

# f2 = RowMetaDataContainsFilter("")
# f2.title = "F2"

# f3 = RowMetaDataContainsFilter("")
# f3.title = "F3"

# f4 = RowMetaDataContainsFilter("")
# f4.title = "F4"

# s = LineSeries()
# s.filters.append(f1)

# repo = FilterRepository()
# repo.addFilter(f1)
# repo.addFilter(f2)
# repo.addFilter(f3)
# repo.addFilter(f4)

# factory = QtCreateFilterDialogSubViewFactory()

# app: QApplication = QApplication([])

# # widget = QtFilterWidget(s, repo).getWidget()
# widget = QtCreateFilterDialog(repo, factory, None).getWidget()
# widget.show()

# app.exec_()
