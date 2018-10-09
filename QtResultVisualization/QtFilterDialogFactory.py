from PyQt5.QtWidgets import QWidget

from QtResultVisualization.QtCreateFilterDialog import QtCreateFilterDialog, QtCreateFilterDialogSubViewFactory
from QtResultVisualization.QtEditSeriesFilterDialog import QtEditSeriesFilterDialog

from ResultVisualization.CreateFilterDialog import CreateFilterDialog
from ResultVisualization.FilterDialogFactory import FilterDialogFactory
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.plot import Series


class QtFilterDialogFactory(FilterDialogFactory):

    def __init__(self, filterRepo: FilterRepository):
        self.__filterRepo: FilterRepository = filterRepo
        self.__parent: QWidget = None

    def setParent(self, parent: QWidget) -> None:
        self.__parent = parent

    def makeCreateFilterDialog(self) -> CreateFilterDialog:
        subViewFactory = QtCreateFilterDialogSubViewFactory()
        return QtCreateFilterDialog(self.__filterRepo, subViewFactory, self.__parent)

    def makeEditSeriesFilterDialog(self, series: Series):
        return QtEditSeriesFilterDialog(series, self.__filterRepo, self.__parent)
