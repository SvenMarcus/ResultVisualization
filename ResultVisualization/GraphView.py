from abc import ABC, abstractmethod
from typing import List, Iterable

from ResultVisualization.Action import Action
from ResultVisualization.Plot import Graph, Series


class GraphView(ABC):

    def __init__(self, initialSeries: Iterable[Series]):
        self._graph: Graph = self._makeGraph()
        self.__series: List[Series] = list(initialSeries)

        for series in self.__series:
            self._addEntryToListView(series.title)
            self._graph.addPlot(series)

        self.createTemplate: 'Command' = None
        self.loadFromTemplate: 'Command' = None

        self.__saveCommand: 'Command' = None
        self.__addSeriesCommand: 'Command' = None
        self.__editSeriesCommand: 'Command' = None
        self.__removeSeriesCommand: 'Command' = None
        self.__duplicateCommand: 'Command' = None
        self.__fillAreaCommand: 'Command' = None
        self.__editSeriesFilterCommand: 'Command' = None
        self.__createFilterCommand: 'Command' = None

        self.__actions: List[Action] = list()

    @property
    def actions(self) -> List[Action]:
        return self.__actions

    def addSeries(self, series: Series) -> None:
        """Adds a series to the GraphView"""

        self._addEntryToListView(series.title)
        self.__series.append(series)
        self._graph.addPlot(series)

    def updateSeries(self, series: Series) -> None:
        """Updates a series in the GraphView table and redraws the plot"""

        self._graph.updatePlot()
        index: int = self.__series.index(series)
        self._setEntryInListView(index, series.title)

    def removeSeries(self, series: Series) -> None:
        """Removes a series from the GraphView"""

        index: int = self.__series.index(series)
        self.__series.remove(series)
        self._removeEntryFromListView(index)
        self._graph.removePlot(series)
        self._graph.updatePlot()

    def update(self) -> None:
        """Redraws the plot"""

        self._graph.updatePlot()

    def getSelectedSeries(self) -> Series:
        """Returns the currently selected series"""

        selectedRow: int = self._getSelectedRow()
        if selectedRow > -1:
            return self.__series[selectedRow]

    @property
    def saveCommand(self) -> 'Command':
        return self.__saveCommand

    @saveCommand.setter
    def saveCommand(self, value: 'Command') -> None:
        self.__saveCommand = value

    @property
    def addSeriesCommand(self) -> 'Command':
        return self.__addSeriesCommand

    @addSeriesCommand.setter
    def addSeriesCommand(self, value: 'Command') -> None:
        self.__addSeriesCommand = value

    @property
    def editSeriesCommand(self) -> 'Command':
        return self.__editSeriesCommand

    @editSeriesCommand.setter
    def editSeriesCommand(self, value: 'Command') -> None:
        self.__editSeriesCommand = value

    @property
    def removeSeriesCommand(self) -> 'Command':
        return self.__removeSeriesCommand

    @removeSeriesCommand.setter
    def removeSeriesCommand(self, value: 'Command') -> None:
        self.__removeSeriesCommand = value

    @property
    def fillAreaCommand(self) -> 'Command':
        return self.__fillAreaCommand

    @fillAreaCommand.setter
    def fillAreaCommand(self, value: 'Command') -> None:
        self.__fillAreaCommand = value

    @property
    def duplicateCommand(self) -> 'Command':
        return self.__duplicateCommand

    @duplicateCommand.setter
    def duplicateCommand(self, value: 'Command') -> None:
        self.__duplicateCommand = value

    @property
    def editSeriesFilterCommand(self) -> 'Command':
        return self.__editSeriesFilterCommand

    @editSeriesFilterCommand.setter
    def editSeriesFilterCommand(self, value: 'Command') -> None:
        self.__editSeriesFilterCommand = value

    @property
    def createFilterCommand(self) -> 'Command':
        return self.__createFilterCommand

    @createFilterCommand.setter
    def createFilterCommand(self, value: 'Command') -> None:
        self.__createFilterCommand = value

    @property
    def addSeriesCommand(self) -> 'Command':
        return self.__addSeriesCommand

    @addSeriesCommand.setter
    def addSeriesCommand(self, value: 'Command') -> None:
        self.__addSeriesCommand = value

    @abstractmethod
    def show(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getSelectedRow(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def _addEntryToListView(self, title: str) -> None:
        """Appends the given title entry to the ListView"""
        raise NotImplementedError()

    @abstractmethod
    def _setEntryInListView(self, index: int, value: str) -> None:
        """Sets the entry at the given index to the given value"""
        raise NotImplementedError()

    @abstractmethod
    def _removeEntryFromListView(self, index: int) -> None:
        """Removes the entry at the given index from the ListView"""
        raise NotImplementedError()

    @abstractmethod
    def _makeGraph(self) -> Graph:
        """Creates and returns an instance of Graph"""
        raise NotImplementedError()

