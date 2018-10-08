from abc import ABC, abstractmethod
from typing import Iterable, List

from ResultVisualization.Filter import ListFilter
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
        self._title: str = ""
        self._xLabel: str = ""
        self._yLabel: str = ""
        self._metaData: List[str] = list()
        self._filters: List[ListFilter] = list()

    def addFilter(self, listFilter: ListFilter) -> None:
        self._filters.append(listFilter)

    def removeFilter(self, listFilter: ListFilter) -> None:
        self._filters.remove(listFilter)

    def clearFilters(self) -> None:
        self._filters.clear()

    @abstractmethod
    def plot(self, plotter: Plotter) -> None:
        raise NotImplementedError()

    @property
    def title(self) -> str:
        """Returns the title of the series."""

        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Sets the title of the series to the given value."""

        self._title = value

    @property
    def xLabel(self) -> str:
        return self._xLabel

    @xLabel.setter
    def xLabel(self, value: str) -> None:
        self._xLabel = value

    @property
    def yLabel(self) -> str:
        return self._yLabel

    @yLabel.setter
    def yLabel(self, value: str) -> None:
        self._yLabel = value

    @property
    def metaData(self) -> List[str]:
        """Returns a list with meta data for the plot."""

        return self._metaData

    @metaData.setter
    def metaData(self, value: List[str]) -> None:
        self._metaData = value

    @property
    def filters(self) -> List[ListFilter]:
        return self._filters

    @filters.setter
    def filters(self, value: List[ListFilter]) -> None:
        self._filters = value


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
        super().__init__()
        self.__title: str = ""
        self.__xLabel: str = ""
        self.__yLabel: str = ""
        self.__xValues = []
        self.__yValues = []
        self.__xLimits = ()
        self.__yLimits = ()
        self.__confidenceBand: float = 0

        self.__filteredX = list()
        self.__filteredY = list()

    def plot(self, plotter: Plotter) -> None:
        self.__sortValuesByX()
        self.__filterValues()
        self.__plotConfidenceBand(plotter)
        plotter.lineSeries(self.__filteredX, self.__filteredY, xLabel=self._xLabel, yLabel=self._yLabel, title=self._title)

    def __filterValues(self) -> None:
        if len(self._filters) == 0:
            self.__filteredX = self.__xValues
            self.__filteredY = self.__yValues
            return

        self.__filteredX = list()
        self.__filteredY = list()

        for i in range(len(self.metaData)):
            shouldAdd: bool = True
            for rowFilter in self._filters:
                shouldAdd = shouldAdd and rowFilter.appliesToIndex(self, i)

            if shouldAdd:
                self.__filteredX.append(self.xValues[i])
                self.__filteredY.append(self.yValues[i])

    def __plotConfidenceBand(self, plotter: Plotter) -> None:
        if self.__confidenceBand > 0:
            lower = [y * (1 - self.__confidenceBand) for y in self.__yValues]
            upper = [y * (1 + self.__confidenceBand) for y in self.__yValues]

            plotter.fillArea(self.__xValues, lower, upper)

    def __sortValuesByX(self) -> None:
        zipped = None
        if len(self.metaData) > 0:
            zipped = zip(self.__xValues, self.__yValues, self.metaData)
            self.__xValues, self.__yValues, self.metaData = list(zip(*sorted(zipped)))
        else:
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
