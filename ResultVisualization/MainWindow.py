from abc import ABC, abstractmethod
from typing import List

from ResultVisualization.Action import Action
from ResultVisualization.Events import Event, InvokableEvent
from ResultVisualization.GraphView import GraphView
from ResultVisualization.GraphViewFactory import GraphViewFactory
from ResultVisualization.Toolbar import Toolbar


class MainWindow(ABC):

    def __init__(self, toolBar: Toolbar, graphViewFactory: GraphViewFactory):
        self.__toolbar: Toolbar = toolBar
        self.__actions: List[Action] = list()
        self._onClose: InvokableEvent = InvokableEvent()

        self.__graphViewFactory: GraphViewFactory = graphViewFactory
        self.__currentViews: List[GraphView] = list()
        self.__activeView: GraphView = None
        self.__linearGraphCount: int = 0
        self.__boxGraphCount: int = 0

    def _createTemplate(self):
        if self.__activeView is not None and self.__activeView.createTemplate is not None:
            self.__activeView.createTemplate.execute()

    def _loadFromTemplate(self):
        if self.__activeView is not None and self.__activeView.loadFromTemplate is not None:
            self.__activeView.loadFromTemplate.execute()

    def onCloseEvent(self) -> Event:
        return self._onClose

    def addGraphView(self, graphView: GraphView, title: str = None) -> None:
        self.__currentViews.append(graphView)
        self._appendGraphView(graphView, title or "Plot")
        self._selectGraphViewAt(len(self.__currentViews) - 1)

    def _setActiveIndex(self, index: int) -> None:
        if self.__activeView is not None:
            for action in self.__activeView.actions:
                self.__toolbar.removeAction(action)

        if index < len(self.__currentViews) and len(self.__currentViews) > 0:
            self.__activeView = self.__currentViews[index]

            for action in self.__activeView.actions:
                self.__toolbar.addAction(action)

    def closeActiveGraphView(self) -> None:
        noCurrentViews = len(self.__currentViews)
        if noCurrentViews > 0:
            index: int = self.__currentViews.index(self.__activeView)
            self.__currentViews.remove(self.__activeView)
            self._removeGraphView(index)

            noCurrentViews = len(self.__currentViews)
            if noCurrentViews > 0:
                self.__activeView = self.__currentViews[noCurrentViews - 1]
                self._selectGraphViewAt(
                    self.__currentViews.index(self.__activeView))
            else:
                self.__activeView = None

    @abstractmethod
    def show(self):
        raise NotImplementedError()

    @abstractmethod
    def _appendGraphView(self, graphView: GraphView, title: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _selectGraphViewAt(self, index: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _removeGraphView(self, index: int) -> None:
        raise NotImplementedError()
