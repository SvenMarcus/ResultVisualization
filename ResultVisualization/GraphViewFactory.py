from abc import ABC, abstractmethod

from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.GraphView import GraphView
from ResultVisualization.SeriesRepository import SeriesRepository


class GraphViewFactory(ABC):

    @abstractmethod
    def makeGraphView(self, kind: str, seriesRepo: SeriesRepository = None, filterRepo: FilterRepository = None) -> GraphView:
        raise NotImplementedError()
