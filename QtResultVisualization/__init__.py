import sys

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QApplication, QTreeView, QMainWindow

from QtResultVisualization.TreeModel import TreeModel
from ResultVisualization.TreeNodes import TreeItem

i1 = TreeItem("A")
i2 = TreeItem("B")
i3 = TreeItem("C")

treeModel = TreeModel()
treeModel.insertItem(i1, QModelIndex(), 0)
treeModel.insertItem(i2, QModelIndex(), 1)
treeModel.insertItem(i3, QModelIndex(), 2)

i1.insert(TreeItem("A2"), 0)

app = QApplication(sys.argv)
window = QMainWindow()
treeView = QTreeView()
treeView.setModel(treeModel)
window.setCentralWidget(treeView)
window.show()
sys.exit(app.exec_())
