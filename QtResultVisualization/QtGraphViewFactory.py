from PyQt5.QtWidgets import QWidget


from QtResultVisualization.Dialogs import QtSaveFileDialog
from QtResultVisualization.QtFilterDialogFactory import QtFilterDialogFactory
from QtResultVisualization.QtGraphView import QtGraphView
from QtResultVisualization.QtSeriesDialogFactory import QtSeriesDialogFactory

from ResultVisualization.Commands import (DuplicateSeriesCommand,
                                          RemoveSeriesCommand,
                                          ShowAddSeriesDialogCommand,
                                          ShowCreateFilterDialogCommand,
                                          ShowEditSeriesDialogCommand,
                                          ShowEditSeriesFilterDialogCommand,
                                          SaveGraphCommand)
from ResultVisualization.Dialogs import SeriesDialogFactory
from ResultVisualization.FilterDialogFactory import FilterDialogFactory
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.GraphView import GraphView
from ResultVisualization.GraphViewFactory import GraphViewFactory
from ResultVisualization.SeriesRepository import SeriesRepository


class QtGraphViewFactory(GraphViewFactory):

    def makeGraphView(self, kind: str, seriesRepo=None, filterRepo=None) -> GraphView:
        graphView: QtGraphView = None
        seriesRepo = seriesRepo or SeriesRepository()
        filterRepo = filterRepo or FilterRepository()
        seriesDialogFactory: SeriesDialogFactory = QtSeriesDialogFactory()

        filterDialogFactory: FilterDialogFactory = QtFilterDialogFactory(filterRepo, seriesRepo)

        graphView = QtGraphView(seriesRepo.getSeries())
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
