from abc import ABC, abstractmethod

from ResultVisualization.GraphView import GraphView
from ResultVisualization.TemplateCreationDialog import TemplateCreationDialog
from ResultVisualization.TemplateRepository import TemplateRepository


class TemplateDialogFactory(ABC):

    @abstractmethod
    def makeTemplateCreationDialog(self) -> TemplateCreationDialog:
        raise NotImplementedError()

    @abstractmethod
    def makeLoadFromTemplateDialog(self) -> TemplateCreationDialog:
        raise NotImplementedError()
