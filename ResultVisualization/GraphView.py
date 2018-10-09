from abc import ABC, abstractmethod
from typing import List

from ResultVisualization.CreateFilterDialog import CreateFilterDialog
from ResultVisualization.Dialogs import (DialogResult, SeriesDialog,
                                         SeriesDialogFactory)
from ResultVisualization.EditSeriesFilterDialog import EditSeriesFilterDialog
from ResultVisualization.FilterDialogFactory import FilterDialogFactory
from ResultVisualization.plot import Graph, Series
from ResultVisualization.SeriesRepository import SeriesRepository


class GraphView(ABC):

    def __init__(self, seriesDialogFactory: SeriesDialogFactory, seriesRepository: SeriesRepository, filterDialogFactory: FilterDialogFactory):
        self._graph: Graph = self._makeGraph()
        self.__repository: SeriesRepository = seriesRepository
        self.__series: List[Series] = list(seriesRepository.getSeries())
        self.__seriesDialogFactory: SeriesDialogFactory = seriesDialogFactory
        self.__filterDialogFactory: FilterDialogFactory = filterDialogFactory

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

        dialog: SeriesDialog = self.__seriesDialogFactory.makeSeriesDialog()
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            series: Series = dialog.getSeries()
            self._addEntryToListView(series.title)
            self.__series.append(series)
            self.__repository.addSeries(series)
            self._graph.addPlot(series)

    def _editSeries(self, index: int) -> None:
        """Opens a SeriesDialog with the Series at the given index"""

        series: Series = self.__series[index]
        dialog: SeriesDialog = self.__seriesDialogFactory.makeSeriesDialog(series)
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            series = dialog.getSeries()
            self._graph.updatePlot()
            self._setEntryInListView(index, series.title)

    def _removeSeries(self, index: int) -> None:
        """Removes the series at the given index from the Graph"""

        series: Series = self.__series.pop(index)
        self.__repository.removeSeries(series)
        self._graph.removePlot(series)
        self._removeEntryFromListView(index)

    def _showEditFilterView(self, index: int) -> None:
        """Shows a dialog to configure Filters for a series"""

        series: Series = self.__series[index]
        dialog: EditSeriesFilterDialog = self.__filterDialogFactory.makeEditSeriesFilterDialog(series)
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            self._graph.updatePlot()

    def _showCreateFilterView(self) -> None:
        """Shows a dialog to create new filters"""

        dialog: CreateFilterDialog = self.__filterDialogFactory.makeCreateFilterDialog()
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            self._graph.updatePlot()
