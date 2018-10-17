import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from QtResultVisualization.Dialogs import QtChooseFileDialog
from QtResultVisualization.QtGraphViewFactory import QtGraphViewFactory
from QtResultVisualization.QtMainWindow import QtMainWindow

from ResultVisualization.Commands import LoadGraphCommand, LoadTemplatesCommand, SaveTemplatesCommand
from ResultVisualization.TemplateRepository import TemplateRepository


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setApplicationName("Simple Graphs")

    factory = QtGraphViewFactory()

    loadTemplatesCommand = LoadTemplatesCommand(sys.path[0] + "/resources/templates", factory)
    saveTemplatesCommand = SaveTemplatesCommand(sys.path[0] + "/resources/templates", factory)

    mainWindow: QtMainWindow = QtMainWindow(factory, loadTemplatesCommand)
    mainWindow.loadTemplatesCommand = loadTemplatesCommand
    mainWindow.saveTemplatesCommand = saveTemplatesCommand
    loadCommand = LoadGraphCommand(mainWindow, factory, QtChooseFileDialog("*.graph", parent=mainWindow.getWidget()))
    mainWindow.loadFileCommand = loadCommand
    mainWindow.show()

    sys.exit(app.exec_())

