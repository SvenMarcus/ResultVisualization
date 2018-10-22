import sys

from PyQt5.QtWidgets import QWidget

from QtResultVisualization.Dialogs import QtSaveFileDialog
from QtResultVisualization.QtFilterDialogFactory import QtFilterDialogFactory
from QtResultVisualization.QtGraphView import QtGraphView
from QtResultVisualization.QtSeriesDialogFactory import QtSeriesDialogFactory
from QtResultVisualization.QtTemplateDialogFactory import \
    QtTemplateDialogFactory

from ResultVisualization.Action import Action
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
            templateDialogFactory = QtTemplateDialogFactory(self.__templateRepo, graphView, seriesRepo)
            graphView.loadFromTemplate = ShowLoadFromTemplateDialogCommand(templateDialogFactory)
            graphView.createTemplate = ShowTemplateCreationDialogCommand(templateDialogFactory)

        modulePath = sys.path[0]
        addSeriesCommand = ShowAddSeriesDialogCommand(graphView, seriesDialogFactory, seriesRepo, kind)
        addSeriesAction = Action("Plot", modulePath + "/resources/Add.svg", "Add Series", addSeriesCommand)

        editSeriesCommand = ShowEditSeriesDialogCommand(graphView, seriesDialogFactory)
        editSeriesAction = Action("Plot", modulePath + "/resources/Edit.svg", "Edit Series", editSeriesCommand)

        removeSeriesCommand = RemoveSeriesCommand(graphView, seriesRepo)
        removeSeriesAction = Action("Plot", modulePath + "/resources/Remove.svg", "Remove Series", removeSeriesCommand)

        duplicateCommand = DuplicateSeriesCommand(graphView, seriesRepo)
        duplicateAction = Action("Plot", modulePath + "/resources/Duplicate.svg", "Duplicate Series", duplicateCommand)

        fillAreaCommand = ShowAddSeriesDialogCommand(graphView, seriesDialogFactory, seriesRepo, "area")
        fillAreaAction = Action("Plot", modulePath + "/resources/Fill.svg", "Fill Area", fillAreaCommand)

        editSeriesFilterCommand = ShowEditSeriesFilterDialogCommand(graphView, filterDialogFactory)
        editSeriesFilterAction = Action("Plot", modulePath + "/resources/EditFilters.svg", "Edit Series Filter", editSeriesFilterCommand)

        createFilterCommand = ShowCreateFilterDialogCommand(graphView, filterDialogFactory)
        createFilterAction = Action("Plot", modulePath + "/resources/Filter.svg", "Manage Filters", createFilterCommand)

        widget: QWidget = graphView.getWidget()

        saveCommand = SaveGraphCommand(QtSaveFileDialog(widget), kind, seriesRepo, filterRepo)
        saveAction = Action("Plot", modulePath + "/resources/Save.svg", "Save Graph", saveCommand)

        graphView.actions.extend(
            [
                saveAction,
                addSeriesAction,
                editSeriesAction,
                removeSeriesAction,
                duplicateAction,
                fillAreaAction,
                editSeriesFilterAction,
                createFilterAction
            ]
        )
        filterDialogFactory.setParent(widget)

        return graphView
