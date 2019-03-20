from typing import List

from PyQt5.QtWidgets import QFileDialog, QWidget

from ResultVisualization.Dialogs import (ChooseFileDialog, ChooseFolderDialog,
                                         ChooseMultipleFilesDialog,
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


class QtSaveFileDialog(ChooseFileDialog):

    def __init__(self, extension: str, parent: QWidget = None):
        self.__extension = extension
        self.__selectedFile: str = ""
        self.__parent: QWidget = parent

    def setStartingFolder(self, path: str) -> None:
        pass

    def getSelectedFile(self) -> str:
        return self.__selectedFile

    def show(self) -> DialogResult:
        self.__selectedFile = QFileDialog.getSaveFileName(
            self.__parent, "Save File", filter=self.__extension)[0]
        if self.__selectedFile and isinstance(self.__selectedFile, str):
            return DialogResult.Ok

        return DialogResult.Cancel


class QtChooseFileDialog(ChooseFileDialog):
    """Qt Implementation of ChooseFolderDialog"""

    def __init__(self, fileType: str, parent: QWidget = None):
        self.__selectedFile: str = ""
        self.__fileType: str = fileType
        self.__parent: QWidget = parent

    def getSelectedFile(self) -> str:
        return self.__selectedFile

    def show(self) -> DialogResult:
        self.__selectedFile = QFileDialog.getOpenFileName(
            self.__parent, "Select File", filter=self.__fileType)[0]
        if self.__selectedFile and isinstance(self.__selectedFile, str):
            return DialogResult.Ok

        return DialogResult.Cancel


class QtChooseMultipleFilesDialog(ChooseMultipleFilesDialog):
    """Qt Implementation of ChooseFolderDialog"""

    def __init__(self, fileType: str, parent: QWidget = None):
        self.__selectedFiles: List[str] = list()
        self.__fileType: str = fileType
        self.__parent: QWidget = parent

    def getSelectedFiles(self) -> List[str]:
        return self.__selectedFiles

    def show(self) -> DialogResult:
        self.__selectedFiles = QFileDialog.getOpenFileNames(
            self.__parent, "Select Files", filter=self.__fileType)[0]
        if len(self.__selectedFiles) > 0:
            return DialogResult.Ok

        return DialogResult.Cancel
