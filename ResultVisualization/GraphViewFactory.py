from abc import ABC, abstractmethod

from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.GraphView import GraphView
from ResultVisualization.SeriesRepository import SeriesRepository
from ResultVisualization.TemplateRepository import TemplateRepository

class GraphViewFactory(ABC):

    @abstractmethod
    def setTemplateRepository(self, templateRepo: TemplateRepository) -> None:
        raise NotImplementedError()

    @abstractmethod
    def getTemplateRepository(self) -> TemplateRepository:
        raise NotImplementedError()

    @abstractmethod
    def makeGraphView(self, kind: str, seriesRepo: SeriesRepository = None, filterRepo: FilterRepository = None) -> GraphView:
        raise NotImplementedError()
