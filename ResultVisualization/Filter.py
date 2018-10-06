from abc import abstractmethod
from typing import List


class RowFilter:

    def __init__(self):
        self.__title: str = ""

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        self.__title = value

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

    def addSeries(self, series) -> None:
        self.__seriesList.append(series)

    def removeSeries(self, series) -> None:
        self.__seriesList.remove(series)

    def appliesToRow(self, sourceSeries, row: int) -> bool:
        value: str = sourceSeries.metaData[row]

        for series in self.__seriesList:
            if sourceSeries is series:
                continue

            if value not in series.metaData:
                return False

        return True
