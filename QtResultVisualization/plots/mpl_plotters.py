from typing import Iterable

from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Axes, Figure

from ResultVisualization.plot import Plotter


class MatplotlibPlotter(Plotter):

    def __init__(self, canvas: FigureCanvas):
        self.__canvas: FigureCanvas = canvas
        self.__figure: Figure = canvas.figure
        self.__axes: Axes = self.__figure.add_subplot(111)

    def clear(self) -> None:
        self.__axes.clear()

    def lineSeries(self, xValues: Iterable, yValues: Iterable, **kwargs) -> None:
        self.__axes.plot(xValues, yValues)

    def fillArea(self, xValues: Iterable, lowerYValues: Iterable, upperYValues: Iterable) -> None:
        self.__axes.fill_between(xValues, lowerYValues, upperYValues)

    def update(self) -> None:
        self.__canvas.draw_idle()
