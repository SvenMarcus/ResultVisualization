from PyQt5.QtWidgets import QWidget

from QtResultVisualization.Dialogs import QtSaveFileDialog
from QtResultVisualization.QtFilterDialogFactory import QtFilterDialogFactory
from QtResultVisualization.QtGraphView import QtGraphView
from QtResultVisualization.QtSeriesDialogFactory import QtSeriesDialogFactory
from QtResultVisualization.QtTemplateDialogFactory import \
    QtTemplateDialogFactory
from ResultVisualization.Commands import (DuplicateSeriesCommand,
                                          RemoveSeriesCommand,
                                          SaveGraphCommand,
                                          ShowAddSeriesDialogCommand,
                                          ShowCreateFilterDialogCommand,
                                          ShowEditSeriesDialogCommand,
                                          ShowEditSeriesFilterDialogCommand,
                                          ShowLoadFromTemplateDialogCommand,
                                          ShowTemplateCreationDialogCommand)
from ResultVisualization.Dialogs import SeriesDialogFactory
from ResultVisualization.FilterDialogFactory import FilterDialogFactory
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.GraphView import GraphView
from ResultVisualization.GraphViewFactory import GraphViewFactory
from ResultVisualization.SeriesRepository import SeriesRepository
from ResultVisualization.TemplateRepository import TemplateRepository


class QtGraphViewFactory(GraphViewFactory):

    def __init__(self, templateRepo: TemplateRepository = None):
        self.__templateRepo: TemplateRepository = None

    def setTemplateRepository(self, templateRepo):
        print("Setting template repo", str(templateRepo))
        self.__templateRepo = templateRepo

    def getTemplateRepository(self) -> TemplateRepository:
        return self.__templateRepo

    def makeGraphView(self, kind: str, seriesRepo=None, filterRepo=None) -> GraphView:
        graphView: QtGraphView = None
        seriesRepo = seriesRepo or SeriesRepository()
        filterRepo = filterRepo or FilterRepository()
        seriesDialogFactory: SeriesDialogFactory = QtSeriesDialogFactory()

        filterDialogFactory: FilterDialogFactory = QtFilterDialogFactory(filterRepo, seriesRepo)

        graphView = QtGraphView(seriesRepo.getSeries())

        if kind == "linear":
            print("Factory Template Repo", self.__templateRepo)
            templateDialogFactory = QtTemplateDialogFactory(self.__templateRepo, graphView, seriesRepo)
            graphView.loadFromTemplate = ShowLoadFromTemplateDialogCommand(templateDialogFactory)
            graphView.createTemplate = ShowTemplateCreationDialogCommand(templateDialogFactory)

        graphView.addSeriesCommand = ShowAddSeriesDialogCommand(graphView, seriesDialogFactory, seriesRepo, kind)
        graphView.editSeriesCommand = ShowEditSeriesDialogCommand(graphView, seriesDialogFactory)
        graphView.removeSeriesCommand = RemoveSeriesCommand(graphView, seriesRepo)
        graphView.duplicateCommand = DuplicateSeriesCommand(graphView, seriesRepo)
        graphView.fillAreaCommand = ShowAddSeriesDialogCommand(graphView, seriesDialogFactory, seriesRepo, "area")
        graphView.editSeriesFilterCommand = ShowEditSeriesFilterDialogCommand(graphView, filterDialogFactory)
        graphView.createFilterCommand = ShowCreateFilterDialogCommand(graphView, filterDialogFactory)

        widget: QWidget = graphView.getWidget()

        graphView.saveCommand = SaveGraphCommand(QtSaveFileDialog(widget), kind, seriesRepo, filterRepo)
        filterDialogFactory.setParent(widget)

        return graphView
