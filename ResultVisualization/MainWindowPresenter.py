from ResultVisualization.TreeView import TreeView


class MainWindowPresenter:

    def __init__(self):
        self.__treeView = None

    @property
    def treeView(self) -> TreeView:
        return self.__treeView

    @treeView.setter
    def treeView(self, value: TreeView) -> None:
        self.__treeView = value
