from matplotlib import pyplot
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Patch
from matplotlib.ticker import StrMethodFormatter


class MplBoxPlot:

    def __init__(self, figure: Figure):
        self.__figure: Figure = figure
        self.__groups = list()
        self.__boxData = list()
        self.__xTicks = list()
        self.__showMedianValues = False
        prop_cycle = pyplot.rcParams['axes.prop_cycle']
        self.__colorRotation = prop_cycle.by_key()['color']

    def addBoxplotData(self, data, xticks, group=""):
        self.__boxData.extend(data)
        self.__xTicks.extend(xticks)
        self.__groups.extend([group for _ in range(0, len(list(data)))])

    def canDraw(self):
        return self.__figure is not None and len(self.__boxData) > 0

    def draw(self):
        mergedBoxData = self.__mergeBoxplotData()
        numCols = len(mergedBoxData.keys())
        allAxes = self.__figure.subplots(nrows=1, ncols=numCols, sharey='all')
        self.__figure.subplots_adjust(wspace=0)
        axIndex = 0
        groupColorLookup = self.__createGroupColorLookup()
        for key, boxplotData in mergedBoxData.items():
            ax: Axes = allAxes[axIndex]
            self.__configureAxes(ax, key)
            self.__drawBox(ax, boxplotData, groupColorLookup)
            axIndex += 1

        ax = allAxes[axIndex - 1]
        self.__createLegend(ax, groupColorLookup)

    def __drawBox(self, ax, boxplotData, groupColorLookup):
        boxplots = ax.boxplot(list(boxplotData["values"]), patch_artist=True, positions=range(1, len(boxplotData["values"]) + 1))
        self.__plotMedianValues(ax, boxplots)
        self.__colorBoxes(boxplots, boxplotData["groups"], groupColorLookup)

    def __createLegend(self, ax, groupColorLookup):
        group_set = set().union(self.__groups)
        group_colors = [Patch(color=groupColorLookup[group]) for group in group_set]
        ax.legend(group_colors, group_set, loc=4)

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

    @staticmethod
    def __configureAxes(ax, key):
        ax.set_xlabel(key)
        ax.get_yaxis().set_major_formatter(
            StrMethodFormatter("{x:.2f}"))

    @staticmethod
    def __plotMedianValues(ax, boxplots):
        for line in boxplots["medians"]:
            x, y = line.get_xydata()[1]
            ax.text(x, y, '%.1f' % y,
                    horizontalalignment='right')

    @staticmethod
    def __colorBoxes(boxplots, groups, groupColorLookup):
        for index, box in enumerate(boxplots["boxes"]):
            group = groups[index]
            if group:
                color = groupColorLookup[group]
                box.set_facecolor(color)

