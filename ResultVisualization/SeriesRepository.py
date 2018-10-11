from typing import Iterable, Set

from ResultVisualization.Plot import Series


class SeriesRepository:

    def __init__(self):
        self.__series: Set[Series] = set()

    def addSeries(self, series: Series) -> None:
        self.__series.add(series)

    def removeSeries(self, series: Series) -> None:
        self.__series.remove(series)

    def getSeries(self) -> Iterable[Series]:
        return self.__series
