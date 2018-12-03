from abc import ABC, abstractmethod
from typing import List, Iterable, Set


class ListFilter(ABC):

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


class RowMetaDataContainsFilter(ListFilter):

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


class ExactMetaDataMatchesInAllSeriesFilter(ListFilter):

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

            meta: int = series.metaData
            if value not in meta and len(meta) > 0:
                return False

        return True

    def accept(self, filterVisitor) -> None:
        filterVisitor.visitExactMetaDataMatchesInAllSeries(self)


class CompositeFilter(ListFilter):

    def __init__(self, filters: Set[ListFilter] = set()):
        self.__filters: Set[ListFilter] = filters

    def addFilter(self, filter: ListFilter) -> None:
        self.__filters.add(filter)

    def removeFilter(self, filter: ListFilter) -> None:
        self.__filters.discard(filter)

    def getFilters(self) -> Set[ListFilter]:
        return set(self.__filters)

    def appliesToIndex(self, sourceSeries, index):
        for filter in self.__filters:
            if not filter.appliesToIndex(sourceSeries, index):
                return False
        return True

    def accept(self, filterVisitor):
        filterVisitor.visitCompositeFilter(self)


class FilterVisitor(ABC):

    @abstractmethod
    def visitRowMetaDataContains(self, filter: RowMetaDataContainsFilter) -> None:
        raise NotImplementedError()

    @abstractmethod
    def visitExactMetaDataMatchesInAllSeries(self, filter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        raise NotImplementedError()

    @abstractmethod
    def visitCompositeFilter(self, filter: CompositeFilter) -> None:
        raise NotImplementedError()
