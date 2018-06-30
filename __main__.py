import sys

from PyQt5.QtWidgets import QApplication
from QtResultVisualization.QtTreeView import QtTreeView

from ResultVisualization.Reader.IbmbExperimentReader import IbmbExperimentReader
from ResultVisualization.TreeItem import TreeItem, CategoryItem
from ResultVisualization.TreeView import TreeIndex
from ResultVisualization.TreeViewController import TreeViewController


def insertIntoTree(dict_, index=None):
    for key in dict_:
        tree_index = TreeIndex(index)
        if type(dict_[key]) is dict:
            treeViewController.insertItem(CategoryItem(key), tree_index)
            insertIntoTree(dict_[key], tree_index)
        else:
            treeViewController.insertItem(TreeItem(key), tree_index)


resultReader = IbmbExperimentReader()
path1 = "./Experiments/PRS1_Door3_FDS607/Results/Results_Export.csv"
path2 = "./Experiments/PRS1_Door4_FDS607/Results/Results_Export.csv"
d = resultReader.readMany([path1, path2])

app = QApplication(sys.argv)

treeView = QtTreeView()

treeViewController: TreeViewController = TreeViewController(treeView)
treeView.show()

insertIntoTree(d)

# item: TreeItem = CategoryItem("Test")
# index: TreeIndex = TreeIndex()
#
# subItem: TreeItem = TreeItem("SubTest")
# subIndex: TreeIndex = TreeIndex(index, 0)
#
# treeViewController.insertItem(item, index)
# treeViewController.insertItem(subItem, subIndex)
sys.exit(app.exec_())
