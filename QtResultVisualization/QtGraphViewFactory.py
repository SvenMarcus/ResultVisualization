from PyQt5.QtWidgets import QWidget

from ResultVisualization.FilterDialogFactory import FilterDialogFactory
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.GraphViewFactory import GraphViewFactory
from ResultVisualization.GraphView import GraphView
from ResultVisualization.SeriesRepository import SeriesRepository
from ResultVisualization.Dialogs import SeriesDialogFactory
from QtResultVisualization.Dialogs import QtLineSeriesDialogFactory
from QtResultVisualization.QtFilterDialogFactory import QtFilterDialogFactory
from QtResultVisualization.QtGraphView import QtGraphView

class QtGraphViewFactory(GraphViewFactory):

    def makeGraphView(self, kind) -> GraphView:
        if kind == "linear":
            seriesDialogFactory: SeriesDialogFactory = QtLineSeriesDialogFactory()
            seriesRepo: SeriesRepository = SeriesRepository()
            filterRepo: FilterRepository = FilterRepository()
            filterDialogFactory: FilterDialogFactory = QtFilterDialogFactory(filterRepo)

            graphView: QtGraphView = QtGraphView(seriesDialogFactory, seriesRepo, filterDialogFactory)
            widget: QWidget = graphView.getWindow()
            filterDialogFactory.setParent(widget)

            return graphView
