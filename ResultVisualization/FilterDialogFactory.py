from abc import ABC, abstractmethod

from ResultVisualization.CreateFilterDialog import CreateFilterDialog
from ResultVisualization.EditSeriesFilterDialog import EditSeriesFilterDialog
from ResultVisualization.Plot import Series


class FilterDialogFactory(ABC):

    @abstractmethod
    def makeCreateFilterDialog(self) -> CreateFilterDialog:
        raise NotImplementedError()

    @abstractmethod
    def makeEditSeriesFilterDialog(self, series: Series) -> EditSeriesFilterDialog:
        raise NotImplementedError()
