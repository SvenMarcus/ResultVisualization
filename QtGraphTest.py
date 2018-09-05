import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QStyleFactory, QWidget

from QtResultVisualization.QtGraph import QtGraph
from QtResultVisualization.QtPlotConfig import QtPlotConfig
from ResultVisualization.Graph import PlotConfig, PlotType


app: QApplication = QApplication(sys.argv)

app.setAttribute(Qt.AA_EnableHighDpiScaling)
if hasattr(QStyleFactory, 'AA_UseHighDpiPixmaps'):
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)


config: PlotConfig = PlotConfig(plotType=PlotType.Line)
config.xValues = [1, 2, 3, 4, 5, 6, 7, 8]
config.yValues = [1, 2, 3, 4, 5, 6, 7, 8]
config.confidenceBand = 0.1

mainWindow: QWidget = QWidget()
layout: QHBoxLayout = QHBoxLayout()
mainWindow.setLayout(layout)

graph: QtGraph = QtGraph()

plotConfig = QtPlotConfig().getWidget()
plotConfig.setMaximumWidth(400)

layout.addWidget(plotConfig)
layout.addWidget(graph.getWidget())

graph.addPlot(config)

mainWindow.show()

app.exec_()
