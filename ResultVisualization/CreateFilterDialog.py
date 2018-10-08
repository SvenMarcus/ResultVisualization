from abc import ABC, abstractmethod
from typing import Dict, List

from ResultVisualization.Events import Event, InvokableEvent
from ResultVisualization.Dialogs import Dialog, DialogResult
from ResultVisualization.Filter import ExactMetaDataMatchesInAllSeriesFilter, ListFilter, RowMetaDataContainsFilter
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.plot import Series


class FilterCreationView(ABC):

    @property
    @abstractmethod
    def onFilterSaved(self) -> Event:
        raise NotImplementedError()

    @abstractmethod
    def getFilter(self) -> ListFilter:
        raise NotImplementedError()


# class MetaDataMatchFilterCreationView(ABC, FilterCreationView):

#     def __init__(self, series: List[Series]):
#         self.__onSavedEvent: InvokableEvent = InvokableEvent()
#         self.__listFilter: ListFilter = None

#     def getFilter(self) -> ListFilter:
#         return self.__listFilter

#     def _save(self):
#         pass


class RowContainsFilterCreationView(FilterCreationView, ABC):

    def __init__(self):
        self.__onSavedEvent: InvokableEvent = InvokableEvent()
        self.__listFilter: ListFilter = None

    def onFilterSaved(self) -> Event:
        return self.__onSavedEvent

    def getFilter(self) -> ListFilter:
        return self.__listFilter

    def _save(self):
        title: str = self._getTitleFromView()
        requiredMeta: str = self._getRequiredMetaDataFromView()
        self.__listFilter: RowMetaDataContainsFilter = RowMetaDataContainsFilter(requiredMeta)
        self.__listFilter.title = title

    @abstractmethod
    def _getTitleFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _getRequiredMetaDataFromView(self) -> str:
        raise NotImplementedError()


class CreateFilterDialogSubViewFactory(ABC):

    @abstractmethod
    def getSubViewVariantDisplayNameToNameDict(self) -> Dict[str, str]:
        raise NotImplementedError()

    @abstractmethod
    def makeView(self, kind: str) -> FilterCreationView:
        raise NotImplementedError()


class CreateFilterDialog(Dialog, ABC):

    def __init__(self, filterRepository: FilterRepository, subViewFactory: CreateFilterDialogSubViewFactory):
        self.__repository: FilterRepository = filterRepository
        self.__subViewFactory: CreateFilterDialogSubViewFactory = subViewFactory
        self._initUI()

        self.__availableFilters: List[ListFilter] = list(self.__repository.getFilters())
        self.__addedFilters: List[ListFilter] = list()

        for listFilter in self.__availableFilters:
            self._addFilterToAvailableFiltersTable(listFilter.title)

        self.__currentView: FilterCreationView = None
        self.__variantDict: Dict[str, str] = self.__subViewFactory.getSubViewVariantDisplayNameToNameDict()

        firstOption: str = ""
        for optionName in self.__variantDict:
            if not firstOption:
                firstOption = optionName
            self._addFilterOptionToView(optionName)

        self._handleFilterOptionSelection(firstOption)

        self._result: DialogResult = DialogResult.Ok

    @abstractmethod
    def _initUI(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _addFilterToAvailableFiltersTable(self, filterName: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _addFilterOptionToView(self, optionName: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _showSubView(self, view: FilterCreationView) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _close(self) -> None:
        raise NotImplementedError()

    def _handleFilterOptionSelection(self, filterOption: str) -> None:
        subViewName: str = self.__variantDict[filterOption]
        self.__currentView = self.__subViewFactory.makeView(subViewName)

        self._showSubView(self.__currentView)

    def _confirm(self) -> None:
        for addedFilter in self.__addedFilters:
            self.__repository.addFilter(addedFilter)
        self._close()

    def __handleFilterSaved(self) -> None:
        addedFilter: ListFilter = self.__currentView.getFilter()
        self.__addedFilters.append(addedFilter)
        self.__availableFilters.append(addedFilter)
        self._addFilterToAvailableFiltersTable(addedFilter.title)
