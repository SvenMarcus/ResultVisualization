import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from QtResultVisualization.Dialogs import QtChooseFileDialog
from QtResultVisualization.QtGraphViewFactory import QtGraphViewFactory
from QtResultVisualization.QtMainWindow import QtMainWindow
from QtResultVisualization.QtToolbar import QtToolbar

from ResultVisualization.Commands import LoadGraphCommand, LoadTemplatesCommand, SaveTemplatesCommand, AddGraphViewCommand, CloseGraphViewCommand
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
    loadTemplatesCommand.execute()

    saveTemplatesCommand = SaveTemplatesCommand(sys.path[0] + "/resources/templates", factory)

    toolbar: Toolbar = QtToolbar()

    mainWindow: QtMainWindow = QtMainWindow(toolbar, factory)
    mainWindow.onCloseEvent().append(lambda sender, args: saveTemplatesCommand.execute())

    addLinePlotCommand = AddGraphViewCommand(mainWindow, factory, "linear")
    addLinePlotAction = Action("Create", moduleFolder + "/resources/LinePlot2.svg", "New Line Plot", addLinePlotCommand)

    addBoxPlotCommand = AddGraphViewCommand(mainWindow, factory, "box")
    addBoxPlotAction = Action("Create", moduleFolder + "/resources/BoxPlot2.svg", "New Box Plot", addBoxPlotCommand)

    closeViewCommand = CloseGraphViewCommand(mainWindow)
    closeViewAction = Action("Close", moduleFolder + "/resources/Close.svg", "Close View", closeViewCommand)

    loadCommand = LoadGraphCommand(mainWindow, factory, QtChooseFileDialog("*.graph", parent=mainWindow.getWidget()))
    loadGraphAction = Action("File", moduleFolder + "/resources/Load.svg", "Load Graph", loadCommand)

    toolbar.addAction(addLinePlotAction)
    toolbar.addAction(addBoxPlotAction)
    toolbar.addAction(closeViewAction)
    toolbar.addAction(loadGraphAction)
    addLinePlotAction.trigger()
    mainWindow.show()

    sys.exit(app.exec_())
