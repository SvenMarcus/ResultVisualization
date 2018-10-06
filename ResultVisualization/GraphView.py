from abc import ABC, abstractmethod
from typing import List

from ResultVisualization.Dialogs import (DialogResult, SeriesDialog,
                                         SeriesDialogFactory)
from ResultVisualization.plot import Graph, Series


class GraphView(ABC):

    def __init__(self, seriesDialogFactory: SeriesDialogFactory):
        self._graph: Graph = self._makeGraph()
        self.__series: List[Series] = list()
        self.__factory: SeriesDialogFactory = seriesDialogFactory

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

    def _addSeries(self) -> None:
        """Opens a SeriesDialog that allows the user to configure a new line series.
        The series will be added to the Graph and the series ListView"""

        dialog: SeriesDialog = self.__factory.makeSeriesDialog()
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            series: Series = dialog.getSeries()
            self._addEntryToListView(series.title)
            self.__series.append(series)
            self._graph.addPlot(series)

    def _editSeries(self, index: int) -> None:
        """Opens a SeriesDialog with the Series at the given index"""

        series: Series = self.__series[index]
        dialog: SeriesDialog = self.__factory.makeSeriesDialog(series)
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            series = dialog.getSeries()
            self._graph.updatePlot()
            self._setEntryInListView(index, series.title)

    def _removeSeries(self, index: int) -> None:
        """Removes the series at the given index from the Graph"""

        series: Series = self.__series.pop(index)
        self._graph.removePlot(series)
        self._removeEntryFromListView(index)

    def _showFilterView(self, index: int) -> None:
        """Shows a view to configure Filters for a series"""

        series: Series = self.__series[index]
        