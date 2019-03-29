from abc import ABC, abstractmethod
from typing import List

from ResultVisualization.Action import Action
from ResultVisualization.Events import Event, InvokableEvent
from ResultVisualization.GraphView import GraphView
from ResultVisualization.GraphViewFactory import GraphViewFactory
from ResultVisualization.MenuBar import MenuBar
from ResultVisualization.Toolbar import Toolbar


class MainWindow(ABC):

    def __init__(self, graphViewFactory: GraphViewFactory, toolBar: Toolbar = None, menuBar: MenuBar = None):
        self.__menuBar: MenuBar = menuBar
        self.__toolbar: Toolbar = toolBar
        self.__actions: List[Action] = list()
        self._onClose: InvokableEvent = InvokableEvent()

        self.__graphViewFactory: GraphViewFactory = graphViewFactory
        self.__currentViews: List[GraphView] = list()
        self.__activeView: GraphView = None
        self.__linearGraphCount: int = 0
        self.__boxGraphCount: int = 0

    def onCloseEvent(self) -> Event:
        return self._onClose

    def addGraphView(self, graphView: GraphView, title: str = None) -> None:
        self.__currentViews.append(graphView)
        self._appendGraphView(graphView, title or "Plot")
        self._selectGraphViewAt(len(self.__currentViews) - 1)
        graphView.titleChanged.append(self.__onTitleChanged)

    def getActiveView(self) -> GraphView:
        return self.__activeView

    def getCurrentViews(self) -> List[GraphView]:
        return list(self.__currentViews)

    def _setActiveIndex(self, index: int) -> None:
        if self.__activeView is not None:
            for action in self.__activeView.actions:
                self.__toolbar.removeAction(action)
                self.__menuBar.removeAction(action)

        if index < len(self.__currentViews) and len(self.__currentViews) > 0:
            self.__activeView = self.__currentViews[index]

            for action in self.__activeView.actions:
                self.__toolbar.addAction(action)
                self.__menuBar.addAction(action)

    def closeActiveGraphView(self) -> None:
        noCurrentViews = len(self.__currentViews)
        if noCurrentViews > 0:
            index: int = self.__currentViews.index(self.__activeView)
            self.__activeView.titleChanged.remove(self.__onTitleChanged)
            self.__currentViews.remove(self.__activeView)
            self._removeGraphView(index)

            noCurrentViews = len(self.__currentViews)
            if noCurrentViews > 0:
                self.__activeView = self.__currentViews[noCurrentViews - 1]
                self._selectGraphViewAt(
                    self.__currentViews.index(self.__activeView))
            else:
                self.__activeView = None

    def __onTitleChanged(self, graphView: GraphView, args) -> None:
        index: int = self.__currentViews.index(graphView)
        self._setGraphViewTitleAt(graphView.getTitle(), index)

    @abstractmethod
    def show(self):
        raise NotImplementedError()

    @abstractmethod
    def _appendGraphView(self, graphView: GraphView, title: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _setGraphViewTitleAt(self, title: str, index: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _selectGraphViewAt(self, index: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _removeGraphView(self, index: int) -> None:
        raise NotImplementedError()
