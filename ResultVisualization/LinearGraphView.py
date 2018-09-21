from abc import ABC, abstractmethod
from typing import List

from ResultVisualization.Dialogs import DialogResult, LineSeriesDialog
from ResultVisualization.Graph import Graph, PlotConfig


class LinearGraphView(ABC):

    def __init__(self):
        self._graph: Graph = self._makeGraph()
        self.__series: List[PlotConfig] = list()

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

    @abstractmethod
    def _makeLineSeriesDialog(self, data: PlotConfig = None) -> LineSeriesDialog:
        """Creates and returns an instance of LineSeriesDialog"""
        raise NotImplementedError()

    def _addSeries(self) -> None:
        """Opens a LineSeriesDialog that allows the user to configure a new line series.
        The series will be added to the Graph and the series ListView"""

        dialog: LineSeriesDialog = self._makeLineSeriesDialog()
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            config: PlotConfig = dialog.getPlotConfig()
            self._addEntryToListView(config.title)
            self.__series.append(config)
            self._graph.addPlot(config)

    def _editSeries(self, index: int) -> None:
        """Opens a LineSeriesDialog with the PlotConfig at the given index"""

        config: PlotConfig = self.__series[index]
        dialog: LineSeriesDialog = self._makeLineSeriesDialog(config)
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            config: PlotConfig = dialog.getPlotConfig()
            self._graph.updatePlot(config)
            self._setEntryInListView(index, config.title)

    def _removeSeries(self, index: int) -> None:
        """Removes the series at the given index from the Graph"""

        config: PlotConfig = self.__series.pop(index)
        self._graph.removePlot(config)
        self._removeEntryFromListView(index)

    @staticmethod
    def __transposePlotConfigData(config: PlotConfig) -> List[List]:
        data: List[List] = [config.xValues, config.yValues]
        return list(map(list, zip(*data)))
