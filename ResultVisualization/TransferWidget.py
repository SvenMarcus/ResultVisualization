from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from ResultVisualization.Titled import Titled

T = TypeVar('T')

class TransferWidget(Generic[T], ABC):

    def __init__(self):
        self.__leftTable: List[T] = list()
        self.__rightTable: List[T] = list()
        self._initUI()

    def setLeftTableItems(self, items: List[T]) -> None:
        self.__leftTable = list(items)
        for item in self.__leftTable:
            self._addToLeftTable(item.title)

    def setRightTableItems(self, items: List[T]) -> None:
        self.__rightTable = list(items)
        for item in self.__rightTable:
            self._addToRightTable(item.title)

    def getLeftTableItems(self) -> List[T]:
        return list(self.__leftTable)

    def getRightTableItems(self) -> List[T]:
        return list(self.__rightTable)

    @abstractmethod
    def setLeftHeader(self, header: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def setRightHeader(self, header: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _initUI(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _addToLeftTable(self, filterName: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _addToRightTable(self, filterName: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _removeFromLeftTable(self, index: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _removeFromRightTable(self, index: int) -> None:
        raise NotImplementedError()

    def _moveItemsToLeftTable(self, indexes: List[int]) -> None:
        movedFilters = list()
        for index in sorted(indexes, reverse=True):
            filterToMove: T = self.__rightTable[index]
            movedFilters.append(filterToMove)
            self.__leftTable.append(filterToMove)

            self._removeFromRightTable(index)
            self._addToLeftTable(filterToMove.title)

        for listFilter in movedFilters:
            self.__rightTable.remove(listFilter)

    def _moveItemsToRightTable(self, indexes: List[int]) -> None:
        movedFilters = list()
        for index in sorted(indexes, reverse=True):
            filterToMove: T = self.__leftTable[index]
            movedFilters.append(filterToMove)
            self.__rightTable.append(filterToMove)

            self._removeFromLeftTable(index)
            self._addToRightTable(filterToMove.title)

        for listFilter in movedFilters:
            self.__leftTable.remove(listFilter)

    def __addInitialFilters(self, filterRepo, series):
        for listFilter in filterRepo.getFilters():
            if listFilter in series.filters:
                self.__leftTable.append(listFilter)
                self._addToLeftTable(listFilter.title)
            else:
                self.__rightTable.append(listFilter)
                self._addToRightTable(listFilter.title)
