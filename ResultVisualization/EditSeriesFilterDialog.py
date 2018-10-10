from abc import ABC, abstractmethod
from typing import List

from ResultVisualization.Dialogs import Dialog, DialogResult
from ResultVisualization.Filter import ListFilter
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.plot import Series
from ResultVisualization.TransferWidget import TransferWidget

class EditSeriesFilterDialog(Dialog, ABC):

    def __init__(self, series: Series, filterRepo: FilterRepository):
        self.__series: Series = series
        self.__activeFilters: List[ListFilter] = list()
        self.__availableFilters: List[ListFilter] = list()

        self._result: DialogResult = DialogResult.Cancel

        self._initUI()
        self.__transferWidget: TransferWidget = self._getTransferWidget()
        self.__transferWidget.setLeftHeader("Active Filters")
        self.__transferWidget.setRightHeader("Available Filters")

        self.__addInitialFilters(filterRepo, series)

    @abstractmethod
    def _initUI(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getTransferWidget(self) -> TransferWidget[ListFilter]:
        raise NotImplementedError()

    @abstractmethod
    def _addFilterToActiveFiltersTable(self, filterName: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _addFilterToAvailableFiltersTable(self, filterName: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _removeFilterFromActiveFiltersTable(self, index: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _removeFilterFromAvailableFiltersTable(self, index: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _close(self) -> None:
        raise NotImplementedError()

    def _addToActiveFilters(self, indexes: List[int]) -> None:
        movedFilters = list()
        for index in sorted(indexes, reverse=True):
            filterToMove: ListFilter = self.__availableFilters[index]
            movedFilters.append(filterToMove)
            self.__activeFilters.append(filterToMove)

            self._removeFilterFromAvailableFiltersTable(index)
            self._addFilterToActiveFiltersTable(filterToMove.title)

        for listFilter in movedFilters:
            self.__availableFilters.remove(listFilter)

    def _removeFromActiveFilters(self, indexes: List[int]) -> None:
        movedFilters = list()
        for index in sorted(indexes, reverse=True):
            filterToMove: ListFilter = self.__activeFilters[index]
            movedFilters.append(filterToMove)
            self.__availableFilters.append(filterToMove)

            self._removeFilterFromActiveFiltersTable(index)
            self._addFilterToAvailableFiltersTable(filterToMove.title)

        for listFilter in movedFilters:
            self.__activeFilters.remove(listFilter)

    def _confirm(self) -> None:
        self.__series.clearFilters()
        # for listFilter in self.__activeFilters:
        for listFilter in self.__transferWidget.getLeftTableItems():
            self.__series.addFilter(listFilter)

        self.__result = DialogResult.Ok
        self._close()

    def _cancel(self) -> None:
        self._close()

    def __addInitialFilters(self, filterRepo, series):
        activeFilters = list()
        availableFilters = list()
        for listFilter in filterRepo.getFilters():
            if listFilter in series.filters:
                activeFilters.append(listFilter)
                # self._addFilterToActiveFiltersTable(listFilter.title)
            else:
                availableFilters.append(listFilter)
                # self._addFilterToAvailableFiltersTable(listFilter.title)

        self.__transferWidget.setLeftTableItems(activeFilters)
        self.__transferWidget.setRightTableItems(availableFilters)
