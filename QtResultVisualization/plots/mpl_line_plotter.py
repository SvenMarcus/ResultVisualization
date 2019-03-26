from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.ticker import StrMethodFormatter

from ResultVisualization import Style


class MplLinePlot:

    def __init__(self, figure: Figure):
        self.__figure: Figure = figure
        self.__axes: Axes = None
        self.__lineData = list()
        self.__xLabel = ""
        self.__yLabel = ""

    def addLineData(self, xValues, yValues, style="-", title="", xLabel="", yLabel=""):
        if not Style.validate(style):
            style = "-"

        self.__lineData.append((xValues, yValues, style, title))
        self.__xLabel = self.__buildLabel(self.__xLabel, xLabel)
        self.__yLabel = self.__buildLabel(self.__yLabel, yLabel)

    def canDraw(self):
        return self.__figure is not None and len(self.__lineData) > 0

    def draw(self):
        self.__axes = self.__figure.add_subplot(111) if len(self.__figure.axes) == 0 else self.__figure.axes[0]
        for lineData in self.__lineData:
            self.__axes.plot(
                lineData[0],
                lineData[1],
                lineData[2],
                label=lineData[3]
            )
        self.__configurePlot()

    def __configurePlot(self):
        self.__axes.set_xlabel(self.__xLabel)
        self.__axes.set_ylabel(self.__yLabel)
        self.__axes.legend(loc=4)
        self.__axes.grid(True)
        self.__axes.get_yaxis().set_major_formatter(
            StrMethodFormatter("{x:.2f}"))

    @staticmethod
    def __buildLabel(currentLabel: str, newValue: str) -> str:
        if currentLabel is None:
            currentLabel = ""

        if currentLabel == newValue:
            return currentLabel

        if len(currentLabel) > 0:
            currentLabel += " // "

        return currentLabel + newValue
