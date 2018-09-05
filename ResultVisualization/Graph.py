from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable

class PlotType(Enum):
    Line: int = 0
    Box: int = 1

class NonNumberInPlotConfigError(RuntimeError):

    def __init__(self, **kwargs):
        RuntimeError.__init__(self, kwargs)

class PlotConfig:

    def __init__(self, plotType: PlotType = PlotType.Line):
        self.__id: str = ""
        self.__plotType: PlotType = plotType
        self.__xValues = []
        self.__yValues = []
        self.__xLimits = ()
        self.__yLimits = ()
        self.__confidenceBand: float = 0

    @property
    def xValues(self) -> list:
        return self.__xValues

    @xValues.setter
    def xValues(self, value: list) -> None:
        self.__assertAllEntriesAreNumbers(value)
        self.__xValues = value

    @property
    def yValues(self) -> list:
        return self.__yValues

    @yValues.setter
    def yValues(self, value: list) -> None:
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
        return self.__confidenceBand

    @confidenceBand.setter
    def confidenceBand(self, value: float) -> None:
        self.__confidenceBand = value

    def __assertAllEntriesAreNumbers(self, collection: Iterable):
        for item in collection:
            if not self.__isNumber(item):
                raise NonNumberInPlotConfigError()

    @staticmethod
    def __isNumber(obj) -> bool:
        return isinstance(obj, (int, float))


class Graph(ABC):
    """Interface for a Graph capable of plotting data"""

    @abstractmethod
    def clear(self) -> None:
        """Clears the Graph area."""

        raise NotImplementedError()

    def addPlot(self, config: PlotConfig) -> None:
        """Adds a plot to the Graph area."""

        raise NotImplementedError()
