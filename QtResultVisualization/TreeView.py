from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QWidget, QTreeView, QVBoxLayout, QPushButton

from QtResultVisualization import TreeModel
from ResultVisualization.TreeViewItem import TreeViewItem


class TreeView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        vBox: QVBoxLayout = QVBoxLayout()

        i1 = TreeViewItem("A")
        i2 = TreeViewItem("B")
        i3 = TreeViewItem("C")
        i1.insert(TreeViewItem("A2"), 0)

        treeModel = TreeModel()
        treeModel.insertItem(i1, QModelIndex(), 0)
        treeModel.insertItem(i2, QModelIndex(), 1)
        treeModel.insertItem(i3, QModelIndex(), 2)

        self.setLayout(vBox)
        self.__treeView: QTreeView = QTreeView()
        self.__treeView.setModel(treeModel)

        vBox.addWidget(self.__treeView)

        self.__filterButton = QPushButton()
        self.__filterButton.setText("Filter")

        vBox.addWidget(self.__filterButton)

