from abc import ABC, abstractmethod
from enum import Enum

from ResultVisualization.Plot import Series


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


class ChooseFileDialog(Dialog, ABC):
    """Interface for a file chooser dialog"""

    @abstractmethod
    def setStartingFolder(self, path: str) -> None:
        """Shows the dialog window. Modality depends on implementation."""

        raise NotImplementedError()

    @abstractmethod
    def getSelectedFile(self) -> str:
        """Returns the file selected by the user. If the dialog was canceled, returns an empty string."""

        raise NotImplementedError()


class SeriesDialog(ABC):

    @abstractmethod
    def getSeries(self) -> Series:
        """Returns a Series object based on the data entered and selected by the user."""
        
        raise NotImplementedError()


class SeriesDialogFactory(ABC):

    @abstractmethod
    def makeSeriesDialog(self, kind: str = "", initialSeries: Series = None) -> SeriesDialog:
        raise NotImplementedError()
