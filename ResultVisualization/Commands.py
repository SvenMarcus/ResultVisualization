import copy
import os.path
import pickle
from abc import ABC, abstractmethod

from ResultVisualization.Dialogs import (ChooseFileDialog, Dialog,
                                         DialogResult, SeriesDialog,
                                         SeriesDialogFactory)
from ResultVisualization.Filter import (ExactMetaDataMatchesInAllSeriesFilter,
                                        FilterVisitor, ListFilter,
                                        RowMetaDataContainsFilter)
from ResultVisualization.FilterDialogFactory import FilterDialogFactory
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.GraphView import GraphView
from ResultVisualization.GraphViewFactory import GraphViewFactory
from ResultVisualization.LoadFromTemplateDialog import LoadFromTemplateDialog
from ResultVisualization.MainWindow import MainWindow
from ResultVisualization.Plot import (BoxSeries, FillAreaSeries,
                                      FilterableSeries, LineSeries, Series)
from ResultVisualization.SeriesRepository import SeriesRepository
from ResultVisualization.SeriesVisitor import SeriesVisitor
from ResultVisualization.TemplateCreationDialog import TemplateCreationDialog
from ResultVisualization.TemplateDialogFactory import TemplateDialogFactory
from ResultVisualization.TemplateRepository import TemplateRepository


class Command(ABC):

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError()


class ShowAddSeriesDialogCommand(Command):

    def __init__(self, graphView: GraphView, dialogFactory: SeriesDialogFactory, seriesRepo: SeriesRepository, dialogKind: str):
        self.__graphView: GraphView = graphView
        self.__seriesDialogFactory: SeriesDialogFactory = dialogFactory
        self.__repository: SeriesRepository = seriesRepo
        self.__kind: str = dialogKind

    def execute(self) -> None:
        dialog: SeriesDialog = self.__seriesDialogFactory.makeSeriesDialog(
            kind=self.__kind)
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            series: Series = dialog.getSeries()
            self.__repository.addSeries(series)
            self.__graphView.addSeries(series)


class ShowEditSeriesDialogCommand(Command):

    def __init__(self, graphView: GraphView, dialogFactory: SeriesDialogFactory):
        self.__graphView: GraphView = graphView
        self.__seriesDialogFactory: SeriesDialogFactory = dialogFactory

    def execute(self) -> None:
        series: Series = self.__graphView.getSelectedSeries()

        if series is None:
            return

        dialog: SeriesDialog = self.__seriesDialogFactory.makeSeriesDialog(
            initialSeries=series)
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            self.__graphView.updateSeries(series)


class RemoveSeriesCommand(Command, FilterVisitor):

    def __init__(self, graphView: GraphView, seriesRepo: SeriesRepository):
        self.__graphView: GraphView = graphView
        self.__repository: SeriesRepository = seriesRepo
        self.__series: Series = None

    def execute(self) -> None:
        self.__series: Series = self.__graphView.getSelectedSeries()

        if self.__series is None:
            return

        self.__repository.removeSeries(self.__series)
        self.__graphView.removeSeries(self.__series)

        if isinstance(self.__series, FilterableSeries):
            for listFilter in self.__series.filters:
                listFilter.accept(self)

    def visitExactMetaDataMatchesInAllSeries(self, filter):
        if self.__series in filter.getSeries():
            filter.removeSeries(self.__series)

    def visitRowMetaDataContains(self, filter):
        pass


class DuplicateSeriesCommand(Command, SeriesVisitor):

    def __init__(self, graphView: GraphView, seriesRepo: SeriesRepository):
        self.__graphView: GraphView = graphView
        self.__repository: SeriesRepository = seriesRepo
        self.__series: Series = None

    def execute(self) -> None:
        series: Series = self.__graphView.getSelectedSeries()

        if series is None:
            return

        series.accept(self)

        if self.__series is None:
            return

        self.__repository.addSeries(self.__series)
        self.__graphView.addSeries(self.__series)

    def visitBoxSeries(self, series: BoxSeries):
        boxSeries: BoxSeries = BoxSeries()
        boxSeries.title = series.title
        boxSeries.xLabel = series.xLabel
        boxSeries.yLabel = series.yLabel
        boxSeries.data = copy.deepcopy(series.data)
        boxSeries.metaData = copy.deepcopy(series.metaData)

        for listFilter in series.filters:
            AddFilterToSeriesCommand(listFilter, boxSeries)

        self.__series = boxSeries

    def visitFillAreaSeries(self, series: FillAreaSeries):
        fillSeries: FillAreaSeries = FillAreaSeries()
        fillSeries.title = series.title
        fillSeries.xLabel = series.xLabel
        fillSeries.yLabel = series.yLabel
        fillSeries.xLimits = copy.deepcopy(series.xLimits)
        fillSeries.yLimits = copy.deepcopy(series.yLimits)
        fillSeries.color = copy.deepcopy(series.color)

        self.__series = fillSeries

    def visitLineSeries(self, series: LineSeries):
        lineSeries: LineSeries = LineSeries()
        lineSeries.title = series.title
        lineSeries.xLabel = series.xLabel
        lineSeries.yLabel = series.yLabel
        lineSeries.xValues = copy.deepcopy(series.xValues)
        lineSeries.yValues = copy.deepcopy(series.yValues)
        lineSeries.metaData = copy.deepcopy(series.metaData)
        lineSeries.confidenceBand = series.confidenceBand
        lineSeries.style = series.style

        for listFilter in series.filters:
            AddFilterToSeriesCommand(listFilter, lineSeries)

        self.__series = lineSeries


class FillAreaCommand(Command):

    def __init__(self, graphView: GraphView, dialogFactory: SeriesDialogFactory):
        self.__graphView: GraphView = graphView
        self.__seriesDialogFactory: SeriesDialogFactory = dialogFactory

    def execute(self) -> None:
        series: Series = self.__graphView.getSelectedSeries()

        if series is None:
            return

        dialog: SeriesDialog = self.__seriesDialogFactory.makeSeriesDialog(
            series)
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            self.__graphView.updateSeries(series)


class ShowEditSeriesFilterDialogCommand(Command):

    def __init__(self, graphView: GraphView, dialogFactory: FilterDialogFactory):
        self.__graphView: GraphView = graphView
        self.__dialogFactory: FilterDialogFactory = dialogFactory

    def execute(self) -> None:
        series: Series = self.__graphView.getSelectedSeries()

        if series is None or not isinstance(series, FilterableSeries):
            return

        dialog: Dialog = self.__dialogFactory.makeEditSeriesFilterDialog(
            series)
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            self.__graphView.update()


class ShowCreateFilterDialogCommand(Command):

    def __init__(self, graphView: GraphView, dialogFactory: FilterDialogFactory):
        self.__graphView: GraphView = graphView
        self.__dialogFactory: FilterDialogFactory = dialogFactory

    def execute(self):
        dialog: Dialog = self.__dialogFactory.makeCreateFilterDialog()
        result: DialogResult = dialog.show()

        if result == DialogResult.Ok:
            self.__graphView.update()


class AddFilterToSeriesCommand(Command, FilterVisitor):

    def __init__(self, listFilter: ListFilter, series: FilterableSeries):
        self.__series: FilterableSeries = series
        self.__filter: ListFilter = listFilter

    def execute(self) -> None:
        self.__series.addFilter(self.__filter)
        self.__filter.accept(self)

    def visitExactMetaDataMatchesInAllSeries(self, filter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        filter.addSeries(self.__series)

    def visitRowMetaDataContains(self, filter: RowMetaDataContainsFilter) -> None:
        pass


class RemoveFilterFromSeriesCommand(Command, FilterVisitor):

    def __init__(self, listFilter: ListFilter, series: FilterableSeries):
        self.__series: FilterableSeries = series
        self.__filter: ListFilter = listFilter

    def execute(self) -> None:
        self.__series.removeFilter(self.__filter)
        self.__filter.accept(self)

    def visitExactMetaDataMatchesInAllSeries(self, filter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        filter.removeSeries(self.__series)

    def visitRowMetaDataContains(self, filter: RowMetaDataContainsFilter) -> None:
        pass


class RegisterFilterCommand(Command, FilterVisitor):

    def __init__(self, listFilter: ListFilter, repo: FilterRepository):
        self.__filter: ListFilter = listFilter
        self.__repo: FilterRepository = repo
        self.__undo: bool = False

    def execute(self) -> None:
        self.__repo.addFilter(self.__filter)
        self.__filter.accept(self)

    def visitRowMetaDataContains(self, listFilter: RowMetaDataContainsFilter) -> None:
        pass

    def visitExactMetaDataMatchesInAllSeries(self, listFilter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        for series in listFilter.getSeries():
            series.addFilter(listFilter)


class DeleteFilterCommand(Command, FilterVisitor):

    def __init__(self, listFilter: ListFilter, repo: FilterRepository):
        self.__filter: ListFilter = listFilter
        self.__repo: FilterRepository = repo
        self.__undo: bool = False

    def execute(self) -> None:
        self.__repo.removeFilter(self.__filter)
        self.__filter.accept(self)

    def visitRowMetaDataContains(self, listFilter: RowMetaDataContainsFilter) -> None:
        pass

    def visitExactMetaDataMatchesInAllSeries(self, listFilter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        for series in listFilter.getSeries():
            series.removeFilter(listFilter)


class SaveGraphCommand(Command):

    def __init__(self, fileChooser: ChooseFileDialog, graphKind: str, seriesRepo: SeriesRepository, filterRepo: FilterRepository):
        self.__kind: str = graphKind
        self.__seriesRepo: SeriesRepository = seriesRepo
        self.__filterRepo: FilterRepository = filterRepo
        self.__fileChooser: ChooseFileDialog = fileChooser

    def execute(self):
        result: DialogResult = self.__fileChooser.show()

        if result == DialogResult.Ok:
            filePath = self.__fileChooser.getSelectedFile()

            try:
                file = open(filePath, 'wb')
                pickle.dump([self.__kind, self.__seriesRepo,
                             self.__filterRepo], file)
                file.close()
            except Exception:
                pass


class LoadGraphCommand(Command):

    def __init__(self, window: MainWindow, graphViewFactory: GraphViewFactory, fileChooser: ChooseFileDialog):
        self.__window: MainWindow = window
        self.__factory: GraphViewFactory = graphViewFactory
        self.__fileChooser: ChooseFileDialog = fileChooser

    def execute(self):
        result: DialogResult = self.__fileChooser.show()

        if result == DialogResult.Ok:
            filePath = self.__fileChooser.getSelectedFile()

            if not os.path.exists(filePath):
                return

            try:
                file = open(filePath, 'rb')
                data = pickle.load(file)
                file.close()

                kind: str = data[0]
                seriesRepo: SeriesRepository = data[1]
                filterRepo: FilterRepository = data[2]
                graphView = self.__factory.makeGraphView(
                    kind, seriesRepo, filterRepo)
                self.__window.addGraphView(
                    graphView, os.path.basename(filePath))

            except Exception:
                pass


class ShowTemplateCreationDialogCommand(Command):

    def __init__(self, dialogFactory: TemplateDialogFactory):
        self.__factory: TemplateDialogFactory = dialogFactory

    def execute(self) -> None:
        dialog: TemplateCreationDialog = self.__factory.makeTemplateCreationDialog()
        dialog.show()


class ShowLoadFromTemplateDialogCommand(Command):

    def __init__(self, dialogFactory: TemplateDialogFactory):
        self.__factory: TemplateDialogFactory = dialogFactory

    def execute(self) -> None:
        dialog: TemplateCreationDialog = self.__factory.makeLoadFromTemplateDialog()
        dialog.show()


class SaveTemplatesCommand(Command):

    def __init__(self, path: str, factory: GraphViewFactory):
        self.__path: str = path
        self.__factory: GraphViewFactory = factory

    def execute(self):
        try:
            file = open(self.__path, 'wb')
            print("Dumping:", self.__factory.getTemplateRepository(), "to", self.__path)
            pickle.dump(self.__factory.getTemplateRepository(), file)
            file.close()
        except Exception:
            pass


class LoadTemplatesCommand(Command):

    def __init__(self, path: str, factory: GraphViewFactory):
        self.__path: str = path
        self.__factory = factory

    def execute(self):
        templateRepo = TemplateRepository()

        if not os.path.exists(self.__path):
            return

        try:
            file = open(self.__path, 'rb')
            tmpTemplateRepo = pickle.load(file)
            print("Loaded Repo:", tmpTemplateRepo)
            if tmpTemplateRepo is not None:
                templateRepo = tmpTemplateRepo

            file.close()
        except Exception:
            pass

        self.__factory.setTemplateRepository(templateRepo)

class FilterCommandFactory:

    def __init__(self, filterRepo: FilterRepository):
        self.__repo: FilterRepository = filterRepo

    def makeAddFilterToSeriesCommand(self, listFilter: ListFilter, series: Series) -> Command:
        return AddFilterToSeriesCommand(listFilter, series)

    def makeRemoveFilterFromSeriesCommand(self, listFilter: ListFilter, series: Series) -> Command:
        return RemoveFilterFromSeriesCommand(listFilter, series)

    def makeRegisterFilterCommand(self, listFilter: ListFilter) -> Command:
        return RegisterFilterCommand(listFilter, self.__repo)

    def makeDeleteFilterCommand(self, listFilter: ListFilter) -> Command:
        return DeleteFilterCommand(listFilter, self.__repo)
