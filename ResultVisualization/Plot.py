from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable, List, Tuple

from ResultVisualization.Filter import ListFilter
from ResultVisualization.SeriesVisitor import SeriesVisitor
from ResultVisualization.Titled import Titled
from ResultVisualization.util import isNumber


class NonNumberInPlotConfigError(RuntimeError):

    def __init__(self, **kwargs):
        RuntimeError.__init__(self, kwargs)


class Plotter(ABC):

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def lineSeries(self, xValues: Iterable, yValues: Iterable, **kwargs) -> None:
        raise NotImplementedError()

    @abstractmethod
    def boxplot(self, data: Iterable[Iterable], **kwargs) -> None:
        raise NotImplementedError()

    @abstractmethod
    def fillArea(self, xValues: Iterable, lowerYValues: Iterable, upperYValues: Iterable, **kwargs) -> None:
        raise NotImplementedError()

    @abstractmethod
    def text(self, x: float, y: float, text: str, use_percentage: bool = False) -> None:
        raise NotImplementedError()

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError()


class Series(Titled, ABC):

    def __init__(self):
        self._title: str = ""
        self._xLabel: str = ""
        self._yLabel: str = ""

    @abstractmethod
    def plot(self, plotter: Plotter) -> None:
        raise NotImplementedError()

    @property
    def title(self) -> str:
        """Returns the title of the series."""

        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Sets the title of the series to the given value."""

        self._title = value

    @property
    def xLabel(self) -> str:
        return self._xLabel

    @xLabel.setter
    def xLabel(self, value: str) -> None:
        self._xLabel = value

    @property
    def yLabel(self) -> str:
        return self._yLabel

    @yLabel.setter
    def yLabel(self, value: str) -> None:
        self._yLabel = value

    @abstractmethod
    def accept(self, seriesVisitor: SeriesVisitor) -> None:
        raise NotImplementedError()


class FilterableSeries(Series):

    def __init__(self):
        super().__init__()
        self._metaData: List[str] = list()
        self._filters: List[ListFilter] = list()

    def addFilter(self, listFilter: ListFilter) -> None:
        self._filters.append(listFilter)

    def removeFilter(self, listFilter: ListFilter) -> None:
        self._filters.remove(listFilter)

    def clearFilters(self) -> None:
        self._filters.clear()

    @property
    def metaData(self) -> List[str]:
        """Returns a list with meta data for the plot."""

        return self._metaData

    @metaData.setter
    def metaData(self, value: List[str]) -> None:
        self._metaData = value

    @property
    def filters(self) -> List[ListFilter]:
        return self._filters

    @filters.setter
    def filters(self, value: List[ListFilter]) -> None:
        self._filters = value


class Graph(ABC):

    def __init__(self, plotter: Plotter = None):
        self.__plotter: Plotter = plotter
        self.__series: List[Series] = list()

    def addPlot(self, series: Series) -> None:
        self.__series.append(series)
        self.updatePlot()

    def removePlot(self, series: Series) -> None:
        self.__series.remove(series)
        self.updatePlot()

    def updatePlot(self) -> None:
        self.__plotter.resetPlotData()
        self.__plotter.clear()
        for series in self.__series:
            series.plot(self.__plotter)
        self.__plotter.finishPlot()


class LineSeries(FilterableSeries):

    def __init__(self):
        super().__init__()
        self.__xValues = []
        self.__yValues = []
        self.__confidenceBand: float = 0
        self.__style: str = "-"

    def plot(self, plotter: Plotter) -> None:
        x, y, meta = self.__getPlotValues()
        self.__plotConfidenceBand(plotter, x, y)
        plotter.lineSeries(x, y, xLabel=self._xLabel, yLabel=self._yLabel, title=self._title, style=self.style)

    def accept(self, seriesVisitor: SeriesVisitor) -> None:
        seriesVisitor.visitLineSeries(self)

    def __getPlotValues(self) -> tuple:
        filteredX, filteredY, filteredMeta = self.__removeNonNumberEntries()
        if len(filteredX) == 0:
            return list(), list(), list()

        filteredX, filteredY, filteredMeta = self.__sortValuesByX(filteredX, filteredY, filteredMeta)
        self.__xValues = filteredX
        self.__yValues = filteredY
        self._metaData = filteredMeta
        filteredX, filteredY = self.__filterValues(self.__xValues, self.__yValues, self._metaData)
        return filteredX, filteredY, filteredMeta

    def __removeNonNumberEntries(self) -> tuple:
        indexesToRemove = self.__determineIndexesToRemove()
        filteredX = list(self.xValues)
        filteredY = list(self.yValues)
        filteredMeta = list(self._metaData)
        for index in indexesToRemove:
            if index < len(filteredX):
                filteredX.pop(index)

            if index < len(filteredY):
                filteredY.pop(index)

            if index < len(filteredMeta):
                filteredMeta.pop(index)

        return filteredX, filteredY, filteredMeta

    def __determineIndexesToRemove(self) -> List[int]:
        xIndexesToRemove = self.__getNonNumberIndexes(self.xValues)
        yIndexesToRemove = self.__getNonNumberIndexes(self.yValues)

        combinedIndexes = xIndexesToRemove.union(yIndexesToRemove)
        return list(sorted(combinedIndexes, reverse=True))

    def __getNonNumberIndexes(self, entries: List) -> set:
        nonNumberEntries = set()
        for index in range(len(entries)):
            entry = entries[index]
            if not isNumber(entry):
                nonNumberEntries.add(index)

        return nonNumberEntries

    def __filterValues(self, x, y, meta) -> tuple:
        if len(self._filters) == 0 or len(meta) == 0:
            filteredX = x
            filteredY = y
            return filteredX, filteredY

        filteredX = list()
        filteredY = list()

        for i in range(len(meta)):
            if i >= len(x) or i >= len(y):
                break

            shouldAdd: bool = True
            for rowFilter in self._filters:
                shouldAdd = shouldAdd and rowFilter.appliesToIndex(self, i)

            if shouldAdd:
                filteredX.append(x[i])
                filteredY.append(y[i])

        return filteredX, filteredY

    def __sortValuesByX(self, x, y, meta) -> tuple:
        zipped = None
        sortedX, sortedY, sortedMeta = (list(), list(), list())
        if len(meta) > 0:
            zipped = zip(x, y, meta)
            sortedX, sortedY, sortedMeta = list(zip(*sorted(zipped)))
        else:
            zipped = zip(x, y)
            sortedX, sortedY = list(zip(*sorted(zipped)))

        return sortedX, sortedY, sortedMeta

    def __plotConfidenceBand(self, plotter: Plotter, xValues: list, yValues: list) -> None:
        if self.__confidenceBand > 0:
            lower = [y * (1 - self.__confidenceBand) for y in yValues]
            upper = [y * (1 + self.__confidenceBand) for y in yValues]

            if len(self.style) > 0:
                plotter.fillArea(xValues, lower, upper, alpha=0.3, color=self.style[0])
            else:
                plotter.fillArea(xValues, lower, upper, alpha=0.3)

            xText = xValues[len(xValues) - 1] * 0.9
            yText = upper[len(upper) - 1]
            plotter.text(xText, yText, str(self.__confidenceBand * 100) + "%")

    @property
    def xValues(self) -> list:
        """Returns the x values for the series."""

        return self.__xValues

    @xValues.setter
    def xValues(self, value: list) -> None:
        """Sets the x values for the series."""

        self.__xValues = value

    @property
    def yValues(self) -> list:
        """Returns the y values for the series."""

        return self.__yValues

    @yValues.setter
    def yValues(self, value: list) -> None:
        """Sets the y values for the series."""

        self.__yValues = value

    @property
    def confidenceBand(self) -> float:
        """Returns the confidence band value for the series. Percentage based on y values."""

        return self.__confidenceBand

    @confidenceBand.setter
    def confidenceBand(self, value: float) -> None:
        """Sets the confidence band value for the series. Percentage based on y values."""

        self.__confidenceBand = value

    @property
    def style(self) -> str:
        """Returns the style string for the series."""

        return self.__style

    @style.setter
    def style(self, value: str) -> None:
        """Sets the style string for the series."""

        self.__style = value

    def __assertAllEntriesAreNumbers(self, collection: Iterable):
        for item in collection:
            if not isNumber(item):
                raise NonNumberInPlotConfigError()


class BoxSeries(FilterableSeries):

    def __init__(self):
        super(BoxSeries, self).__init__()

        self.__data: List[List] = list()

    def plot(self, plotter: Plotter):
        data, meta = self.__filterData()
        plotter.boxplot(data, xLabels=meta, show_median_values=True)

    def accept(self, seriesVisitor: SeriesVisitor) -> None:
        seriesVisitor.visitBoxSeries(self)

    def __filterData(self):
        meta = list(self._metaData)
        indexesToRemove = set()
        for index in range(len(meta)):
            for listFilter in self._filters:
                if not listFilter.appliesToIndex(self, index):
                    indexesToRemove.add(index)

        sortedIndexes = list(sorted(indexesToRemove, reverse=True))
        data = list(self.__data)

        for index in sortedIndexes:
            meta.pop(index)
            data.pop(index)

        return data, meta

    @property
    def data(self) -> List[List]:
        return self.__data

    @data.setter
    def data(self, value: List[List]) -> None:
        self.__data = value


class TextPosition(Enum):
    Left = 0
    TopLeft = 1
    TopCenter = 2
    TopRight = 3
    Right = 4
    BottomRight = 5
    BottomCenter = 6
    BottomLeft = 7


class FillAreaSeries(Series):

    def __init__(self):
        super().__init__()
        self.__xLims: Tuple[float, float] = (0, 0)
        self.__yLims: Tuple[float, float] = (0, 0)
        self.__text: str = ""
        self.__textPos: TextPosition = TextPosition.Right
        self.__color: Tuple[float, float, float, float] = (0, 0, 0, 0.1)
        self.__textColor: Tuple[float, float, float, float] = (0, 0, 0, 1)

    def plot(self, plotter: Plotter):
        plotter.fillArea(self.__xLims, [self.__yLims[0], self.__yLims[0]], [self.__yLims[1], self.__yLims[1]], color=self.__color)
        self.plotText(plotter)

    def accept(self, seriesVisitor: SeriesVisitor) -> None:
        seriesVisitor.visitFillAreaSeries(self)

    def plotText(self, plotter: Plotter):
        if not self.text:
            return

        x = 0
        y = 0
        halignment = "center"
        valignment = "center"
        if self.textPosition == TextPosition.Left:
            x = self.xLimits[0]
            y = (self.yLimits[0] + self.yLimits[1]) / 2
            halignment = "left"
        elif self.textPosition == TextPosition.Right:
            x = self.xLimits[1]
            y = (self.yLimits[0] + self.yLimits[1]) / 2
            halignment = "right"
        elif self.textPosition == TextPosition.TopLeft:
            x = self.xLimits[0]
            y = self.yLimits[1]
            halignment = "left"
            valignment = "top"
        elif self.textPosition == TextPosition.TopCenter:
            x = (self.xLimits[0] + self.xLimits[1]) / 2
            y = self.yLimits[1]
            valignment = "top"
        elif self.textPosition == TextPosition.TopRight:
            x = self.xLimits[1]
            y = self.yLimits[1]
            halignment = "right"
            valignment = "top"
        elif self.textPosition == TextPosition.BottomLeft:
            x = self.xLimits[0]
            y = self.yLimits[0]
            halignment = "left"
            valignment = "bottom"
        elif self.textPosition == TextPosition.BottomCenter:
            x = (self.xLimits[0] + self.xLimits[1]) / 2
            y = self.yLimits[0]
            valignment = "bottom"
        elif self.textPosition == TextPosition.BottomRight:
            x = self.xLimits[1]
            y = self.yLimits[0]
            halignment = "right"
            valignment = "bottom"

        plotter.text(x, y, self.text, halignment=halignment, valignment=valignment, color=self.textColor)

    @property
    def xLimits(self) -> Tuple[float, float]:
        return self.__xLims

    @xLimits.setter
    def xLimits(self, value: Tuple[float, float]) -> None:
        self.__xLims = value

    @property
    def yLimits(self) -> Tuple[float, float]:
        return self.__yLims

    @yLimits.setter
    def yLimits(self, value: Tuple[float, float]) -> None:
        self.__yLims = value

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, value: str) -> None:
        self.__text = value

    @property
    def textPosition(self) -> TextPosition:
        return self.__textPos

    @textPosition.setter
    def textPosition(self, value: TextPosition) -> None:
        self.__textPos = value

    @property
    def textColor(self) -> Tuple[int, int, int, int]:
        return self.__textColor

    @textColor.setter
    def textColor(self, value: Tuple[int, int, int, int]) -> None:
        self.__textColor = value

    @property
    def color(self) -> Tuple[int, int, int, int]:
        return self.__color

    @color.setter
    def color(self, value: Tuple[int, int, int]) -> None:
        self.__color = value
