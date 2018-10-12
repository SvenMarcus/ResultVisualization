from PyQt5.QtWidgets import QWidget

from QtResultVisualization.QtCreateFilterDialog import QtCreateFilterDialog, QtCreateFilterDialogSubViewFactory
from QtResultVisualization.QtEditSeriesFilterDialog import QtEditSeriesFilterDialog

from ResultVisualization.Commands import FilterCommandFactory
from ResultVisualization.CreateFilterDialog import CreateFilterDialog
from ResultVisualization.EditSeriesFilterDialog import EditSeriesFilterDialog
from ResultVisualization.FilterDialogFactory import FilterDialogFactory
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.Plot import Series
from ResultVisualization.SeriesRepository import SeriesRepository


class QtFilterDialogFactory(FilterDialogFactory):

    def __init__(self, filterRepo: FilterRepository, seriesRepo: SeriesRepository):
        self.__filterRepo: FilterRepository = filterRepo
        self.__seriesRepo: SeriesRepository = seriesRepo
        self.__commandFactory = FilterCommandFactory(self.__filterRepo)
        self.__parent: QWidget = None

    def setParent(self, parent: QWidget) -> None:
        self.__parent = parent

    def makeCreateFilterDialog(self) -> CreateFilterDialog:
        subViewFactory = QtCreateFilterDialogSubViewFactory(self.__seriesRepo)
        return QtCreateFilterDialog(self.__filterRepo, subViewFactory, self.__commandFactory, self.__parent)

    def makeEditSeriesFilterDialog(self, series: Series) -> EditSeriesFilterDialog:
        return QtEditSeriesFilterDialog(series, self.__filterRepo, self.__commandFactory, self.__parent)
