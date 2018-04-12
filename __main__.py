import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout

from QtResultVisualization.GraphWindow import GraphWindow
from QtResultVisualization.QtTreeView import QtTreeView

app = QApplication(sys.argv)
window = QMainWindow()

graphWindow = GraphWindow()
graphWindow.setMinimumWidth(800)
graphWindow.setMinimumHeight(600)

treeView = QtTreeView()
treeView.setMinimumWidth(200)

splitter = QWidget()
layout = QHBoxLayout()
splitter.setLayout(layout)
layout.addWidget(treeView)
layout.addWidget(graphWindow)


window.setCentralWidget(splitter)
window.show()

# graphWindow.show()
sys.exit(app.exec_())

