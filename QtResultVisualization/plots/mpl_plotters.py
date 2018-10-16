from numbers import Number
from typing import Iterable, List, Tuple

from matplotlib.ticker import StrMethodFormatter
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Axes, Figure

from ResultVisualization.Plot import Plotter


class MatplotlibPlotter(Plotter):

    def __init__(self, canvas: FigureCanvas):
        self.__canvas: FigureCanvas = canvas
        self.__figure: Figure = canvas.figure
        self.__axes: Axes = self.__figure.add_subplot(111)

        self.__lineData: List[Tuple] = list()
        self.__boxData: List[Iterable[Number]] = list()
        self.__title = ""
        self.__xLabel = ""
        self.__yLabel = ""
        self.__xTicks = []
        self.__showMedianValues = False

    def resetPlotData(self) -> None:
        self.__lineData = list()
        self.__boxData = list()
        self.__title = ""
        self.__xLabel = ""
        self.__yLabel = ""
        self.__xTicks = []
        self.__showMedianValues = False

    def finishPlot(self) -> None:
        if len(self.__boxData) > 0:
            boxplots = self.__axes.boxplot(self.__boxData)
            for line in boxplots["medians"]:
                x, y = line.get_xydata()[1]
                self.__axes.text(x, y, '%.1f' % y,
                                 horizontalalignment='right')

            self.__axes.set_xticklabels(self.__xTicks)
        elif len(self.__lineData) > 0:
            for lineData in self.__lineData:
                self.__axes.plot(
                    lineData[0], lineData[1], lineData[2], label=lineData[3])
            self.__axes.set_xlabel(self.__xLabel)
            self.__axes.set_ylabel(self.__yLabel)
            self.__axes.legend(loc=4)

        self.__axes.grid(True)
        self.__axes.get_yaxis().set_major_formatter(
            StrMethodFormatter("{x:.2f}"))
        self.update()

    def clear(self) -> None:
        self.__axes.clear()

    def lineSeries(self, xValues: Iterable, yValues: Iterable, **kwargs) -> None:
        title: str = ""
        style: str = "-"
        for key, value in kwargs.items():
            if key == "xLabel":
                self.__xLabel = self.__buildLabel(self.__xLabel, value)
            elif key == "yLabel":
                self.__yLabel = self.__buildLabel(self.__yLabel, value)
            elif key == "title":
                title = value
            elif key == "style":
                style = value

        if not self.__validate(style):
            style = "-"

        self.__lineData.append((xValues, yValues, style, title))

    def __buildLabel(self, currentLabel: str, newValue: str) -> str:
        if currentLabel is None:
            currentLabel = ""

        if currentLabel == newValue:
            return currentLabel

        if len(currentLabel) > 0:
            currentLabel += " // "

        return currentLabel + newValue

    def __validate(self, style: str) -> bool:
        if not style:
            return False

        if style[0] in {'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'}:
            style = style[1:]

        markers = {
            '.', ',', 'o', 'v',
            '^', '<', '>', '1',
            '2', '3', '4', 's',
            'p', '*', 'h', 'H',
            '+', 'x', 'D', 'd',
            '|', '_'
        }

        for marker in markers:
            if style[0:len(marker)] == marker:
                style = style[len(marker):]
                break

        lineStyles = [
            '--', '-.', '-', ':'
        ]

        for lineStyle in lineStyles:
            tmp = style[0:len(lineStyle)]

            if tmp == lineStyle:
                style = style[len(lineStyle):]
                break

        return not style

    def boxplot(self, data, **kwargs):
        xLabels: List[str] = []
        if "xLabels" in kwargs.keys():
            xLabels = kwargs["xLabels"]
        if "show_median_values" in kwargs.keys():
            self.__showMedianValues = kwargs["show_median_values"]

        self.__boxData.extend(data)
        self.__xTicks.extend(xLabels)

    def fillArea(self, xValues: Iterable, lowerYValues: Iterable, upperYValues: Iterable, **kwargs) -> None:
        alpha = 1
        color = None
        for key, value in kwargs.items():
            if key == "alpha":
                alpha = value
            if key == "color":
                color = value

        if color is None:
            self.__axes.fill_between(
                xValues, lowerYValues, upperYValues, alpha=alpha)
        else:
            canPlot = True

            if isinstance(color, str):
                if color[0] not in {'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'}:
                    canPlot = False

            if canPlot:
                self.__axes.fill_between(
                    xValues, lowerYValues, upperYValues, facecolor=color, alpha=alpha)

    def text(self, x: float, y: float, text: str, **kwargs) -> None:
        halignment = "center"
        valignment = "center"
        color = (0, 0, 0, 1)
        for key, value in kwargs.items():
            if key == "halignment":
                halignment = value
            elif key == "valignment":
                valignment = value
            elif key == "color":
                color = value

        self.__axes.text(x, y, text, horizontalalignment=halignment,
                         verticalalignment=valignment, color=color)

    def update(self) -> None:
        self.__canvas.draw_idle()
