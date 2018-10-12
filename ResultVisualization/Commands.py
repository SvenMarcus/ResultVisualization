from abc import ABC, abstractmethod

from ResultVisualization.Dialogs import Dialog, DialogResult, SeriesDialogFactory, SeriesDialog
from ResultVisualization.Filter import FilterVisitor, ListFilter, ExactMetaDataMatchesInAllSeriesFilter, RowMetaDataContainsFilter
from ResultVisualization.FilterDialogFactory import FilterDialogFactory
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.GraphView import GraphView
from ResultVisualization.Plot import Series
from ResultVisualization.SeriesRepository import SeriesRepository

class Command(ABC):

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError()


class ShowAddSeriesDialogCommand(Command):

    def __init__(self, graphView: GraphView, dialogFactory: SeriesDialogFactory, seriesRepo: SeriesRepository):
        self.__graphView: GraphView = graphView
        self.__seriesDialogFactory: SeriesDialogFactory = dialogFactory
        self.__repository: SeriesRepository = seriesRepo

    def execute(self) -> None:
        dialog: SeriesDialog = self.__seriesDialogFactory.makeSeriesDialog()
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            series: Series = dialog.getSeries()
            self.__repository.addSeries(series)
            self.__graphView.addSeries(series)


class ShowEditSeriesDialogCommand(Command):

    def __init__(self, graphView: GraphView, dialogFactory: SeriesDialogFactory):
        self.__graphView: GraphView = graphView
        self.__seriesDialogFactory: SeriesDialogFactory = dialogFactory

    def execute(self) -> None:
        series: Series = self.__graphView.getSelectedSeries()

        if series is None:
            return

        dialog: SeriesDialog = self.__seriesDialogFactory.makeSeriesDialog(series)
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            self.__graphView.updateSeries(series)


class RemoveSeriesCommand(Command):

    def __init__(self, graphView: GraphView, seriesRepo: SeriesRepository):
        self.__graphView: GraphView = graphView
        self.__repository: SeriesRepository = seriesRepo

    def execute(self) -> None:
        series: Series = self.__graphView.getSelectedSeries()

        if series is None:
            return

        self.__repository.removeSeries(series)
        self.__graphView.removeSeries(series)


class ShowEditSeriesFilterDialogCommand(Command):

    def __init__(self, graphView: GraphView, dialogFactory: FilterDialogFactory):
        self.__graphView: GraphView = graphView
        self.__dialogFactory: FilterDialogFactory = dialogFactory

    def execute(self) -> None:
        series: Series = self.__graphView.getSelectedSeries()

        if series is None:
            return

        dialog: Dialog = self.__dialogFactory.makeEditSeriesFilterDialog(series)
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            self.__graphView.update()


class ShowCreateFilterDialogCommand(Command):

    def __init__(self, graphView: GraphView, dialogFactory: FilterDialogFactory):
        self.__graphView: GraphView = graphView
        self.__dialogFactory: FilterDialogFactory = dialogFactory

    def execute(self):
        dialog: Dialog = self.__dialogFactory.makeCreateFilterDialog()
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            self.__graphView.update()


class AddFilterToSeriesCommand(Command, FilterVisitor):

    def __init__(self, listFilter: ListFilter, series: Series):
        self.__series: Series = series
        self.__filter: ListFilter = listFilter

    def execute(self) -> None:
        self.__series.addFilter(self.__filter)
        self.__filter.accept(self)

    def visitExactMetaDataMatchesInAllSeries(self, filter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        filter.addSeries(self.__series)

    def visitRowMetaDataContains(self, filter: RowMetaDataContainsFilter) -> None:
        pass


class RemoveFilterFromSeriesCommand(Command, FilterVisitor):

    def __init__(self, listFilter: ListFilter, series: Series):
        self.__series: Series = series
        self.__filter: ListFilter = listFilter

    def execute(self) -> None:
        self.__series.removeFilter(self.__filter)
        self.__filter.accept(self)

    def visitExactMetaDataMatchesInAllSeries(self, filter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        filter.removeSeries(self.__series)

    def visitRowMetaDataContains(self, filter: RowMetaDataContainsFilter) -> None:
        pass


class RegisterFilterCommand(Command, FilterVisitor):

    def __init__(self, listFilter: ListFilter, repo: FilterRepository):
        self.__filter: ListFilter = listFilter
        self.__repo: FilterRepository = repo
        self.__undo: bool = False

    def execute(self) -> None:
        self.__repo.addFilter(self.__filter)
        self.__filter.accept(self)

    def visitRowMetaDataContains(self, listFilter: RowMetaDataContainsFilter) -> None:
        pass

    def visitExactMetaDataMatchesInAllSeries(self, listFilter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        for series in listFilter.getSeries():
            series.addFilter(listFilter)


class FilterCommandFactory:

    def __init__(self, filterRepo: FilterRepository):
        self.__repo: FilterRepository = filterRepo

    def makeAddFilterToSeriesCommand(self, listFilter: ListFilter, series: Series) -> Command:
        return AddFilterToSeriesCommand(listFilter, series)

    def makeRemoveFilterFromSeriesCommand(self, listFilter: ListFilter, series: Series) -> Command:
        return RemoveFilterFromSeriesCommand(listFilter, series)

    def makeRegisterFilterCommand(self, listFilter: ListFilter) -> Command:
        return RegisterFilterCommand(listFilter, self.__repo)
