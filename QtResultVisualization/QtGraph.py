from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from QtResultVisualization.plots.mpl_plotters import MatplotlibPlotter
from ResultVisualization.Plot import Graph


class DuplicatePlotConfigError(RuntimeError):

    def __init__(self):
        super().__init__()


class QtGraph(Graph):

    def __init__(self, parent: QWidget = None):
        self.__widget: QWidget = None
        self.__canvas: FigureCanvas = None
        self.__initUI(parent)
        self.__axes = self.__canvas.figure.add_subplot(111)
        super().__init__(MatplotlibPlotter(self.__canvas))

    def __initUI(self, parent: QWidget) -> None:
        self.__widget = QWidget(parent)
        self.__canvas = FigureCanvas(Figure())
        navBar = NavigationToolbar(self.__canvas, self.__widget)

        layout: QVBoxLayout = QVBoxLayout(self.__widget)
        self.__widget.setLayout(layout)

        layout.addWidget(navBar)
        layout.addWidget(self.__canvas)

    def getWidget(self) -> QWidget:
        return self.__widget

    def getFigureCanvas(self) -> FigureCanvas:
        return self.__canvas
