from abc import ABC, abstractmethod
from typing import List


class Widget(ABC):
    def __init__(self):
        ABC.__init__(self)

    @abstractmethod
    def showWidget(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def hideWidget(self) -> None:
        raise NotImplementedError()

class PlotConfig:

    def __init__(self, widgets: List[Widget]):
        self.__widgets: List[Widget] = widgets
        self.__currentWidget: Widget = None
        self.__selectWidget(0)

    def __selectWidget(self, index: int) -> None:
        if self.__currentWidget:
            self.__currentWidget.hideWidget()
        
        self.__currentWidget = self.__widgets[index]
        self.__currentWidget.showWidget()


class LinePlotConfig:
    pass
    # def __init__()