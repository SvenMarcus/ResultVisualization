from ResultVisualization.DialogResult import DialogResult
from ResultVisualization.Dialogs.Dialog import Dialog


class ChooseFolderDialog(Dialog):

    def __init__(self):
        self.startingFolder: str = ""

    def setStartingFolder(self, path: str) -> None:
        self.startingFolder = path

    def getSelectedFolder(self) -> str:
        pass

    def show(self) -> DialogResult:
        pass