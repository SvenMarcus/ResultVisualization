import sys

from PyQt5.QtWidgets import QApplication

from QtResultVisualization.QtTreeView import QtTreeView
# window = QMainWindow()
#
# graphWindow = GraphWindow()
# graphWindow.setMinimumWidth(800)
# graphWindow.setMinimumHeight(600)
#
# treeView = QtTreeView()
# treeView.setMinimumWidth(200)
#
# splitter = QWidget()
# layout = QHBoxLayout()
# splitter.setLayout(layout)
# layout.addWidget(treeView)
# layout.addWidget(graphWindow)
#
#
# window.setCentralWidget(splitter)
# window.show()
#
# # graphWindow.show()
# sys.exit(app.exec_())
from ResultVisualization.TreeItem import TreeItem
from ResultVisualization.TreeView import TreeIndex
from ResultVisualization.TreeViewController import TreeViewController

app = QApplication(sys.argv)

treeView = QtTreeView()

treeViewController: TreeViewController = TreeViewController(treeView)
treeView.show()

item: TreeItem = TreeItem("Test")
index: TreeIndex = TreeIndex()


treeViewController.insertItem(item, index, 0)
sys.exit(app.exec_())