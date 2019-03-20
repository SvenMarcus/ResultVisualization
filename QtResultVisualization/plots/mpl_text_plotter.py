from matplotlib.figure import Figure


class TextBlock:
    def __init__(self, x, y, text, hAlignment="center", vAlignment="center", color=(0, 0, 0, 1)):
        self.x = x
        self.y = y
        self.text = text
        self.hAlignment = "center"
        self.vAlignment = "center"
        self.color = (0, 0, 0, 1)


class MplTextPlot:

    def __init__(self, figure: Figure):
        self.__figure: Figure = figure
        self.__axes = None
        self.__textBlocks = list()

    def addTextBlock(self, x, y, text, hAlignment="center", vAlignment="center", color=(0, 0, 0, 1)):
        self.__textBlocks.append(TextBlock(x, y, text, hAlignment, vAlignment, color))

    def canDraw(self):
        return self.__figure is not None and len(self.__textBlocks) > 0

    def draw(self):
        self.__axes = self.__figure.add_subplot(111) if len(self.__figure.axes) == 0 else self.__figure.axes[0]
        for textBlock in self.__textBlocks:
            self.__axes.text(
                textBlock.x,
                textBlock.y,
                textBlock.text,
                horizontalalignment=textBlock.hAlignment,
                verticalalignment=textBlock.vAlignment,
                color=textBlock.color
            )
