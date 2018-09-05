from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict


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


class DataChooserDialog(Dialog, ABC):
    """Interface for a dialog to choose data"""

    @abstractmethod
    def getChosenData(self) -> Dict[str, float]:
        """Returns the data chosen in the dialog as dictionary of strings and floats."""

        raise NotImplementedError()


class DialogFactory(ABC):
    """Interface for a factory to create dialogs"""

    @abstractmethod
    def makeChooseFolderDialog(self) -> ChooseFolderDialog:
        """Creates and returns a ChooseFolderDialog."""

        raise NotImplementedError()

    @abstractmethod
    def makeDataChooserDialog(self) -> DataChooserDialog:
        """Creates and returns a DataChooserDialog."""

        raise NotImplementedError()