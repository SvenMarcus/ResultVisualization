import sys

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QApplication, QTreeView, QMainWindow

from QtResultVisualization.TreeModel import TreeModel
from ResultVisualization.TreeViewItem import TreeViewItem

i1 = TreeViewItem("A")
i2 = TreeViewItem("B")
i3 = TreeViewItem("C")
i1.insert(TreeViewItem("A2"), 0)

treeModel = TreeModel()
treeModel.insertItem(i1, QModelIndex(), 0)
treeModel.insertItem(i2, QModelIndex(), 1)
treeModel.insertItem(i3, QModelIndex(), 2)

app = QApplication(sys.argv)
window = QMainWindow()
treeView = QTreeView()
treeView.setModel(treeModel)
window.setCentralWidget(treeView)
window.show()
sys.exit(app.exec_())
