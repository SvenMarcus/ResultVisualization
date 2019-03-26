import os.path as path
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from QtResultVisualization.Dialogs import QtChooseFileDialog, QtSaveFileDialog
from QtResultVisualization.MplCommands import ExportPdfCommand
from QtResultVisualization.QtGraphViewFactory import QtGraphViewFactory
from QtResultVisualization.QtMainWindow import QtMainWindow
from QtResultVisualization.QtMenuBar import QtMenuBar, QtMenu
from QtResultVisualization.QtToolbar import QtToolbar
from ResultVisualization.Action import Action
from ResultVisualization.Commands import LoadGraphCommand, LoadTemplatesCommand, SaveTemplatesCommand, \
    AddGraphViewCommand, CloseGraphViewCommand
from ResultVisualization.MenuBar import MenuBar, Menu
from ResultVisualization.Toolbar import Toolbar

if __name__ == "__main__":
    moduleFolder: str = sys.path[0]

    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setApplicationName("Simple Graphs")

    factory = QtGraphViewFactory()

    loadTemplatesCommand = LoadTemplatesCommand(path.join(moduleFolder, "resources", "templates"), factory)
    loadTemplatesCommand.execute()

    saveTemplatesCommand = SaveTemplatesCommand(path.join(moduleFolder, "resources", "templates"), factory)

    toolbar: Toolbar = QtToolbar()
    menubar: MenuBar = QtMenuBar()

    mainWindow: QtMainWindow = QtMainWindow(factory, toolbar, menubar)
    mainWindow.onCloseEvent().append(lambda sender, args: saveTemplatesCommand.execute())

    addLinePlotCommand = AddGraphViewCommand(mainWindow, factory, "linear")
    addLinePlotAction = Action(path.join(moduleFolder, "resources", "LinePlot2.svg"), "New Line Plot",
                               addLinePlotCommand)

    addBoxPlotCommand = AddGraphViewCommand(mainWindow, factory, "box")
    addBoxPlotAction = Action(path.join(moduleFolder, "resources", "BoxPlot2.svg"), "New Box Plot", addBoxPlotCommand)

    closeViewCommand = CloseGraphViewCommand(mainWindow)
    closeViewAction = Action(path.join(moduleFolder, "resources", "Close.svg"), "Close View", closeViewCommand)

    loadCommand = LoadGraphCommand(mainWindow, factory, QtChooseFileDialog("*.graph", parent=mainWindow.getWidget()))
    loadGraphAction = Action(path.join(moduleFolder, "resources", "Load.svg"), "Load Graph", loadCommand)

    exportCommand = ExportPdfCommand(mainWindow, QtSaveFileDialog("*.pdf", parent=mainWindow.getWidget()))
    exportAction = Action(path.join(moduleFolder, "resources", "file-pdf.svg"), "Export Pdf", exportCommand)

    toolbar.addAction(addLinePlotAction)
    toolbar.addAction(addBoxPlotAction)
    toolbar.addAction(closeViewAction)
    toolbar.addAction(exportAction)
    toolbar.addAction(loadGraphAction)

    fileMenu: Menu = QtMenu("File")
    fileMenu.addAction(addLinePlotAction)

    menubar.addMenu(fileMenu)

    addLinePlotAction.trigger()
    mainWindow.show()

    sys.exit(app.exec_())
