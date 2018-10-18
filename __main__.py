import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from QtResultVisualization.Dialogs import QtChooseFileDialog
from QtResultVisualization.QtGraphViewFactory import QtGraphViewFactory
from QtResultVisualization.QtMainWindow import QtMainWindow
from QtResultVisualization.QtToolbar import QtToolbar

from ResultVisualization.Commands import LoadGraphCommand, LoadTemplatesCommand, SaveTemplatesCommand
from ResultVisualization.Action import Action
from ResultVisualization.Toolbar import Toolbar


if __name__ == "__main__":
    moduleFolder: str = sys.path[0]

    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setApplicationName("Simple Graphs")

    factory = QtGraphViewFactory()

    loadTemplatesCommand = LoadTemplatesCommand(sys.path[0] + "/resources/templates", factory)
    saveTemplatesCommand = SaveTemplatesCommand(sys.path[0] + "/resources/templates", factory)

    toolbar: Toolbar = QtToolbar()

    mainWindow: QtMainWindow = QtMainWindow(toolbar, factory, loadTemplatesCommand)
    mainWindow.loadTemplatesCommand = loadTemplatesCommand
    mainWindow.saveTemplatesCommand = saveTemplatesCommand

    loadCommand = LoadGraphCommand(mainWindow, factory, QtChooseFileDialog("*.graph", parent=mainWindow.getWidget()))
    loadGraphAction = Action("File", moduleFolder + "/resources/Load.svg", "Load Graph", loadCommand)
    toolbar.addAction(loadGraphAction)

    mainWindow.show()

    sys.exit(app.exec_())

