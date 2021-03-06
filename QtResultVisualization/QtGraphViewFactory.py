import os.path as path
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
        self.__lineFilterRepo = FilterRepository()
        self.__boxFilterRepo = FilterRepository()

    def setTemplateRepository(self, templateRepo):
        self.__templateRepo = templateRepo

    def getTemplateRepository(self) -> TemplateRepository:
        return self.__templateRepo

    def makeGraphView(self, kind: str, seriesRepo=None, filterRepo=None) -> GraphView:
        seriesRepo = seriesRepo or SeriesRepository()

        if filterRepo:
            self.__mergeFilterRepositories(kind, filterRepo)

        filterRepo = self.__getFilterRepository(kind)

        seriesDialogFactory: SeriesDialogFactory = QtSeriesDialogFactory()

        filterDialogFactory: FilterDialogFactory = QtFilterDialogFactory(filterRepo, seriesRepo)

        graphView: QtGraphView = QtGraphView(seriesRepo.getSeries())

        resources = path.join(sys.path[0], "resources")

        addSeriesCommand = ShowAddSeriesDialogCommand(graphView, seriesDialogFactory, seriesRepo, kind)
        addSeriesAction = Action("Plot", path.join(resources, "Add.svg"), "Add Series", addSeriesCommand, shortcut="Ctrl+N")

        editSeriesCommand = ShowEditSeriesDialogCommand(graphView, seriesDialogFactory)
        editSeriesAction = Action("Plot", path.join(resources, "Edit.svg"), "Edit Series", editSeriesCommand, shortcut="Ctrl+E")

        removeSeriesCommand = RemoveSeriesCommand(graphView, seriesRepo)
        removeSeriesAction = Action("Plot", path.join(resources, "Remove.svg"), "Remove Series", removeSeriesCommand, shortcut="Ctrl+K")

        duplicateCommand = DuplicateSeriesCommand(graphView, seriesRepo)
        duplicateAction = Action("Plot", path.join(resources, "Duplicate.svg"), "Duplicate Series", duplicateCommand, shortcut="Ctrl+D")

        editSeriesFilterCommand = ShowEditSeriesFilterDialogCommand(graphView, filterDialogFactory)
        editSeriesFilterAction = Action("Plot", path.join(resources, "EditFilters.svg"), "Edit Series Filters",
                                        editSeriesFilterCommand, shortcut="Ctrl+F")

        createFilterCommand = ShowCreateFilterDialogCommand(graphView, filterDialogFactory)
        createFilterAction = Action("Plot", path.join(resources, "Filter.svg"), "Manage Filters", createFilterCommand, shortcut="Ctrl+M")

        widget: QWidget = graphView.getWidget()

        saveCommand = SaveGraphCommand(QtSaveFileDialog("*.graph", widget), kind, seriesRepo, filterRepo)
        saveAction = Action("File", path.join(resources, "Save.svg"), "Save Graph", saveCommand, shortcut="Ctrl+S")

        graphView.actions.extend(
            [
                saveAction,
                addSeriesAction,
                editSeriesAction,
                removeSeriesAction,
                duplicateAction,
                editSeriesFilterAction,
                createFilterAction
            ]
        )

        title: str = "Box Plot"

        if kind == "linear":
            title = "Line Plot"
            fillAreaCommand = ShowAddSeriesDialogCommand(graphView, seriesDialogFactory, seriesRepo, "area")
            fillAreaAction = Action("Plot", path.join(resources, "Fill.svg"), "Fill Area", fillAreaCommand, shortcut="Ctrl+A")
            graphView.actions.append(fillAreaAction)

            templateDialogFactory = QtTemplateDialogFactory(self.__templateRepo, graphView, seriesRepo)
            loadFromTemplate = ShowLoadFromTemplateDialogCommand(templateDialogFactory)
            loadFromTemplateAction = Action("Template", path.join(resources, "LoadTemplate.svg"), "Load from Template",
                                            loadFromTemplate)

            createTemplate = ShowTemplateCreationDialogCommand(templateDialogFactory)
            createTemplateAction = Action("Template", path.join(resources, "Template.svg"), "Create Template", createTemplate)
            graphView.actions.extend([
                loadFromTemplateAction,
                createTemplateAction
            ])

        filterDialogFactory.setParent(widget)
        graphView.setTitle(title)

        return graphView

    def __getFilterRepository(self, kind: str) -> FilterRepository:
        if kind == "linear":
            return self.__lineFilterRepo

        return self.__boxFilterRepo

    def __mergeFilterRepositories(self, kind: str, repository: FilterRepository) -> None:
        targetRepository: FilterRepository
        if kind == "linear":
            targetRepository = self.__lineFilterRepo
        else:
            targetRepository = self.__boxFilterRepo

        for filter in repository.getFilters():
            targetRepository.addFilter(filter)
