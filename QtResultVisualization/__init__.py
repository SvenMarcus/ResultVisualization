import sys

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QApplication, QTreeView, QMainWindow, QHBoxLayout, QWidget, QSplitter

from QtResultVisualization.GraphWindow import GraphWindow
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
treeView.setMinimumWidth(200)

graphWindow = GraphWindow()
graphWindow.setMinimumWidth(800)
graphWindow.setMinimumHeight(600)

splitter = QSplitter()
splitter.addWidget(treeView)
splitter.addWidget(graphWindow)


window.setCentralWidget(splitter)
window.show()
sys.exit(app.exec_())
