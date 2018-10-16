from abc import ABC, abstractmethod
from typing import List

from ResultVisualization.GraphView import GraphView
from ResultVisualization.GraphViewFactory import GraphViewFactory


class MainWindow(ABC):

    def __init__(self, graphViewFactory: GraphViewFactory, loadTemplatesCommand: 'Command'):
        self.__loadTemplatesCommand: 'Command' = loadTemplatesCommand
        loadTemplatesCommand.execute()
        self.__saveTemplatesCommand: 'Command' = None

        self.__graphViewFactory: GraphViewFactory = graphViewFactory
        self.__currentViews: List[GraphView] = list()
        self.__activeView: GraphView = None
        self.__linearGraphCount: int = 0
        self.__boxGraphCount: int = 0
        self.__loadFileCommand: 'Command' = None
        self.__loadFileCommand: 'Command' = None
        self._newLinearPlot()

    def _createTemplate(self):
        if self.__activeView is not None and self.__activeView.createTemplate is not None:
            self.__activeView.createTemplate.execute()

    def _loadFromTemplate(self):
        if self.__activeView is not None and self.__activeView.loadFromTemplate is not None:
            self.__activeView.loadFromTemplate.execute()

    def _onClose(self):
        self.saveTemplatesCommand.execute()

    @property
    def loadFileCommand(self) -> 'Command':
        return self.__loadFileCommand

    @loadFileCommand.setter
    def loadFileCommand(self, value: 'Command') -> None:
        self.__loadFileCommand = value

    @property
    def loadTemplatesCommand(self) -> 'Command':
        return self.__loadTemplatesCommand

    @loadTemplatesCommand.setter
    def loadTemplatesCommand(self, value: 'Command') -> None:
        self.__loadTemplatesCommand = value

    @property
    def saveTemplatesCommand(self) -> 'Command':
        return self.__saveTemplatesCommand

    @saveTemplatesCommand.setter
    def saveTemplatesCommand(self, value: 'Command') -> None:
        self.__saveTemplatesCommand = value

    def addGraphView(self, graphView: GraphView, title: str) -> None:
        self.__currentViews.append(graphView)
        self._appendGraphView(graphView, title)
        self.__activeView = graphView
        self._selectGraphViewAt(self.__currentViews.index(self.__activeView))

    def _setActiveIndex(self, index: int) -> None:
        if index < len(self.__currentViews) and len(self.__currentViews) > 0:
            self.__activeView = self.__currentViews[index]

    def _save(self) -> None:
        if self.__activeView is not None:
            self.__activeView.saveCommand.execute()

    def _newLinearPlot(self) -> None:
        graphView: GraphView = self.__graphViewFactory.makeGraphView("linear")
        self.__linearGraphCount += 1
        self.__currentViews.append(graphView)
        self._appendGraphView(graphView, "Linear Plot" +
                              str(self.__linearGraphCount))
        self.__activeView = graphView
        self._selectGraphViewAt(self.__currentViews.index(self.__activeView))

    def _newBoxPlot(self) -> None:
        graphView: GraphView = self.__graphViewFactory.makeGraphView("box")
        self.__boxGraphCount += 1
        self.__currentViews.append(graphView)
        self._appendGraphView(graphView, "Box Plot" +
                              str(self.__boxGraphCount))
        self.__activeView = graphView
        self._selectGraphViewAt(self.__currentViews.index(self.__activeView))

    def _closeActiveGraphView(self) -> None:
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
