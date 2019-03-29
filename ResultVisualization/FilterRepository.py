from typing import Iterable, Set

from ResultVisualization.Filter import SeriesFilter

class FilterRepository:

    def __init__(self):
        self.__filters: Set[SeriesFilter] = set()

    def addFilter(self, filter: SeriesFilter) -> None:
        self.__filters.add(filter)

    def removeFilter(self, filter: SeriesFilter) -> None:
        self.__filters.remove(filter)

    def getFilters(self) -> Iterable[SeriesFilter]:
        return self.__filters
