from abc import ABC, abstractmethod

from ResultVisualization.Dialogs import Dialog, DialogResult
from ResultVisualization.Plot import PlotSettings


class PlotSettingsDialog(Dialog, ABC):

    def __init__(self, plotSettings: PlotSettings = None):
        self.__plotSettings: PlotSettings = plotSettings or PlotSettings()
        self._result: DialogResult = DialogResult.Cancel
        if plotSettings is not None:
            self._setMinXInView(plotSettings.minX)
            self._setMaxXInView(plotSettings.maxX)
            self._setMinYInView(plotSettings.minY)
            self._setMaxYInView(plotSettings.maxY)

    def getPlotSettings(self) -> PlotSettings:
        return self.__plotSettings

    def _confirm(self) -> None:
        self.__plotSettings.minX = self._getMinXFromView()
        self.__plotSettings.maxX = self._getMaxXFromView()
        self.__plotSettings.minY = self._getMinYFromView()
        self.__plotSettings.maxY = self._getMaxYFromView()
        self._result = DialogResult.Ok
        self._close()

    @abstractmethod
    def _close(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _setMinXInView(self, x) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getMinXFromView(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def _setMaxXInView(self, x) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getMaxXFromView(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def _setMinYInView(self, y) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getMinYFromView(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def _setMaxYInView(self, y) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getMaxYFromView(self) -> float:
        raise NotImplementedError()
