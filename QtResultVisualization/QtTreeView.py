from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QWidget, QTreeView, QVBoxLayout

from QtResultVisualization.QtTreeModel import QtTreeModel
from QtResultVisualization.TreeViewItem import TreeViewItem
from ResultVisualization.TreeItem import TreeItem
from ResultVisualization.TreeView import TreeView, TreeIndex


class QtTreeView(TreeView, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        vBox: QVBoxLayout = QVBoxLayout()

        self.__treeView: QTreeView = QTreeView()
        self.__treeModel = QtTreeModel()
        self.setLayout(vBox)
        self.__treeView.setModel(self.__treeModel)

        vBox.addWidget(self.__treeView)

    def insertItem(self, item: TreeItem, index: TreeIndex, childPos: int):
        qModelIndex: QModelIndex = self.__treeModel.convertToQModelIndex(index)
        self.__treeModel.insertItem(TreeViewItem(item.text), qModelIndex, childPos)

    def deleteItem(self, index: TreeIndex):
        pass


class ItemCheckHandler:

    def __init__(self):
        self.__origin: TreeViewItem = None
        self.__upAllowed: bool = False

    def addToTreeItem(self, item: TreeViewItem):
        item.checkStateChanged.append(self.__item_changed_handler)

    def __item_changed_handler(self, item: TreeViewItem, checkState: bool) -> None:
        self.__set_origin(item)
        self.__check_children(item)
        self.__check_parents(item)
        self.__reset_check_helpers(item)

    def __set_origin(self, item: TreeViewItem) -> None:
        if self.__origin is None:
            self.__origin = item

    def __check_children(self, item: TreeViewItem) -> None:
        if not self.__upAllowed:
            for i in range(0, item.getChildCount()):
                child: TreeViewItem = item.getChild(i)
                child.checked = item.checked

    def __check_parents(self, item: TreeViewItem) -> None:
        if self.__origin == item:
            self.__upAllowed = True

        if self.__upAllowed:
            parent: TreeViewItem = item.parent
            isTopLevel = parent.parent is None
            if not isTopLevel:
                allChildrenSelected = self.__all_children_selected(parent)
                parent.checked = allChildrenSelected

    def __reset_check_helpers(self, item) -> None:
        if self.__origin == item:
            self.__origin = None
            self.__upAllowed = False

    @staticmethod
    def __all_children_selected(item: TreeViewItem) -> bool:
        for i in range(0, item.getChildCount()):
            child: TreeViewItem = item.getChild(i)
            if not child.checked:
                return False
        return True
