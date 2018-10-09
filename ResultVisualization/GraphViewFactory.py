from abc import ABC, abstractmethod

from ResultVisualization.GraphView import GraphView


class GraphViewFactory(ABC):

    @abstractmethod
    def makeGraphView(self, kind: str) -> GraphView:
        raise NotImplementedError()
