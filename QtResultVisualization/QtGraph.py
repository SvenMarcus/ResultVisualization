from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Artist, Figure, Axes
from typing import List, Dict

from ResultVisualization.Graph import Graph, PlotConfig


class DuplicatePlotConfigError(RuntimeError):

    def __init__(self):
        super().__init__()


class QtGraph(Graph):

    def __init__(self, parent: QWidget = None):
        self.__widget: QWidget = None
        self.__canvas: FigureCanvas = None

        self.__plots: List[Artist] = list()
        self.__plotConfigs: Dict[PlotConfig, List[Artist]] = {}
        self.__axes: Axes = None

        self.__initUI(parent)

    def __initUI(self, parent: QWidget) -> None:
        self.__widget = QWidget(parent)
        self.__canvas = FigureCanvas(Figure())
        navBar = NavigationToolbar(self.__canvas, self.__widget)

        layout: QVBoxLayout = QVBoxLayout(self.__widget)
        self.__widget.setLayout(layout)

        layout.addWidget(navBar)
        layout.addWidget(self.__canvas)

    def clear(self):
        self.__canvas.figure.clf()

    def addPlot(self, config: PlotConfig) -> None:
        if config in self.__plotConfigs.keys():
            raise DuplicatePlotConfigError()

        self.__plotConfigs[config] = list()

        if self.__axes is None:
            self.__axes = self.__canvas.figure.add_subplot(111)

        self.__axes.set_xlabel(config.xLabel)
        self.__axes.set_ylabel(config.yLabel)
        self.__axes.autoscale()

        self.__plotConfigData(config)

    def __plotConfigData(self, config: PlotConfig) -> None:
        config.xValues, config.yValues = self.__sortValuesByX(config)
        self.__plotConfidenceBand(config)
        self.__plotData(config)
        self.__canvas.draw_idle()

    def updatePlot(self, config: PlotConfig):
        if config not in self.__plotConfigs.keys():
            return

        self.__clearArtistsForConfig(config)
        self.__plotConfigData(config)

    def removePlot(self, config: PlotConfig) -> None:
        if config not in self.__plotConfigs.keys():
            return

        self.__clearArtistsForConfig(config)
        self.__plotConfigs.pop(config)
        self.__canvas.draw_idle()

    def __clearArtistsForConfig(self, config):
        for artist in self.__plotConfigs[config]:
            artist.remove()
        self.__plotConfigs[config].clear()

    def getWidget(self) -> QWidget:
        return self.__widget

    def __plotConfidenceBand(self, config: PlotConfig) -> None:
        if config.confidenceBand > 0:
            y1Values = [y * (1 - config.confidenceBand) for y in config.yValues]
            y2Values = [y * (1 + config.confidenceBand) for y in config.yValues]

            artist: Artist = self.__axes.fill_between(config.xValues, y1Values, y2Values, alpha=0.3)
            self.__plotConfigs[config].append(artist)

    def __plotData(self, config: PlotConfig) -> None:
        artistList = self.__axes.plot(config.xValues, config.yValues, label=config.title)
        self.__plotConfigs[config].append(artistList[0])
        self.__plots.append(artistList[0])

    @staticmethod
    def __sortValuesByX(config):
        zipped = zip(config.xValues, config.yValues)
        x, y = list(zip(*sorted(zipped)))
        return x, y