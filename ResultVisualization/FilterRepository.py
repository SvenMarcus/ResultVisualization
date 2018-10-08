from typing import Iterable, Set

from ResultVisualization.Filter import ListFilter

class FilterRepository:

    def __init__(self):
        self.__filters: Set[ListFilter] = set()

    def addFilter(self, filter: ListFilter) -> None:
        self.__filters.add(filter)

    def removeFilter(self, filter: ListFilter) -> None:
        self.__filters.remove(filter)

    def getFilters(self) -> Iterable[ListFilter]:
        return self.__filters
