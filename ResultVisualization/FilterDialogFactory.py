from abc import ABC, abstractmethod

from ResultVisualization.Dialogs import Dialog
from ResultVisualization.Plot import Series


class FilterDialogFactory(ABC):

    @abstractmethod
    def makeCreateFilterDialog(self) -> Dialog:
        raise NotImplementedError()

    @abstractmethod
    def makeEditSeriesFilterDialog(self, series: Series) -> Dialog:
        raise NotImplementedError()
