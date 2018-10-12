from abc import ABC, abstractmethod

from ResultVisualization.Filter import FilterVisitor, ListFilter, ExactMetaDataMatchesInAllSeriesFilter, RowMetaDataContainsFilter
from ResultVisualization.Plot import Series

class Command(ABC):

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError()


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

    def visitExactMetaDataMatchesInAllSeries(self, filter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        filter.removeSeries(self.__series)

    def visitRowMetaDataContains(self, filter: RowMetaDataContainsFilter) -> None:
        pass


class FilterCommandFactory:

    def makeAddFilterToSeriesCommand(self, listFilter: ListFilter, series: Series) -> Command:
        return AddFilterToSeriesCommand(listFilter, series)

    def makeRemoveFilterFromSeriesCommand(self, listFilter: ListFilter, series: Series) -> Command:
        return RemoveFilterFromSeriesCommand(listFilter, series)
