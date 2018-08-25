from PyQt5.QtWidgets import QFileDialog, QWidget

from ResultVisualization.Dialogs import (ChooseFolderDialog, DialogFactory,
                                         DialogResult)


class QtChooseFolderDialog(ChooseFolderDialog):
    """Qt Implementation of ChooseFolderDialog"""

    def __init__(self, parent: QWidget = None):
        self.__selectedFolder: str = ""
        self.__parent: QWidget = parent

    def setStartingFolder(self, path: str) -> None:
        pass

    def getSelectedFolder(self) -> str:
        return self.__selectedFolder

    def show(self) -> DialogResult:
        self.__selectedFolder = str(QFileDialog.getExistingDirectory(
            self.__parent, "Select Folder", options=QFileDialog.ShowDirsOnly))
        if self.__selectedFolder:
            return DialogResult.Ok

        return DialogResult.Cancel


class QtDialogFactory(DialogFactory):
    """Qt Implementation of DialogFactory. Creates Qt implementations of Dialogs."""

    def __init__(self, parent: QWidget = None):
        self.__parent: QWidget = parent

    def setParent(self, parent: QWidget):
        """Sets the parent widget for created dialogs"""
        self.__parent = parent

    def makeChooseFolderDialog(self) -> ChooseFolderDialog:
        return QtChooseFolderDialog(self.__parent)
