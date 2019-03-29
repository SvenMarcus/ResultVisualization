from abc import ABC, abstractmethod
from typing import List

from ResultVisualization.Action import Action


class Toolbar(ABC):

    def __init__(self):
        self.__actions: list = list()

    def addAction(self, action: Action) -> None:
        self.__actions.append(action)
        self._addActionToView(action)

    def removeAction(self, action: Action) -> None:
        self.__actions.remove(action)
        self._removeActionFromView(action)

    def clearActions(self) -> None:
        self.__actions.clear()
        self._clearActionsInView()

    @abstractmethod
    def _addActionToView(self, action: Action) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _removeActionFromView(self, action: Action) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _clearActionsInView(self) -> None:
        raise NotImplementedError()
