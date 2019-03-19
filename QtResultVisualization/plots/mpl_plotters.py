from numbers import Number
from typing import Iterable, List, Tuple

from matplotlib import pyplot
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Axes, Figure
from matplotlib.ticker import StrMethodFormatter

from ResultVisualization.Plot import Plotter


class BoxPlotData:
    values = list()
    labels = list()
    group = ""


class MatplotlibPlotter(Plotter):

    def __init__(self, canvas: FigureCanvas):
        self.__canvas: FigureCanvas = canvas
        self.__figure: Figure = canvas.figure
        self.__axes: Axes = None

        self.__lineData: List[Tuple] = list()
        self.__boxData: List[Iterable[Number]] = list()
        self.__groups: List[str] = list()
        self.__title = ""
        self.__xLabel = ""
        self.__yLabel = ""
        self.__xTicks = []
        self.__showMedianValues = False
        prop_cycle = pyplot.rcParams['axes.prop_cycle']
        self.__colorRotation = prop_cycle.by_key()['color']

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
            mergedBoxData = self.__mergeBoxplotData()
            numCols = len(mergedBoxData.keys())
            allAxes = self.__figure.subplots(nrows=1, ncols=numCols, sharex='all', sharey='all')
            axIndex = 0

            xTickLabels = list()
            groupColorLookup = self.__createGroupColorLookup()

            for key, boxplotData in mergedBoxData.items():
                xTickLabels.append(key)
                ax: Axes = allAxes[axIndex]
                boxplots = ax.boxplot(list(boxplotData["values"]), patch_artist=True)
                ax.set_xlabel(key)
                ax.get_yaxis().set_major_formatter(
                    StrMethodFormatter("{x:.2f}"))
                axIndex += 1
                self.__plotMedianValues(ax, boxplots)
                self.__colorBoxes(boxplots, boxplotData["groups"], groupColorLookup)

        elif len(self.__lineData) > 0:
            self.__axes = self.__figure.add_subplot(111)
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

    def __plotMedianValues(self, ax, boxplots):
        for line in boxplots["medians"]:
            x, y = line.get_xydata()[1]
            ax.text(x, y, '%.1f' % y,
                    horizontalalignment='right')

    def __colorBoxes(self, boxplots, groups, groupColorLookup):
        for index, box in enumerate(boxplots["boxes"]):
            group = groups[index]
            if group:
                color = groupColorLookup[group]
                box.set_facecolor(color)

    def __createGroupColorLookup(self):
        groupColorLookup = dict()
        colorIndex = 0
        for group in self.__groups:
            if group and group not in groupColorLookup.keys():
                groupColorLookup[group] = self.__colorRotation[colorIndex]
                colorIndex += 1
                if colorIndex >= len(self.__colorRotation):
                    colorIndex = 0

        return groupColorLookup

    def __mergeBoxplotData(self) -> dict:
        mergedData = dict()

        for index, xLabel in enumerate(self.__xTicks):
            if xLabel not in mergedData.keys():
                mergedData[xLabel] = {
                    "values": list(),
                    "groups": list()
                }

            mergedData[xLabel]["values"].append(list(self.__boxData[index]))
            mergedData[xLabel]["groups"].append(self.__groups[index])

        return mergedData

    def clear(self) -> None:
        self.__figure.clear()

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
        group: str = "a"
        if "xLabels" in kwargs.keys():
            xLabels = kwargs["xLabels"]
        if "show_median_values" in kwargs.keys():
            self.__showMedianValues = kwargs["show_median_values"]
        if "group" in kwargs.keys():
            group = kwargs["group"]

        self.__boxData.extend(data)
        self.__xTicks.extend(xLabels)
        self.__groups.extend([group for _ in range(0, len(list(data)))])

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
