from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.axes import Axes
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from QtResultVisualization.plots.mpl_plotters import MatplotlibPlotter
from ResultVisualization.Plot import Graph, PlotSettings


class CustomMplNavigationToolbar(NavigationToolbar):

    def __init__(self, canvas, parent):
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'), ('Back', 'Back to previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'), (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'), (None, None, None, None),
            ('Save', 'Save the figure', 'filesave', 'save_figure')
        )
        super().__init__(canvas, parent)


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
        navBar = CustomMplNavigationToolbar(self.__canvas, self.__widget)

        layout: QVBoxLayout = QVBoxLayout(self.__widget)
        self.__widget.setLayout(layout)

        layout.addWidget(navBar)
        layout.addWidget(self.__canvas)

    def _setTitleInView(self, title: str):
        self.__canvas.figure.suptitle(title)

    def getFigureCanvas(self) -> FigureCanvas:
        return self.__canvas

    def getWidget(self) -> QWidget:
        return self.__widget

    def _setPlotSettingsInView(self, plotSettings: PlotSettings) -> None:
        ax: Axes
        for ax in self.__canvas.figure.axes:
            if plotSettings.minX != plotSettings.maxX:
                ax.set_xbound(plotSettings.minX, plotSettings.maxX)
            if plotSettings.minY != plotSettings.maxY:
                ax.set_ybound(plotSettings.minY, plotSettings.maxY)
