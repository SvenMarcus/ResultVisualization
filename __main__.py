import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction

from QtResultVisualization.QtTreeView import QtTreeView
from QtResultVisualization.Dialogs import QtDialogFactory

from ResultVisualization.TreeFileLoader.TreeViewFileLoader import TreeViewFileLoader
from ResultVisualization.TreeViewController import TreeViewController
from ResultVisualization.Actions import ChooseFolderAction

path1 = "./Experiments/PRS1_Door3_FDS607/Results/Results_Export.csv"
path2 = "./Experiments/PRS1_Door4_FDS607/Results/Results_Export.csv"


app = QApplication(sys.argv)
mainWindow: QMainWindow = QMainWindow()

treeView: QtTreeView = QtTreeView(mainWindow)
treeView.setMinimumHeight(300)
treeView.setMinimumWidth(300)

treeViewController: TreeViewController = TreeViewController(treeView)
loader: TreeViewFileLoader = TreeViewFileLoader(treeViewController)
loader.readFiles([path1, path2])

menuBar: QMenuBar = QMenuBar(mainWindow)
fileMenu: QMenu = QMenu("File", menuBar)
menuBar.addMenu(fileMenu)


dialogFactory: QtDialogFactory = QtDialogFactory()

chooseFolderAction: ChooseFolderAction = ChooseFolderAction(dialogFactory)

qtChooseFolderAction: QAction = QAction("Choose Folder")
qtChooseFolderAction.triggered.connect(chooseFolderAction.execute)

exitAction: QAction = QAction("Exit")
exitAction.triggered.connect(exit)

fileMenu.addAction(qtChooseFolderAction)
fileMenu.addAction(exitAction)

mainWindow.setMenuBar(menuBar)

mainWindow.show()

# item: TreeItem = CategoryItem("Test")
# index: TreeIndex = TreeIndex()
#
# subItem: TreeItem = TreeItem("SubTest")
# subIndex: TreeIndex = TreeIndex(index, 0)
#
# treeViewController.insertItem(item, index)
# treeViewController.insertItem(subItem, subIndex)
sys.exit(app.exec_())
