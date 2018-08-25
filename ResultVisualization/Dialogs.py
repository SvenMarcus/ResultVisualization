from abc import ABC, abstractmethod
from enum import Enum


class DialogResult(Enum):
    Ok: int = 0
    Cancel: int = 1


class Dialog(ABC):
    """Interface for a dialog window"""

    @abstractmethod
    def show(self) -> DialogResult:
        """Shows the dialog window. Modality depends on implementation."""

        raise NotImplementedError()


class ChooseFolderDialog(Dialog, ABC):
    """Interface for a folder chooser dialog"""

    @abstractmethod
    def setStartingFolder(self, path: str) -> None:
        """Shows the dialog window. Modality depends on implementation."""

        raise NotImplementedError()

    @abstractmethod
    def getSelectedFolder(self) -> str:
        """Returns the folder selected by the user. If the dialog was canceled, returns an empty string."""

        raise NotImplementedError()


class DialogFactory(ABC):
    """Interface for a factory to create dialogs"""

    @abstractmethod
    def makeChooseFolderDialog(self) -> ChooseFolderDialog:
        """Creates and returns a ChooseFolderDialog."""

        raise NotImplementedError()