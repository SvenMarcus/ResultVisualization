from abc import ABC, abstractmethod
from typing import Tuple

from ResultVisualization.Dialogs import DialogResult, SeriesDialog
from ResultVisualization.Plot import FillAreaSeries, Series, TextPosition
from ResultVisualization.util import tryConvertToFloat

class FillAreaDialog(SeriesDialog, ABC):

    def __init__(self, initialSeries: FillAreaSeries = None):
        self._result: DialogResult = DialogResult.Cancel
        self.__series = initialSeries or FillAreaSeries()
        self.__setInitialSeriesInView(self.__series)

    def getSeries(self) -> Series:
        return self.__series

    def _confirm(self) -> None:
        self.__series.title = self._getTitleFromView()
        self.__series.text = self._getTextFromView()
        self.__series.textPosition = self._getTextPositionFromView()

        minX = tryConvertToFloat(self._getMinXFromView()) or 0
        maxX = tryConvertToFloat(self._getMaxXFromView()) or 0
        minY = tryConvertToFloat(self._getMinYFromView()) or 0
        maxY = tryConvertToFloat(self._getMaxYFromView()) or 0

        alphaStr = self._getAlphaFromView()
        if alphaStr:
            alpha = tryConvertToFloat(alphaStr)
            color = self.__series.color

        self.__series.color = (color[0], color[1], color[2], alpha)

        self.__series.xLimits = (minX, maxX)
        self.__series.yLimits = (minY, maxY)

        self._result = DialogResult.Ok
        self._close()

    def _setColor(self, color: Tuple[float, float, float, float]) -> None:
        self.__series.color = color

    def _setTextColor(self, color: Tuple[float, float, float, float]) -> None:
        self.__series.textColor = color

    def __setInitialSeriesInView(self, series: FillAreaSeries) -> None:
        self._setTitleInView(series.title)
        self._setTextInView(series.text)
        self._setTextPositionInView(series.textPosition)
        self._setMinXInView(series.xLimits[0])
        self._setMaxXInView(series.xLimits[1])
        self._setMinYInView(series.yLimits[0])
        self._setMaxYInView(series.yLimits[1])
        self._setAlphaInView(series.color[3])

    @abstractmethod
    def _close(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _getTitleFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _getTextFromView(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _getTextPositionFromView(self) -> TextPosition:
        raise NotImplementedError()

    @abstractmethod
    def _getMinXFromView(self):
        raise NotImplementedError()

    @abstractmethod
    def _getMaxXFromView(self):
        raise NotImplementedError()

    @abstractmethod
    def _getMinYFromView(self):
        raise NotImplementedError()

    @abstractmethod
    def _getMaxYFromView(self):
        raise NotImplementedError()

    @abstractmethod
    def _getAlphaFromView(self):
        raise NotImplementedError()

    @abstractmethod
    def _setTitleInView(self, title) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _setTextInView(self, text) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _setTextPositionInView(self, pos) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _setMinXInView(self, value) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _setMaxXInView(self, value) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _setMinYInView(self, value) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _setMaxYInView(self, value) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _setAlphaInView(self, value) -> None:
        raise NotImplementedError()
