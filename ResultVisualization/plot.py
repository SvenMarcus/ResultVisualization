from abc import ABC, abstractmethod
from typing import Iterable, List

from ResultVisualization.util import isNumber


class NonNumberInPlotConfigError(RuntimeError):

    def __init__(self, **kwargs):
        RuntimeError.__init__(self, kwargs)


class Plotter(ABC):

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def lineSeries(self, xValues: Iterable, yValues: Iterable, **kwargs) -> None:
        raise NotImplementedError()

    @abstractmethod
    def fillArea(self, xValues: Iterable, lowerYValues: Iterable, upperYValues: Iterable) -> None:
        raise NotImplementedError()

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError()


class Series(ABC):

    def __init__(self):
        self.__title: str = ""
        self.__xLabel: str = ""
        self.__yLabel: str = ""


    @abstractmethod
    def plot(self, plotter: Plotter) -> None:
        raise NotImplementedError()

    @property
    def title(self) -> str:
        """Returns the title of the series."""

        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        """Sets the title of the series to the given value."""

        self.__title = value

    @property
    def xLabel(self) -> str:
        return self.__xLabel

    @xLabel.setter
    def xLabel(self, value: str) -> None:
        self.__xLabel = value

    @property
    def yLabel(self) -> str:
        return self.__yLabel

    @yLabel.setter
    def yLabel(self, value: str) -> None:
        self.__yLabel = value


class Graph(ABC):

    def __init__(self, plotter: Plotter = None):
        self.__plotter: Plotter = plotter
        self.__series: List[Series] = list()

    def addPlot(self, series: Series) -> None:
        self.__series.append(series)
        series.plot(self.__plotter)
        self.__plotter.update()

    def removePlot(self, series: Series) -> None:
        self.__series.remove(series)
        self.updatePlot()

    def updatePlot(self) -> None:
        self.__plotter.clear()
        for series in self.__series:
            series.plot(self.__plotter)
        self.__plotter.update()


class LineSeries(Series):

    def __init__(self):
        self.__title: str = ""
        self.__xLabel: str = ""
        self.__yLabel: str = ""
        self.__xValues = []
        self.__yValues = []
        self.__xLimits = ()
        self.__yLimits = ()
        self.__confidenceBand: float = 0

    def plot(self, plotter: Plotter) -> None:
        print(self.__xValues, self.yValues, sep="\n")
        self.__sortValuesByX()
        self.__plotConfidenceBand(plotter)
        plotter.lineSeries(self.__xValues, self.__yValues)

    def __plotConfidenceBand(self, plotter: Plotter) -> None:
        if self.__confidenceBand > 0:
            lower = [y * (1 - self.__confidenceBand) for y in self.__yValues]
            upper = [y * (1 + self.__confidenceBand) for y in self.__yValues]

            plotter.fillArea(self.__xValues, lower, upper)

    def __sortValuesByX(self) -> None:
        zipped = zip(self.__xValues, self.__yValues)
        self.__xValues, self.__yValues = list(zip(*sorted(zipped)))

    @property
    def xValues(self) -> list:
        """Returns the x values for the series."""

        return self.__xValues

    @xValues.setter
    def xValues(self, value: list) -> None:
        """Sets the x values for the series."""

        self.__assertAllEntriesAreNumbers(value)
        self.__xValues = value

    @property
    def yValues(self) -> list:
        """Returns the y values for the series."""

        return self.__yValues

    @yValues.setter
    def yValues(self, value: list) -> None:
        """Sets the y values for the series."""

        self.__assertAllEntriesAreNumbers(value)
        self.__yValues = value

    @property
    def xLimits(self) -> tuple:
        return self.__xLimits

    @xLimits.setter
    def xLimits(self, value: tuple) -> None:
        self.__assertAllEntriesAreNumbers(value)
        self.__xLimits = value

    @property
    def yLimits(self) -> tuple:
        return self.__yLimits

    @yLimits.setter
    def yLimits(self, value: tuple) -> None:
        self.__assertAllEntriesAreNumbers(value)
        self.__yLimits = value

    @property
    def confidenceBand(self) -> float:
        """Returns the confidence band value for the series. Percentage based on y values."""

        return self.__confidenceBand

    @confidenceBand.setter
    def confidenceBand(self, value: float) -> None:
        """Sets the confidence band value for the series. Percentage based on y values."""

        self.__confidenceBand = value

    def __assertAllEntriesAreNumbers(self, collection: Iterable):
        for item in collection:
            if not isNumber(item):
                raise NonNumberInPlotConfigError()
