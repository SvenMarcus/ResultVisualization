from abc import ABC, abstractmethod
from typing import Dict, List

from ResultVisualization.Commands import FilterCommandFactory, Command
from ResultVisualization.Events import Event, InvokableEvent
from ResultVisualization.Dialogs import Dialog, DialogResult
from ResultVisualization.Filter import ExactMetaDataMatchesInAllSeriesFilter, ListFilter, RowMetaDataContainsFilter
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.Plot import Series
from ResultVisualization.SeriesRepository import SeriesRepository
from ResultVisualization.TransferWidget import TransferWidget


class FilterCreationView(ABC):

    @property
    @abstractmethod
    def onFilterSaved(self) -> Event:
        raise NotImplementedError()

    @abstractmethod
    def getFilter(self) -> ListFilter:
        raise NotImplementedError()


class MetaDataMatchFilterCreationView(FilterCreationView, ABC):

    def __init__(self, seriesRepo: SeriesRepository):
        self.__onSavedEvent: InvokableEvent = InvokableEvent()
        self.__listFilter: ListFilter = None
        self._initUI()
        self.__transferWidget: TransferWidget[Series] = self._getTransferWidget()
        self.__transferWidget.setLeftHeader("Selected Series")
        self.__transferWidget.setRightHeader("Available Series")
        self.__transferWidget.setRightTableItems(seriesRepo.getSeries())

    def onFilterSaved(self) -> Event:
        return self.__onSavedEvent

    def getFilter(self) -> ListFilter:
        return self.__listFilter

    def _save(self) -> None:
        title: str = self._getTitleFromView()
        if not title:
            self._showMessage("Please enter a title.")
            return

        selectedSeries: List[Series] = self.__transferWidget.getLeftTableItems()
        self.__listFilter = ExactMetaDataMatchesInAllSeriesFilter(selectedSeries)
        self.__listFilter.title = self._getTitleFromView()
        self.__onSavedEvent(self)

    @abstractmethod
    def _initUI(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getTransferWidget(self) -> TransferWidget[Series]:
        raise NotImplementedError()

    @abstractmethod
    def _getTitleFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _showMessage(self, message: str) -> None:
        raise NotImplementedError()


class RowContainsFilterCreationView(FilterCreationView, ABC):

    def __init__(self):
        self.__onSavedEvent: InvokableEvent = InvokableEvent()
        self.__listFilter: ListFilter = None

    def onFilterSaved(self) -> Event:
        return self.__onSavedEvent

    def getFilter(self) -> ListFilter:
        return self.__listFilter

    def _save(self):
        isValid: bool = self.__validate()

        if not isValid:
            self._showMessage("Please enter a title and the required meta data.")
            return

        title: str = self._getTitleFromView()
        requiredMeta: str = self._getRequiredMetaDataFromView()
        self.__listFilter: RowMetaDataContainsFilter = RowMetaDataContainsFilter(requiredMeta)
        self.__listFilter.title = title
        self.__onSavedEvent(self)

    @abstractmethod
    def _getTitleFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _getRequiredMetaDataFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _showMessage(self, message: str) -> None:
        raise NotImplementedError()

    def __validate(self) -> bool:
        return self._getTitleFromView() and self._getRequiredMetaDataFromView()


class CreateFilterDialogSubViewFactory(ABC):

    def __init__(self, seriesRepo: SeriesRepository):
        self._seriesRepo = seriesRepo

    def getSubViewVariantDisplayNameToNameDict(self) -> Dict[str, str]:
        return {
            "Match meta data in row": "RowContains",
            "Meta Data must be in all series": "ExactMetaMatch"
        }

    @abstractmethod
    def makeView(self, kind: str) -> FilterCreationView:
        raise NotImplementedError()


class CreateFilterDialog(Dialog, ABC):

    def __init__(self, filterRepository: FilterRepository, subViewFactory: CreateFilterDialogSubViewFactory, commandFactory: FilterCommandFactory):
        self.__repository: FilterRepository = filterRepository
        self.__subViewFactory: CreateFilterDialogSubViewFactory = subViewFactory
        self.__commandFactory: FilterCommandFactory = commandFactory
        self._initUI()

        self.__availableFilters: List[ListFilter] = list(self.__repository.getFilters())
        self.__addedFilters: List[ListFilter] = list()
        self.__commands: List[Command] = list()

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

        self._result: DialogResult = DialogResult.Cancel

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
    def _closeSubView(self, view: FilterCreationView) -> None:
        raise NotImplementedError

    @abstractmethod
    def _close(self) -> None:
        raise NotImplementedError()

    def _handleFilterOptionSelection(self, filterOption: str) -> None:
        subViewName: str = self.__variantDict[filterOption]
        self.__currentView = self.__subViewFactory.makeView(subViewName)
        self.__currentView.onFilterSaved().append(self.__handleFilterSaved)

        self._showSubView(self.__currentView)

    def _confirm(self) -> None:
        for cmd in self.__commands:
            cmd.execute()

        self._result = DialogResult.Ok
        self._close()

    def __handleFilterSaved(self, sender, args) -> None:
        addedFilter: ListFilter = self.__currentView.getFilter()
        self.__addedFilters.append(addedFilter)
        cmd: Command = self.__commandFactory.makeRegisterFilterCommand(addedFilter)
        self.__commands.append(cmd)
        self.__availableFilters.append(addedFilter)
        self._addFilterToAvailableFiltersTable(addedFilter.title)
        self._closeSubView(self.__currentView)
