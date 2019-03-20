from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.backends.backend_template import FigureCanvas

from ResultVisualization.Commands import Command
from ResultVisualization.Dialogs import ChooseFileDialog, DialogResult
from ResultVisualization.MainWindow import MainWindow


class ExportPdfCommand(Command):

    def __init__(self, mainWindow: MainWindow, fileChooser: ChooseFileDialog):
        self.__mainWindow: MainWindow = mainWindow
        self.__fileChooser = fileChooser

    def execute(self):
        result = self.__fileChooser.show()

        if result is not DialogResult.Ok:
            return

        pdf = PdfPages(self.__fileChooser.getSelectedFile())

        for graphView in self.__mainWindow.getCurrentViews():
            graph = graphView.getGraph()
            canvas: FigureCanvas = graph.getFigureCanvas()
            pdf.savefig(canvas.figure)

        pdf.close()
