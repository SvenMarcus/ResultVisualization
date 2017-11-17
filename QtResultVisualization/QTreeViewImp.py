from PyQt5.QtWidgets import QTreeWidget

from ResultVisualization.TreeView import TreeView


class QTreeViewImp(TreeView):
    def __init__(self, treeWidget: QTreeWidget = None):
        TreeView.__init__(self)
        self.__treeWidget: QTreeWidget = treeWidget or QTreeWidget()

    def getWidget(self) -> QTreeWidget:
        return self.__treeWidget

    def _addToView(self, viewTreeNode) -> None:
        self.__treeWidget.addTopLevelItem(viewTreeNode.getWidgetItem())

    def _removeFromView(self, index: int) -> None:
        self.__treeWidget.takeTopLevelItem(index)
