import copy
import os.path
import pickle
from abc import ABC, abstractmethod
from typing import Callable

from ResultVisualization.Dialogs import (ChooseFileDialog, Dialog,
                                         DialogResult, SeriesDialog,
                                         SeriesDialogFactory)
from ResultVisualization.Filter import (ExactMetaDataMatchesInAllSeriesFilter,
                                        FilterVisitor, SeriesFilter,
                                        RowMetaDataContainsFilter)
from ResultVisualization.FilterDialogFactory import FilterDialogFactory
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.FilterUtilities import FilterConnector, FilterDisconnector
from ResultVisualization.GraphView import GraphView
from ResultVisualization.GraphViewFactory import GraphViewFactory
from ResultVisualization.MainWindow import MainWindow
from ResultVisualization.Plot import (BoxSeries, FillAreaSeries,
                                      FilterableSeries, LineSeries, Series, Graph)
from ResultVisualization.PlotSettingsDialog import PlotSettingsDialog
from ResultVisualization.SeriesRepository import SeriesRepository
from ResultVisualization.SeriesVisitor import SeriesVisitor
from ResultVisualization.TemplateCreationDialog import TemplateCreationDialog
from ResultVisualization.TemplateDialogFactory import TemplateDialogFactory
from ResultVisualization.TemplateRepository import TemplateRepository
from ResultVisualization.TextInputDialog import TextInputDialog


class Command(ABC):

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError()


class UndoableCommand(Command, ABC):

    @abstractmethod
    def undo(self) -> None:
        raise NotImplementedError()


class ShowAddSeriesDialogCommand(Command):

    def __init__(self, graphView: GraphView, dialogFactory: SeriesDialogFactory, seriesRepo: SeriesRepository,
                 dialogKind: str):
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

    def visitExactMetaDataMatchesInAllSeries(self, seriesFilter):
        if self.__series in seriesFilter.getSeries():
            seriesFilter.removeSeries(self.__series)

    def visitRowMetaDataContains(self, seriesFilter):
        pass

    def visitCompositeFilter(self, seriesFilter):
        for subFilter in seriesFilter.getFilters():
            subFilter.accept(self)


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

    def __init__(self, listFilter: SeriesFilter, series: FilterableSeries):
        self.__series: FilterableSeries = series
        self.__filter: SeriesFilter = listFilter

    def execute(self) -> None:
        self.__series.addFilter(self.__filter)
        self.__filter.accept(self)

    def visitExactMetaDataMatchesInAllSeries(self, seriesFilter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        seriesFilter.addSeries(self.__series)

    def visitRowMetaDataContains(self, seriesFilter: RowMetaDataContainsFilter) -> None:
        pass

    def visitCompositeFilter(self, seriesFilter):
        for subFilter in seriesFilter.getFilters():
            subFilter.accept(self)


class RemoveFilterFromSeriesCommand(Command, FilterVisitor):

    def __init__(self, listFilter: SeriesFilter, series: FilterableSeries):
        self.__series: FilterableSeries = series
        self.__filter: SeriesFilter = listFilter

    def execute(self) -> None:
        self.__series.removeFilter(self.__filter)
        self.__filter.accept(self)

    def visitExactMetaDataMatchesInAllSeries(self, seriesFilter: ExactMetaDataMatchesInAllSeriesFilter) -> None:
        seriesFilter.removeSeries(self.__series)

    def visitRowMetaDataContains(self, seriesFilter: RowMetaDataContainsFilter) -> None:
        pass

    def visitCompositeFilter(self, seriesFilter):
        for subFilter in seriesFilter.getFilters():
            subFilter.accept(self)


class RegisterFilterCommand(UndoableCommand):

    def __init__(self, listFilter: SeriesFilter, repo: FilterRepository):
        self.__filter: SeriesFilter = listFilter
        self.__repo: FilterRepository = repo
        self.__connector: FilterConnector = FilterConnector()
        self.__disconnector: FilterDisconnector = FilterDisconnector()

    def execute(self) -> None:
        self.__repo.addFilter(self.__filter)
        self.__connector.connect(self.__filter)

    def undo(self) -> None:
        self.__repo.removeFilter(self.__filter)
        self.__disconnector.disconnect(self.__filter)


class DeleteFilterCommand(UndoableCommand):

    def __init__(self, listFilter: SeriesFilter, repo: FilterRepository):
        self.__filter: SeriesFilter = listFilter
        self.__repo: FilterRepository = repo
        self.__connector: FilterConnector = FilterConnector()
        self.__disconnector: FilterDisconnector = FilterDisconnector()

    def execute(self) -> None:
        self.__repo.removeFilter(self.__filter)
        self.__disconnector.disconnect(self.__filter)

    def undo(self) -> None:
        self.__repo.addFilter(self.__filter)
        self.__connector.connect(self.__filter)


class SaveGraphCommand(Command):

    def __init__(self, fileChooser: ChooseFileDialog, graphKind: str, seriesRepo: SeriesRepository,
                 filterRepo: FilterRepository):
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
                return


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

    def execute(self) -> None:
        try:
            file = open(self.__path, 'wb')

            pickle.dump(self.__factory.getTemplateRepository(), file)

            file.close()

        except Exception:
            return


class LoadTemplatesCommand(Command):

    def __init__(self, path: str, factory: GraphViewFactory):
        self.__path: str = path
        self.__factory = factory

    def execute(self) -> None:
        templateRepo = TemplateRepository()

        try:
            file = open(self.__path, 'rb')

            tmpTemplateRepo = pickle.load(file)
            if isinstance(tmpTemplateRepo, TemplateRepository):
                templateRepo = tmpTemplateRepo

            file.close()

        except Exception:
            pass

        self.__factory.setTemplateRepository(templateRepo)


class AddGraphViewCommand(Command):

    def __init__(self, mainWindow: MainWindow, factory: GraphViewFactory, kind: str, textInputDialog: TextInputDialog):
        self.__mainWindow: MainWindow = mainWindow
        self.__factory: GraphViewFactory = factory
        self.__kind: str = kind
        self.__textInputDialog: TextInputDialog = textInputDialog

    def execute(self) -> None:
        result: DialogResult = self.__textInputDialog.show()
        if result is DialogResult.Ok:
            graphView: GraphView = self.__factory.makeGraphView(self.__kind)
            graphView.setTitle(self.__textInputDialog.getText())
            self.__mainWindow.addGraphView(graphView, graphView.getTitle())


class EditGraphViewTitleCommand(Command):

    def __init__(self, mainWindow: MainWindow, textInputDialog: TextInputDialog):
        self.__textInputDialog = textInputDialog
        self.__mainWindow = mainWindow

    def execute(self) -> None:
        result: DialogResult = self.__textInputDialog.show()
        if result is DialogResult.Ok:
            graphView: GraphView = self.__mainWindow.getActiveView()
            graphView.setTitle(self.__textInputDialog.getText())
            graphView.update()


class CloseGraphViewCommand(Command):

    def __init__(self, mainWindow: MainWindow):
        self.__mainWindow: MainWindow = mainWindow

    def execute(self) -> None:
        self.__mainWindow.closeActiveGraphView()


class ShowPlotSettingsDialogCommand(Command):

    def __init__(self, mainWindow: MainWindow, makePlotSettingsDialogFunc: Callable):
        self.__mainWindow = mainWindow
        self.__makeDialog = makePlotSettingsDialogFunc

    def execute(self) -> None:
        graph = self.__mainWindow.getActiveView().getGraph()
        settings = graph.getPlotSettings()
        dialog: PlotSettingsDialog = self.__makeDialog(settings)
        result: DialogResult = dialog.show()
        if result is DialogResult.Ok:
            graph.setPlotSettings(dialog.getPlotSettings())
            graph.enablePlotSettings(True)


class FilterCommandFactory:

    def __init__(self, filterRepo: FilterRepository):
        self.__repo: FilterRepository = filterRepo

    def makeAddFilterToSeriesCommand(self, listFilter: SeriesFilter, series: Series) -> Command:
        return AddFilterToSeriesCommand(listFilter, series)

    def makeRemoveFilterFromSeriesCommand(self, listFilter: SeriesFilter, series: Series) -> Command:
        return RemoveFilterFromSeriesCommand(listFilter, series)

    def makeRegisterFilterCommand(self, listFilter: SeriesFilter) -> UndoableCommand:
        return RegisterFilterCommand(listFilter, self.__repo)

    def makeDeleteFilterCommand(self, listFilter: SeriesFilter) -> UndoableCommand:
        return DeleteFilterCommand(listFilter, self.__repo)
