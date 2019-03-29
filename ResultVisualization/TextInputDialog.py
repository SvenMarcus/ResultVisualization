from abc import ABC, abstractmethod

from ResultVisualization.Dialogs import Dialog, DialogResult


class TextInputDialog(Dialog, ABC):

    def __init__(self, title: str = "", label: str = "Enter Text"):
        self._result: DialogResult = DialogResult.Cancel
        self.__text: str = ""
        self._title: str = title
        self._label: str = label

    def _confirm(self):
        self.__text = self._getTextFromView()
        self._result = DialogResult.Ok

    def getText(self) -> str:
        return self.__text

    @abstractmethod
    def _getTextFromView(self) -> str:
        raise NotImplementedError()

