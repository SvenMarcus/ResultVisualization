from abc import abstractmethod
from typing import List


class RowFilter:

    @abstractmethod
    def appliesToRow(self, sourceSeries, row: int) -> bool:
        raise NotImplementedError()


class RowMetaDataContainsFilter(RowFilter):

    def __init__(self, requiredValue: str):
        self.__requiredValue: str = requiredValue

    def appliesToRow(self, sourceSeries, row: int) -> bool:
        return self.__requiredValue in sourceSeries.metaData[row]


class ExactMetaDataMatchesInAllSeriesFilter(RowFilter):

    def __init__(self, seriesList: List):
        self.__seriesList: List = seriesList

    def appliesToRow(self, sourceSeries, row: int) -> bool:
        value: str = sourceSeries.metaData[row]

        for series in self.__seriesList:
            if sourceSeries is series:
                continue

            if value not in series.metaData:
                return False

        return True
