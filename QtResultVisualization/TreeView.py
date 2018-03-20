from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QWidget, QTreeView, QVBoxLayout, QPushButton

from QtResultVisualization.FilterView import FilterView
from QtResultVisualization.TreeModel import TreeModel
from ResultVisualization.FilterDialogPresenter import FilterDialogPresenter
from ResultVisualization.TreeViewItem import TreeViewItem


class TreeView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        vBox: QVBoxLayout = QVBoxLayout()

        i1: TreeViewItem = TreeViewItem("A")
        i2: TreeViewItem = TreeViewItem("B")
        i3: TreeViewItem = TreeViewItem("C")
        subItem: TreeViewItem = TreeViewItem("A2")

        i1.insert(subItem, 0)

        self.__treeView: QTreeView = QTreeView()
        treeModel = TreeModel()
        self.__itemChangedHandler = ItemCheckHandler(treeModel, self.__treeView)
        self.__itemChangedHandler.addToTreeItem(i1)
        self.__itemChangedHandler.addToTreeItem(subItem)
        self.__itemChangedHandler.addToTreeItem(i2)
        self.__itemChangedHandler.addToTreeItem(i3)

        treeModel.insertItem(i1, QModelIndex(), 0)
        treeModel.insertItem(i2, QModelIndex(), 1)
        treeModel.insertItem(i3, QModelIndex(), 2)

        self.setLayout(vBox)

        self.__treeView.setModel(treeModel)

        vBox.addWidget(self.__treeView)

        self.__filterButton = QPushButton()
        self.__filterButton.setText("Filter")
        self.__filterButton.clicked.connect(self.createFilterDialog().showDialog)

        vBox.addWidget(self.__filterButton)

    def createFilterDialog(self) -> FilterDialogPresenter:
        view: FilterView = FilterView()
        presenter: FilterDialogPresenter = FilterDialogPresenter(view)
        view.setPresenter(presenter)
        return presenter

class ItemCheckHandler:

    def __init__(self, treeModel: TreeModel, treeView: QTreeView):
        self.__treeModel = treeModel
        self.__origin: TreeViewItem = None
        self.__upAllowed: bool = False
        self.__treeView: QTreeView = treeView

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
