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
        title: str = ""
        for key, value in kwargs.items():
            if key == "xLabel":
                xLabel: str = self.__axes.get_xlabel()
                xLabel = self.__buildLabel(xLabel, value)
                self.__axes.set_xlabel(xLabel)
            elif key == "yLabel":
                yLabel: str = self.__axes.get_ylabel()
                yLabel = self.__buildLabel(yLabel, value)
                self.__axes.set_ylabel(yLabel)
            elif key == "title":
                title = value

        self.__axes.plot(xValues, yValues, label=title)

    def __buildLabel(self, currentLabel: str, newValue: str) -> str:
        if currentLabel is None:
            currentLabel = ""

        if currentLabel == newValue:
            return currentLabel

        if len(currentLabel) > 0:
            currentLabel += " // "

        return currentLabel + newValue

    def fillArea(self, xValues: Iterable, lowerYValues: Iterable, upperYValues: Iterable) -> None:
        self.__axes.fill_between(xValues, lowerYValues, upperYValues)

    def update(self) -> None:
        self.__canvas.draw_idle()
