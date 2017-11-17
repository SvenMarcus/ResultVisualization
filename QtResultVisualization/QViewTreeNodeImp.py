from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

from ResultVisualization import ViewTreeNode
from ResultVisualization.TreeNodes import TreeNode


class QViewTreeNodeImp(ViewTreeNode):
    def __init__(self, treeNode: TreeNode):
        ViewTreeNode.__init__(self, treeNode)
        self.__treeWidgetItem = QTreeWidgetItem()
        self.__treeWidgetItem.setCheckState(0, Qt.Unchecked)
        self.__treeWidgetItem.setText(0, treeNode.get_text())

    def getWidgetItem(self) -> QTreeWidgetItem:
        return self.__treeWidgetItem

    def _addToView(self, viewTreeNode) -> None:
        self.__treeWidgetItem.addChild(viewTreeNode.getWidgetItem())

    def _removeFromView(self, index: int) -> None:
        self.__treeWidgetItem.takeChild(index)

    def _makeViewTreeNode(self, content: TreeNode):
        return QViewTreeNodeImp(content)

    def _setCheckStateInView(self, state: bool) -> None:
        if state:
            checkState = Qt.Checked
        else:
            checkState = Qt.Unchecked
        self.__treeWidgetItem.checkState(checkState)
