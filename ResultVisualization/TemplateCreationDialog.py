from abc import ABC, abstractmethod
from typing import List

from ResultVisualization.Dialogs import Dialog, DialogResult
from ResultVisualization.Templates import LineTemplate
from ResultVisualization.TemplateRepository import TemplateRepository


class TemplateCreationDialog(Dialog):

    def __init__(self, templateRepository: TemplateRepository):
        self.__template = LineTemplate()
        self.__template.name = "default"
        self.__repository = templateRepository
        self._result: DialogResult = DialogResult.Cancel

    def _addStyle(self) -> None:
        style: str = self._getStyleStringFromView()

        if not style:
            self._showMessage("Error. Cannot add empty style.")
            return

        self._clearStyleStringInView()
        self.__template.styles.append(style)
        self._addStyleToListView(style)

    def _removeStyle(self) -> None:
        selectedIndexes = list(
            sorted(self._getSelectedStyleIndexes(), reverse=True))
        for index in selectedIndexes:
            self.__template.styles.pop(index)
            self._removeStyleFromListView(index)

    def _confirm(self) -> None:
        self.__template.name = self._getTitleFromView()
        self.__template.xColumnTitle = self._getXColumnFromView()
        self.__template.yColumnTitle = self._getYColumnFromView()
        self.__template.metaColumnTitle = self._getMetaColumnFromView()

        if not self.__template.xColumnTitle or not self.__template.yColumnTitle:
            self._showMessage("Error. Empty x or y column header!")
            return

        self.__template.xLabel = self._getXLabelFromView()
        self.__template.yLabel = self._getYLabelFromView()

        self.__repository.addTemplate(self.__template)

        self._result = DialogResult.Ok
        self._close()

    @abstractmethod
    def _addStyleToListView(self, style: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _removeStyleFromListView(self, index: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getSelectedStyleIndexes(self) -> List[int]:
        raise NotImplementedError()

    @abstractmethod
    def _getTitleFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _getStyleStringFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _getXColumnFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _getYColumnFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _getMetaColumnFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _getXLabelFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _getYLabelFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _clearStyleStringInView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _showMessage(self, msg: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _close(self) -> None:
        raise NotImplementedError()
