import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter

from QtResultVisualization.GraphWindow import GraphWindow
from QtResultVisualization.TreeModel import TreeModel
from QtResultVisualization.TreeView import TreeView

app = QApplication(sys.argv)
window = QMainWindow()

graphWindow = GraphWindow()
graphWindow.setMinimumWidth(800)
graphWindow.setMinimumHeight(600)

treeView = TreeView()
treeView.setMinimumWidth(200)

splitter = QSplitter()
splitter.addWidget(treeView)
splitter.addWidget(graphWindow)


window.setCentralWidget(splitter)
window.show()
sys.exit(app.exec_())
