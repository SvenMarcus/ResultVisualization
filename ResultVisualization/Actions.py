from abc import ABC, abstractmethod

from ResultVisualization.Events import Event, InvokableEvent
from ResultVisualization.Dialogs import ChooseFolderDialog, DialogFactory


class Action(ABC):
    """Interface for Menu Actions"""

    @abstractmethod
    def execute(self) -> None:
        """Executes the Action."""

        raise NotImplementedError()


class ChooseFolderAction(Action):
    """Shows ChooseFolderDialog when executed"""

    def __init__(self, dialogFactory: DialogFactory):
        self.__dialogFactory = dialogFactory
        self.__onChooseFolder: Event = InvokableEvent()

    @property
    def onChooseFolder(self) -> Event:
        return self.__onChooseFolder

    def execute(self) -> None:
        dialog: ChooseFolderDialog = self.__dialogFactory.makeChooseFolderDialog()
        dialog.show()
