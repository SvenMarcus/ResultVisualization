from abc import ABC, abstractmethod

from ResultVisualization.Events import Event, InvokableEvent
from ResultVisualization.Dialogs import ChooseFolderDialog, DialogFactory, DialogResult


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
        """This Event is triggered when the user selects a folder."""

        return self.__onChooseFolder

    def execute(self) -> None:
        dialog: ChooseFolderDialog = self.__dialogFactory.makeChooseFolderDialog()
        result: DialogResult = dialog.show()
        if result == DialogResult.Ok:
            self.__onChooseFolder(self, dialog.getSelectedFolder())
