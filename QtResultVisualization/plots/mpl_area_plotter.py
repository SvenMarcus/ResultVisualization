from matplotlib.figure import Figure


class MplAreaPlot:

    def __init__(self, figure: Figure):
        self.__figure = figure
        self.__axes = None
        self.__areas = list()

    def addArea(self, xValues, lowerYValues, upperYValues, color=None, alpha=1):
        self.__areas.append((xValues, lowerYValues, upperYValues, color, alpha))

    def canDraw(self):
        return self.__figure is not None and len(self.__areas) > 0

    def draw(self):
        self.__axes = self.__figure.add_subplot(111) if len(self.__figure.axes) == 0 else self.__figure.axes[0]
        for area in self.__areas:
            xValues = area[0]
            lowerYValues = area[1]
            upperYValues = area[2]
            color = area[3]
            alpha = area[4]

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
                        xValues,
                        lowerYValues,
                        upperYValues,
                        facecolor=color
                    )
