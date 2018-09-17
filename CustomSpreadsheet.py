


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDockWidget, QMainWindow, QWidget

from QtResultVisualization.Dialogs import QtLineSeriesDialog
from QtResultVisualization.QtGraph import QtGraph
from QtResultVisualization.QtSpreadsheet import QtSpreadsheet
from ResultVisualization.Dialogs import DialogResult
from ResultVisualization.Graph import Graph, PlotConfig
from ResultVisualization.Spreadsheet import Spreadsheet


class CustomMainWindow(QMainWindow):

    def __init__(self):
        super(CustomMainWindow, self).__init__()
        graph: Graph = QtGraph(self)
        self.setCentralWidget(graph.getWidget())
        self.addDockWidget(Qt.LeftDockWidgetArea, QDockWidget(self))
        lineDialog: QtLineSeriesDialog = QtLineSeriesDialog(self)
        result: DialogResult = lineDialog.show()
        if result == DialogResult.Ok:
            config: PlotConfig = lineDialog.getPlotConfig()
            graph.addPlot(config)

app: QApplication = QApplication([])

mainWindow: QMainWindow = CustomMainWindow()
# view: QtSpreadsheet = QtSpreadsheet(mainWindow)

# spreadsheet: Spreadsheet = Spreadsheet(view)
# view.setSpreadsheet(spreadsheet)

# data = [
#     [1, 2, 3, 4],
#     ["a", "b", "c", "d"]
# ]

# spreadsheet.onCellSelectionChanged.append(lambda sender, args: print(spreadsheet.selectedCells()))


mainWindow.show()
# spreadsheet.setData(data)


app.exec_()
