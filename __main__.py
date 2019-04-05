import os.path as path
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from QtResultVisualization.Dialogs import QtChooseFileDialog, QtSaveFileDialog
from QtResultVisualization.MplCommands import ExportPdfCommand
from QtResultVisualization.QtGraphViewFactory import QtGraphViewFactory
from QtResultVisualization.QtMainWindow import QtMainWindow
from QtResultVisualization.QtMenuBar import QtMenuBar, QtMenu
from QtResultVisualization.QtPlotSettingsDialog import QtPlotSettingsDialog
from QtResultVisualization.QtTextInputDialog import QtTextInputDialog
from QtResultVisualization.QtToolbar import QtToolbar
from ResultVisualization.Action import Action
from ResultVisualization.Commands import LoadGraphCommand, LoadTemplatesCommand, SaveTemplatesCommand, \
    AddGraphViewCommand, CloseGraphViewCommand, EditGraphViewTitleCommand, ShowPlotSettingsDialogCommand
from ResultVisualization.GraphView import GraphView
from ResultVisualization.MenuBar import MenuBar, Menu
from ResultVisualization.Toolbar import Toolbar

if __name__ == "__main__":
    moduleFolder: str = sys.path[0]
    resourcesFolder = path.join(moduleFolder, "resources")

    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setApplicationName("Simple Graphs")

    factory = QtGraphViewFactory()

    loadTemplatesCommand = LoadTemplatesCommand(path.join(resourcesFolder, "templates"), factory)
    loadTemplatesCommand.execute()

    saveTemplatesCommand = SaveTemplatesCommand(path.join(resourcesFolder, "templates"), factory)

    toolbar: Toolbar = QtToolbar()
    menubar: MenuBar = QtMenuBar()

    mainWindow: QtMainWindow = QtMainWindow(factory, toolbar, menubar)
    mainWindow.onCloseEvent().append(lambda sender, args: saveTemplatesCommand.execute())

    addLinePlotCommand = AddGraphViewCommand(mainWindow, factory, "linear", QtTextInputDialog())
    addLinePlotAction = Action("New", path.join(resourcesFolder, "LinePlot2.svg"), "Line Plot",
                               addLinePlotCommand, shortcut="Ctrl+L")

    addBoxPlotCommand = AddGraphViewCommand(mainWindow, factory, "box", QtTextInputDialog())
    addBoxPlotAction = Action("New", path.join(resourcesFolder, "BoxPlot2.svg"), "Box Plot",
                              addBoxPlotCommand, shortcut="Ctrl+B")

    editGraphViewTitleCommand = EditGraphViewTitleCommand(mainWindow, QtTextInputDialog())
    editGraphViewTitleAction = Action("Edit", "", "Edit Graph Title", editGraphViewTitleCommand, shortcut="Ctrl+R")

    closeViewCommand = CloseGraphViewCommand(mainWindow)
    closeViewAction = Action("View", path.join(resourcesFolder, "Close.svg"), "Close View", closeViewCommand, shortcut="Ctrl+W")

    loadCommand = LoadGraphCommand(mainWindow, factory, QtChooseFileDialog("*.graph", parent=mainWindow.getWidget()))
    loadGraphAction = Action("File", path.join(resourcesFolder, "Load.svg"), "Load Graph", loadCommand, shortcut="Ctrl+O")

    exportCommand = ExportPdfCommand(mainWindow, QtSaveFileDialog("*.pdf", parent=mainWindow.getWidget()))
    exportAction = Action("File", path.join(resourcesFolder, "file-pdf.svg"), "Export Pdf", exportCommand, shortcut="Ctrl+P")

    plotSettingsCommand = ShowPlotSettingsDialogCommand(mainWindow, QtPlotSettingsDialog(mainWindow.getWidget()))
    plotSettingsAction = Action("Edit", "", "Plot Settings", plotSettingsCommand)

    toolbar.addAction(addLinePlotAction)
    toolbar.addAction(addBoxPlotAction)
    toolbar.addAction(closeViewAction)
    toolbar.addAction(exportAction)
    toolbar.addAction(loadGraphAction)

    fileMenu: Menu = QtMenu("File")
    fileMenu.addChild(QtMenu("New"))

    menubar.addMenu(fileMenu)
    menubar.addAction(addLinePlotAction)
    menubar.addAction(addBoxPlotAction)
    menubar.addAction(editGraphViewTitleAction)
    menubar.addAction(plotSettingsAction)
    menubar.addAction(exportAction)
    menubar.addAction(loadGraphAction)
    menubar.addAction(closeViewAction)

    graphView: GraphView = factory.makeGraphView("linear")
    mainWindow.addGraphView(graphView, graphView.getTitle())
    mainWindow.show()

    sys.exit(app.exec_())
