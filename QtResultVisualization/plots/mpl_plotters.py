from typing import Iterable, List, Tuple

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
                self.__axes.plot(lineData[0], lineData[1], label=lineData[2])
            self.__axes.set_xlabel(self.__xLabel)
            self.__axes.set_ylabel(self.__yLabel)
        self.update()

    def clear(self) -> None:
        self.__axes.clear()

    def lineSeries(self, xValues: Iterable, yValues: Iterable, **kwargs) -> None:
        title: str = ""
        for key, value in kwargs.items():
            if key == "xLabel":
                xLabel: str = self.__axes.get_xlabel()
                self.__xLabel = self.__buildLabel(self.__xLabel, value)
            elif key == "yLabel":
                self.__yLabel = self.__buildLabel(self.__yLabel, value)
            elif key == "title":
                title = value

        self.__lineData.append((xValues, yValues, title))

    def __buildLabel(self, currentLabel: str, newValue: str) -> str:
        if currentLabel is None:
            currentLabel = ""

        if currentLabel == newValue:
            return currentLabel

        if len(currentLabel) > 0:
            currentLabel += " // "

        return currentLabel + newValue

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
        for key, value in kwargs.items():
            if key == "alpha":
                alpha = value

        self.__axes.fill_between(
            xValues, lowerYValues, upperYValues, alpha=alpha)

    def text(self, x: float, y: float, text: str) -> None:
        self.__axes.text(x, y, text)

    def update(self) -> None:
        self.__canvas.draw_idle()
