import uuid
from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable
from uuid import UUID

from ResultVisualization.util import isNumber


class PlotType(Enum):
    Line: int = 0
    Scatter: int = 1
    Box: int = 2


class NonNumberInPlotConfigError(RuntimeError):

    def __init__(self, **kwargs):
        RuntimeError.__init__(self, kwargs)


class PlotConfig:
    """A data class containing data for plot configuration"""

    def __init__(self, plotType: PlotType = PlotType.Line):
        self.__title: str = ""
        self.__plotType: PlotType = plotType
        self.__xLabel: str = ""
        self.__yLabel: str = ""
        self.__xValues = []
        self.__yValues = []
        self.__xLimits = ()
        self.__yLimits = ()
        self.__confidenceBand: float = 0

    @property
    def title(self) -> str:
        """Returns the title of the series."""

        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        """Sets the title of the series to the given value."""

        self.__title = value

    @property
    def plotType(self) -> PlotType:
        """Returns the PlotType of the series."""

        return self.__plotType

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


class Graph(ABC):
    """Interface for a Graph capable of plotting data"""

    @abstractmethod
    def clear(self) -> None:
        """Clears the Graph area."""

        raise NotImplementedError()

    @abstractmethod
    def addPlot(self, config: PlotConfig) -> None:
        """Adds a plot to the Graph area."""

        raise NotImplementedError()

    def updatePlot(self, config: PlotConfig):
        """Updates the plot with the given PlotConfig in the graph."""

        raise NotImplementedError()

    @abstractmethod
    def removePlot(self, config: PlotConfig) -> None:
        """Removes the plot at the given index from the Graph area."""

        raise NotImplementedError()
