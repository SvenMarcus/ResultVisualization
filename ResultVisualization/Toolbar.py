from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import List

from ResultVisualization.Action import Action

class Toolbar(ABC):

    def __init__(self):
        self.__actions: OrderedDict = OrderedDict()

    def addAction(self, action: Action) -> None:
        if action.category not in self.__actions.keys():
            self.__actions[action.category] = list()

        actionsInCategory: List[Action] = self.__actions[action.category]
        actionsInCategory.append(action)
        self._addActionToView(action)

    def clearActions(self) -> None:
        self.__actions.clear()

    @abstractmethod
    def _addActionToView(self, action: Action) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _clearActionsInView(self) -> None:
        raise NotImplementedError()
