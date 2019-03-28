from PyQt5.QtWidgets import QWidget, QInputDialog

from ResultVisualization.Dialogs import DialogResult
from ResultVisualization.TextInputDialog import TextInputDialog


class QtTextInputDialog(TextInputDialog):

    def __init__(self,  parent: QWidget = None):
        super().__init__()
        self.__parent = parent
        self.__text: str = ""

    def _getTextFromView(self) -> str:
        return self.__text

    def show(self) -> DialogResult:
        self._result = DialogResult.Cancel
        text, ok = QInputDialog.getText(self.__parent, self._title, self._label)
        if ok:
            self.__text = text
            self._confirm()

        return self._result
