from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Artist, Figure
from typing import List, Dict

from ResultVisualization.Graph import Graph, PlotConfig


class DuplicatePlotConfigError(RuntimeError):

    def __init__(self):
        super().__init__()


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
        self.__plotConfigs: Dict[PlotConfig, List[Artist]] = {}

    def clear(self):
        self.__canvas.figure.clf()

    def addPlot(self, config: PlotConfig) -> None:
        if config in self.__plotConfigs.keys():
            raise DuplicatePlotConfigError()

        self.__plotConfigs[config] = list()
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
        self.__canvas.draw_idle()

    def __clearArtistsForConfig(self, config):
        for artist in self.__plotConfigs[config]:
            artist.remove()
        self.__plotConfigs[config].clear()

    def getWidget(self) -> QWidget:
        return self.__widget

    @staticmethod
    def __sortValuesByX(config):
        zipped = zip(config.xValues, config.yValues)
        x, y = list(zip(*sorted(zipped)))
        return x, y

    def __plotConfidenceBand(self, config: PlotConfig) -> None:
        if config.confidenceBand > 0:
            y1Values = [y * (1 - config.confidenceBand) for y in config.yValues]
            y2Values = [y * (1 + config.confidenceBand) for y in config.yValues]

            artist: Artist = self.__canvas.figure.add_subplot(111).fill_between(config.xValues, y1Values, y2Values,
                                                                                alpha=0.3)
            self.__plotConfigs[config].append(artist)

    def __plotData(self, config: PlotConfig) -> None:
        artistList = self.__canvas.figure.add_subplot(111).plot(config.xValues, config.yValues, label=config.title)
        self.__plotConfigs[config].append(artistList[0])
        self.__plots.append(artistList[0])
