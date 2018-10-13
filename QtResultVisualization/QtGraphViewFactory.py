from PyQt5.QtWidgets import QWidget

from QtResultVisualization.QtBoxSeriesDialog import QtBoxSeriesDialogFactory
from QtResultVisualization.Dialogs import QtLineSeriesDialogFactory
from QtResultVisualization.QtFilterDialogFactory import QtFilterDialogFactory
from QtResultVisualization.QtGraphView import QtGraphView

from ResultVisualization.Commands import (RemoveSeriesCommand,
                                          ShowAddSeriesDialogCommand,
                                          ShowCreateFilterDialogCommand,
                                          ShowEditSeriesDialogCommand,
                                          ShowEditSeriesFilterDialogCommand)
from ResultVisualization.Dialogs import SeriesDialogFactory
from ResultVisualization.FilterDialogFactory import FilterDialogFactory
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.GraphView import GraphView
from ResultVisualization.GraphViewFactory import GraphViewFactory
from ResultVisualization.SeriesRepository import SeriesRepository


class QtGraphViewFactory(GraphViewFactory):

    def makeGraphView(self, kind) -> GraphView:
        graphView: QtGraphView = None
        seriesDialogFactory: SeriesDialogFactory = None
        
        if kind == "linear":
            seriesDialogFactory: SeriesDialogFactory = QtLineSeriesDialogFactory()
        elif kind == "box":
            seriesDialogFactory = QtBoxSeriesDialogFactory()
        else:
            return None

        seriesRepo: SeriesRepository = SeriesRepository()
        filterRepo: FilterRepository = FilterRepository()
        filterDialogFactory: FilterDialogFactory = QtFilterDialogFactory(filterRepo, seriesRepo)

        graphView = QtGraphView(seriesRepo.getSeries())

        graphView.addSeriesCommand = ShowAddSeriesDialogCommand(graphView, seriesDialogFactory, seriesRepo)
        graphView.editSeriesCommand = ShowEditSeriesDialogCommand(graphView, seriesDialogFactory)
        graphView.removeSeriesCommand = RemoveSeriesCommand(graphView, seriesRepo)
        graphView.editSeriesFilterCommand = ShowEditSeriesFilterDialogCommand(graphView, filterDialogFactory)
        graphView.createFilterCommand = ShowCreateFilterDialogCommand(graphView, filterDialogFactory)

        widget: QWidget = graphView.getWindow()
        filterDialogFactory.setParent(widget)

        return graphView
