from abc import ABC, abstractmethod
from typing import Dict, List

from ResultVisualization.Commands import FilterCommandFactory, UndoableCommand
from ResultVisualization.CommandStack import CommandStack
from ResultVisualization.Events import Event, InvokableEvent
from ResultVisualization.Dialogs import Dialog, DialogResult
from ResultVisualization.Filter import CompositeFilter, ExactMetaDataMatchesInAllSeriesFilter, SeriesFilter, RowMetaDataContainsFilter
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.Plot import FilterableSeries, Series
from ResultVisualization.SeriesRepository import SeriesRepository
from ResultVisualization.TransferWidget import TransferWidget


class FilterCreationView(ABC):
    """Interface for a view that creates a Filter"""

    @property
    @abstractmethod
    def onFilterSaved(self) -> Event:
        """This Event is triggered when the Filter is saved"""

        raise NotImplementedError()

    @abstractmethod
    def getFilter(self) -> SeriesFilter:
        """Returns the Filter created in the view"""

        raise NotImplementedError()


class MetaDataMatchFilterCreationView(FilterCreationView, ABC):
    """An abstract view that creates a ExactMetaDataMatchesInAllSeriesFilter"""

    def __init__(self, seriesRepo: SeriesRepository):
        self.__onSavedEvent: InvokableEvent = InvokableEvent()
        self.__listFilter: SeriesFilter = None
        self._initUI()
        self.__transferWidget: TransferWidget[Series] = self._getTransferWidget()
        self.__transferWidget.setLeftHeader("Selected Series")
        self.__transferWidget.setRightHeader("Available Series")

        filterableSeries: List[FilterableSeries] = list(filter(lambda series: isinstance(series, FilterableSeries), seriesRepo.getSeries()))
        self.__transferWidget.setRightTableItems(filterableSeries)

    def onFilterSaved(self) -> Event:
        return self.__onSavedEvent

    def getFilter(self) -> SeriesFilter:
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
    """An abstract view that create a RowMetaDataContainsFilter"""

    def __init__(self):
        self.__onSavedEvent: InvokableEvent = InvokableEvent()
        self.__listFilter: SeriesFilter = None

    def onFilterSaved(self) -> Event:
        return self.__onSavedEvent

    def getFilter(self) -> SeriesFilter:
        return self.__listFilter

    def _save(self):
        isValid: bool = self.__validate()

        if not isValid:
            self._showMessage("Please enter a title and the required meta data.")
            return

        title: str = self._getTitleFromView()
        requiredMeta: str = self._getRequiredMetaDataFromView()
        inverse: bool = self._getInverseFromView()
        self.__listFilter: RowMetaDataContainsFilter = RowMetaDataContainsFilter(requiredMeta)
        self.__listFilter.title = title
        self.__listFilter.setInverse(inverse)
        self.__onSavedEvent(self)

    @abstractmethod
    def _getTitleFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _getRequiredMetaDataFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _getInverseFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _showMessage(self, message: str) -> None:
        raise NotImplementedError()

    def __validate(self) -> bool:
        return self._getTitleFromView() and self._getRequiredMetaDataFromView()


class CompositeFilterCreationView(FilterCreationView):

    def __init__(self, availableFilters: List[SeriesFilter]):
        self.__onSaveEvent: InvokableEvent = InvokableEvent()
        self.__filters: List[SeriesFilter] = availableFilters

        self._initUI()
        self.__transferWidget: TransferWidget[SeriesFilter] = self._getTransferWidget()
        self.__transferWidget.setLeftHeader("Included Filters")
        self.__transferWidget.setRightHeader("Available Filters")
        self.__transferWidget.setRightTableItems(self.__filters)
        self.__compositeFilter: CompositeFilter = CompositeFilter()

    def onFilterSaved(self) -> Event:
        return self.__onSaveEvent

    def _save(self):
        self.__compositeFilter.title = self._getTitleFromView()
        includedFilters: List[SeriesFilter] = self.__transferWidget.getLeftTableItems()

        for filter in includedFilters:
            self.__compositeFilter.addFilter(filter)

        if not self.__validate():
            return

        self.__onSaveEvent(self)

    def getFilter(self):
        return self.__compositeFilter

    def __validate(self) -> bool:
        if not self.__compositeFilter.title:
            self._showMessage("Please enter a title.")
            return False

        if len(self.__compositeFilter.getFilters()) == 0:
            self._showMessage("Must include at least one filter.")
            return False

        return True

    @abstractmethod
    def _initUI(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _showMessage(self, message: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getTitleFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _getTransferWidget(self) -> TransferWidget[SeriesFilter]:
        raise NotImplementedError()


class CreateFilterDialogSubViewFactory(ABC):
    """An abstract base class for a factory that creates FilterCreationViews"""

    def __init__(self, seriesRepo: SeriesRepository, filterRepo: FilterRepository):
        self._seriesRepo = seriesRepo
        self._filterRepo = filterRepo

    def getSubViewVariantDisplayNameToNameDict(self) -> Dict[str, str]:
        """Returns a dictionary with display names as keys and
        strings that can be used to request new FilterCreationView instances"""

        return {
            "Match meta data in row": "RowContains",
            "Meta Data must be in all series": "ExactMetaMatch",
            "Filter Group": "CompositeFilter"
        }

    @abstractmethod
    def makeView(self, kind: str) -> FilterCreationView:
        """Creates a FilterCreationView based on the provided string"""

        raise NotImplementedError()


class CreateFilterDialog(Dialog, ABC):
    """A dialog that allows the user to configure and save new Filters"""

    def __init__(self, filterRepository: FilterRepository, subViewFactory: CreateFilterDialogSubViewFactory, commandFactory: FilterCommandFactory):
        self.__repository: FilterRepository = filterRepository
        self.__subViewFactory: CreateFilterDialogSubViewFactory = subViewFactory
        self.__commandFactory: FilterCommandFactory = commandFactory
        self._initUI()

        self.__availableFilters: List[SeriesFilter] = list(self.__repository.getFilters())
        self.__commandStack: CommandStack = CommandStack()

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
    def _removeFilterFromAvailableFiltersTable(self, index: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getSelectedFilterIndexFromView(self) -> int:
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

    def _handleFilterRemove(self) -> None:
        selectedIndex: int = self._getSelectedFilterIndexFromView()

        if selectedIndex < 0:
            return

        self._removeFilterFromAvailableFiltersTable(selectedIndex)
        filter: SeriesFilter = self.__availableFilters.pop(selectedIndex)
        cmd: UndoableCommand = self.__commandFactory.makeDeleteFilterCommand(filter)
        self.__commandStack.addCommand(cmd)

    def _confirm(self) -> None:
        self._result = DialogResult.Ok
        self._close()

    def _cancel(self) -> None:
        self._onWindowClosed()
        self._close()

    def _onWindowClosed(self) -> None:
        if self._result == DialogResult.Ok:
            return

        self._result = DialogResult.Cancel
        while self.__commandStack.canUndo():
            self.__commandStack.undo()

    def __handleFilterSaved(self, sender, args) -> None:
        addedFilter: SeriesFilter = self.__currentView.getFilter()
        cmd: UndoableCommand = self.__commandFactory.makeRegisterFilterCommand(addedFilter)
        self.__commandStack.addCommand(cmd)

        self.__availableFilters.append(addedFilter)
        self._addFilterToAvailableFiltersTable(addedFilter.title)
        self._closeSubView(self.__currentView)
