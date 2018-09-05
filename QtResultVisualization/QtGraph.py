from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

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

    def clear(self):
        self.__canvas.figure.clf()

    def addPlot(self, config: PlotConfig) -> None:
        if config.confidenceBand > 0:
            y1Values = [y * (1 - config.confidenceBand) for y in config.yValues]
            y2Values = [y * (1 + config.confidenceBand) for y in config.yValues]
            
            self.__canvas.figure.add_subplot(111).fill_between(config.xValues, y1Values, y2Values, alpha=0.3, edgecolor='#CC4F1B', facecolor='#FF9848')

        self.__canvas.figure.add_subplot(111).plot(config.xValues, config.yValues)

    def getWidget(self) -> QWidget:
        return self.__widget
