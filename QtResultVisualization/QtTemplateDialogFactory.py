from QtResultVisualization.QtLoadFromTemplateDialog import \
    QtLoadFromTemplateDialog
from QtResultVisualization.QtTemplateCreationDialog import \
    QtTemplateCreationDialog
from ResultVisualization.GraphView import GraphView
from ResultVisualization.LoadFromTemplateDialog import LoadFromTemplateDialog
from ResultVisualization.SeriesRepository import SeriesRepository
from ResultVisualization.TemplateCreationDialog import TemplateCreationDialog
from ResultVisualization.TemplateDialogFactory import TemplateDialogFactory
from ResultVisualization.TemplateRepository import TemplateRepository


class QtTemplateDialogFactory(TemplateDialogFactory):

    def __init__(self, templateRepo: TemplateRepository, graphView: GraphView, seriesRepo: SeriesRepository):
        self.__templateRepo: TemplateRepository = templateRepo
        self.__graphView: GraphView = graphView
        self.__seriesRepo: SeriesRepository = seriesRepo

    def makeTemplateCreationDialog(self) -> TemplateCreationDialog:
        return QtTemplateCreationDialog(self.__templateRepo)

    def makeLoadFromTemplateDialog(self) -> LoadFromTemplateDialog:
        return QtLoadFromTemplateDialog(self.__templateRepo, self.__graphView, self.__seriesRepo)
