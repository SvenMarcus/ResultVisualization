import sys

from PyQt5.QtWidgets import QApplication

from QtResultVisualization.QtTreeView import QtTreeView
from ResultVisualization.TreeFileLoader.TreeViewFileLoader import TreeViewFileLoader
from ResultVisualization.TreeViewController import TreeViewController

path1 = "./Experiments/PRS1_Door3_FDS607/Results/Results_Export.csv"
path2 = "./Experiments/PRS1_Door4_FDS607/Results/Results_Export.csv"


app = QApplication(sys.argv)

treeView = QtTreeView()

treeViewController: TreeViewController = TreeViewController(treeView)
loader: TreeViewFileLoader = TreeViewFileLoader(treeViewController)
loader.readFiles([path1, path2])

treeView.show()

# item: TreeItem = CategoryItem("Test")
# index: TreeIndex = TreeIndex()
#
# subItem: TreeItem = TreeItem("SubTest")
# subIndex: TreeIndex = TreeIndex(index, 0)
#
# treeViewController.insertItem(item, index)
# treeViewController.insertItem(subItem, subIndex)
sys.exit(app.exec_())
