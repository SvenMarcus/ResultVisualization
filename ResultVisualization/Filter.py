from abc import ABC, abstractmethod
from typing import List, Iterable, Set


class SeriesFilter(ABC):

    def __init__(self):
        self.__title: str = ""

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        self.__title = value

    @abstractmethod
    def appliesToIndex(self, sourceSeries, index: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def accept(self, filterVisitor) -> None:
        raise NotImplementedError()


class RowMetaDataContainsFilter(SeriesFilter):

    def __init__(self, requiredValue: str):
        self.__requiredValue: str = requiredValue
        self.__inverse: bool = False

    def setInverse(self, value: bool) -> None:
        self.__inverse = value

    def appliesToIndex(self, sourceSeries, index: int) -> bool:
        if not self.__inverse:
            return self.__requiredValue in sourceSeries.metaData[index]
        else:
            return self.__requiredValue not in sourceSeries.metaData[index]

    def accept(self, filterVisitor) -> None:
        filterVisitor.visitRowMetaDataContains(self)


class ExactMetaDataMatchesInAllSeriesFilter(SeriesFilter):

    def __init__(self, seriesList: List = list()):
        self.__seriesList: List = seriesList

    def addSeries(self, series) -> None:
        self.__seriesList.append(series)

    def removeSeries(self, series) -> None:
        self.__seriesList.remove(series)

    def getSeries(self) -> Iterable:
        return iter(self.__seriesList)

    def appliesToIndex(self, sourceSeries, index: int) -> bool:
        value: str = sourceSeries.metaData[index]

        for series in self.__seriesList:
            if sourceSeries is series:
                continue

            meta: List = series.metaData
            if meta and value not in meta:
                return False

        return True

    def accept(self, filterVisitor) -> None:
        filterVisitor.visitExactMetaDataMatchesInAllSeries(self)


class CompositeFilter(SeriesFilter):

    def __init__(self, filters: Set[SeriesFilter] = set()):
        self.__filters: Set[SeriesFilter] = filters

    def addFilter(self, seriesFilter: SeriesFilter) -> None:
        self.__filters.add(seriesFilter)

    def removeFilter(self, seriesFilter: SeriesFilter) -> None:
        self.__filters.discard(seriesFilter)

    def getFilters(self) -> Set[SeriesFilter]:
        return set(self.__filters)

    def appliesToIndex(self, sourceSeries, index):
        for seriesFilter in self.__filters:
            if not seriesFilter.appliesToIndex(sourceSeries, index):
                return False
        return True

    def accept(self, filterVisitor):
        filterVisitor.visitCompositeFilter(self)


class FilterVisitor(ABC):

    @abstractmethod
    def visitRowMetaDataContains(self, seriesFilter: RowMetaDataContainsFilter) -> None:
        raise NotImplementedError()

    @abstractmethod
    def visitExactMetaDataMatchesInAllSeries(self, seriesFilter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        raise NotImplementedError()

    @abstractmethod
    def visitCompositeFilter(self, seriesFilter: CompositeFilter) -> None:
        raise NotImplementedError()
