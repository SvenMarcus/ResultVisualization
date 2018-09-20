from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Artist, Figure
from typing import List

from ResultVisualization.Graph import Graph, PlotConfig


class QtGraph(Graph):

    def __init__(self, parent: QWidget = None):
        self.__widget = QWidget(parent)
        self.__layout: QVBoxLayout = QVBoxLayout(self.__widget)
        self.__widget.setLayout(self.__layout)
        self.__canvas: FigureCanvas = FigureCanvas(Figure())
        self.__navBar: NavigationToolbar = NavigationToolbar(self.__canvas, self.__widget)

        self.__layout.addWidget(self.__navBar)
        self.__layout.addWidget(self.__canvas)

        self.__plots: List[Artist] = list()

    def clear(self):
        self.__canvas.figure.clf()

    def addPlot(self, config: PlotConfig) -> None:
        config.xValues, config.yValues = self.__sortValuesByX(config)
        self.__plotConfidenceBand(config)

        self.__plotData(config)
        self.__canvas.draw_idle()

    def removePlot(self, index: int) -> None:
        line2d = self.__plots.pop(index)
        line2d.remove()
        self.__canvas.draw_idle()

    def getWidget(self) -> QWidget:
        return self.__widget

    def __sortValuesByX(self, config):
        zipped = zip(config.xValues, config.yValues)
        x, y = list(zip(*sorted(zipped)))
        return x, y

    def __plotConfidenceBand(self, config: PlotConfig) -> None:
        if config.confidenceBand > 0:
            y1Values = [y * (1 - config.confidenceBand) for y in config.yValues]
            y2Values = [y * (1 + config.confidenceBand) for y in config.yValues]

            self.__canvas.figure.add_subplot(111).fill_between(config.xValues, y1Values, y2Values, alpha=0.3, edgecolor='#CC4F1B', facecolor='#FF9848')

    def __plotData(self, config: PlotConfig) -> None:
        lines = list()
        lines = self.__canvas.figure.add_subplot(111).plot(config.xValues, config.yValues, label=config.title)
        self.__plots.append(lines[0])
