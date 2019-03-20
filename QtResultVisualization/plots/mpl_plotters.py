from typing import Iterable, List

from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Axes, Figure

from QtResultVisualization.plots.mpl_area_plotter import MplAreaPlot
from QtResultVisualization.plots.mpl_boxplot_plotter import MplBoxPlot
from QtResultVisualization.plots.mpl_line_plotter import MplLinePlot
from QtResultVisualization.plots.mpl_text_plotter import MplTextPlot
from ResultVisualization.Plot import Plotter


class MatplotlibPlotter(Plotter):

    def __init__(self, canvas: FigureCanvas):
        self.__canvas: FigureCanvas = canvas
        self.__figure: Figure = canvas.figure
        self.__axes: Axes = None
        self.__boxPlot = MplBoxPlot(self.__figure)
        self.__linePlot = MplLinePlot(self.__figure)
        self.__areaPlot = MplAreaPlot(self.__figure)
        self.__textPlot = MplTextPlot(self.__figure)

    def resetPlotData(self) -> None:
        self.__boxPlot = MplBoxPlot(self.__figure)
        self.__linePlot = MplLinePlot(self.__figure)
        self.__areaPlot = MplAreaPlot(self.__figure)
        self.__textPlot = MplTextPlot(self.__figure)

    def finishPlot(self) -> None:
        if self.__boxPlot.canDraw():
            self.__boxPlot.draw()
        if self.__linePlot.canDraw():
            self.__linePlot.draw()
        if self.__areaPlot.canDraw():
            self.__areaPlot.draw()
        if self.__textPlot.canDraw():
            self.__textPlot.draw()

        self.update()

    def clear(self) -> None:
        self.__figure.clear()

    def lineSeries(self, xValues: Iterable, yValues: Iterable, **kwargs) -> None:
        title: str = ""
        style: str = "-"
        xLabel: str = "-"
        yLabel: str = "-"
        for key, value in kwargs.items():
            if key == "xLabel":
                xLabel = value
            elif key == "yLabel":
                yLabel = value
            elif key == "title":
                title = value
            elif key == "style":
                style = value

        self.__linePlot.addLineData(xValues, yValues, style, title, xLabel, yLabel)

    def boxplot(self, data, **kwargs):
        xLabels: List[str] = []
        group: str = ""
        if "xLabels" in kwargs.keys():
            xLabels = kwargs["xLabels"]
        if "group" in kwargs.keys():
            group = kwargs["group"]

        self.__boxPlot.addBoxplotData(data, xLabels, group)

    def fillArea(self, xValues: Iterable, lowerYValues: Iterable, upperYValues: Iterable, **kwargs) -> None:
        color = None
        alpha = 1
        for key, value in kwargs.items():
            if key == "color":
                color = value
            if key == "alpha":
                alpha = value
        self.__areaPlot.addArea(xValues, lowerYValues, upperYValues, color, alpha)

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

        self.__textPlot.addTextBlock(x, y, text, halignment, valignment, color)

    def update(self) -> None:
        self.__canvas.draw_idle()
