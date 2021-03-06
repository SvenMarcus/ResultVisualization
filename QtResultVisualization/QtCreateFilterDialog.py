from typing import List

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QDialog, QGridLayout,
                             QHBoxLayout, QHeaderView, QLabel, QLineEdit,
                             QMessageBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)

from QtResultVisualization.QtTransferWidget import QtTransferWidget
from ResultVisualization.Commands import FilterCommandFactory
from ResultVisualization.CreateFilterDialog import (CompositeFilterCreationView,
                                                    CreateFilterDialog,
                                                    CreateFilterDialogSubViewFactory,
                                                    FilterCreationView,
                                                    MetaDataMatchFilterCreationView,
                                                    RowContainsFilterCreationView)
from ResultVisualization.Dialogs import DialogResult
from ResultVisualization.Filter import SeriesFilter
from ResultVisualization.FilterRepository import FilterRepository
from ResultVisualization.Plot import Series
from ResultVisualization.SeriesRepository import SeriesRepository
from ResultVisualization.TransferWidget import TransferWidget


class QtRowContainsFilterWidget(RowContainsFilterCreationView):

    def __init__(self, parent: QWidget = None):
        super(QtRowContainsFilterWidget, self).__init__()
        self.__widget: QWidget = QWidget(parent)
        layout = QVBoxLayout()
        self.__widget.setLayout(layout)

        self.__titleBox: QLineEdit = QLineEdit()
        self.__requiredDataBox: QLineEdit = QLineEdit()
        self.__inverseCheckBox: QCheckBox = QCheckBox("Inverse")
        self.__okButton: QPushButton = QPushButton("OK")
        self.__okButton.clicked.connect(self._save)

        self.__buttonBar: QHBoxLayout = QHBoxLayout()
        self.__buttonBar.addWidget(self.__okButton, 1)
        self.__buttonBar.addStretch(3)

        self.__widget.layout().addStretch(2)
        self.__widget.layout().addWidget(QLabel("Filter Title:"))
        self.__widget.layout().addWidget(self.__titleBox, 1)
        self.__widget.layout().addWidget(QLabel("Required meta data:"))
        self.__widget.layout().addWidget(self.__requiredDataBox, 1)
        self.__widget.layout().addWidget(self.__inverseCheckBox)
        self.__widget.layout().addLayout(self.__buttonBar)
        self.__widget.layout().addStretch(2)

    def getWidget(self) -> QWidget:
        return self.__widget

    def _getTitleFromView(self) -> str:
        return self.__titleBox.text()

    def _getRequiredMetaDataFromView(self) -> str:
        return self.__requiredDataBox.text()

    def _getInverseFromView(self) -> bool:
        return self.__inverseCheckBox.isChecked()

    def _showMessage(self, message: str):
        QMessageBox.information(self.__widget, "Error", message)


class QtMetaDataMatchFilterCreationView(MetaDataMatchFilterCreationView):

    def __init__(self, seriesRepo: SeriesRepository, parent: QWidget = None):
        self.__parent: QWidget = parent
        super().__init__(seriesRepo)

    def getWidget(self) -> QWidget:
        return self.__widget

    def _initUI(self) -> None:
        self.__widget: QWidget = QWidget(self.__parent)

        self.__titleBox: QLineEdit = QLineEdit()
        self.__transferWidget: QtTransferWidget = QtTransferWidget()

        self.__okButton: QPushButton = QPushButton("Ok")
        self.__okButton.clicked.connect(self._save)

        self.__buttonBar: QHBoxLayout = QHBoxLayout()
        self.__buttonBar.addWidget(self.__okButton, 1)
        self.__buttonBar.addStretch(3)

        self.__widget.setLayout(QVBoxLayout())

        self.__widget.layout().addWidget(QLabel("Filter Title:"))
        self.__widget.layout().addWidget(self.__titleBox)
        self.__widget.layout().addWidget(self.__transferWidget.getWidget(), 3)
        self.__widget.layout().addLayout(self.__buttonBar)

    def _getTransferWidget(self) -> TransferWidget[Series]:
        return self.__transferWidget

    def _getTitleFromView(self) -> str:
        return self.__titleBox.text()

    def _showMessage(self, message: str):
        QMessageBox.information(self.__widget, "Error", message)


class QtCompositeFilterCreationView(CompositeFilterCreationView):

    def __init__(self, filters: List[SeriesFilter], parent: QWidget = None):
        self.__parent: QWidget = parent
        super().__init__(filters)

    def getWidget(self) -> QWidget:
        return self.__widget

    def _initUI(self) -> None:
        self.__widget: QWidget = QWidget(self.__parent)

        self.__titleBox: QLineEdit = QLineEdit()
        self.__transferWidget: QtTransferWidget = QtTransferWidget()

        self.__okButton: QPushButton = QPushButton("Ok")
        self.__okButton.clicked.connect(self._save)

        self.__buttonBar: QHBoxLayout = QHBoxLayout()
        self.__buttonBar.addWidget(self.__okButton, 1)
        self.__buttonBar.addStretch(3)

        self.__widget.setLayout(QVBoxLayout())

        self.__widget.layout().addWidget(QLabel("Filter Title:"))
        self.__widget.layout().addWidget(self.__titleBox)
        self.__widget.layout().addWidget(self.__transferWidget.getWidget(), 3)
        self.__widget.layout().addLayout(self.__buttonBar)

    def _getTransferWidget(self) -> TransferWidget[Series]:
        return self.__transferWidget

    def _getTitleFromView(self) -> str:
        return self.__titleBox.text()

    def _showMessage(self, message: str):
        QMessageBox.information(self.__widget, "Error", message)


class QtCreateFilterDialogSubViewFactory(CreateFilterDialogSubViewFactory):

    def __init__(self, seriesRepo: SeriesRepository, filterRepo: FilterRepository):
        super().__init__(seriesRepo, filterRepo)

    def makeView(self, kind: str) -> FilterCreationView:
        filterCreationView: FilterCreationView = None
        if kind == "RowContains":
            filterCreationView = QtRowContainsFilterWidget()
        elif kind == "ExactMetaMatch":
            filterCreationView = QtMetaDataMatchFilterCreationView(self._seriesRepo)
        elif kind == "CompositeFilter":
            filterCreationView = QtCompositeFilterCreationView(self._filterRepo.getFilters())
        else:
            return None

        filterCreationView.getWidget().setMinimumSize(600, 600)
        return filterCreationView


class QtCreateFilterDialog(CreateFilterDialog):

    def __init__(self, filterRepository: FilterRepository, subViewFactory: CreateFilterDialogSubViewFactory,
                 commandFactory: FilterCommandFactory, parent: QWidget = None):
        self.__parent: QWidget = parent
        self.__dialog: QDialog = None
        self.__availableFilters: QTableWidget = None
        self.__addFilterButton: QPushButton = None
        self.__removeFilterButton: QPushButton = None
        self.__filterTypeComboBox: QComboBox = None
        self.__subView: QWidget = None
        super(QtCreateFilterDialog, self).__init__(filterRepository, subViewFactory, commandFactory)

    def getWidget(self) -> QWidget:
        return self.__dialog

    def _initUI(self) -> None:
        self.__dialog: QDialog = QDialog(self.__parent)
        self.__dialog.setWindowTitle("Filter Creator")
        self.__dialog.setMinimumSize(1000, 800)
        self.__dialog.setLayout(QGridLayout())
        self.__dialog.finished.connect(lambda x: self._onWindowClosed())

        self.__availableFilters: QTableWidget = QTableWidget()
        self.__availableFilters.setEditTriggers(QTableWidget.NoEditTriggers)
        self.__availableFilters.setColumnCount(1)
        self.__availableFilters.setHorizontalHeaderLabels(["Available Filters"])
        self.__availableFilters.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.__addFilterButton: QPushButton = QPushButton("Select")
        self.__addFilterButton.clicked.connect(
            lambda: self._handleFilterOptionSelection(self.__filterTypeComboBox.currentText()))

        self.__removeFilterButton: QPushButton = QPushButton("Remove")
        self.__removeFilterButton.clicked.connect(self._handleFilterRemove)

        self.__filterTypeComboBox: QComboBox = QComboBox()

        self.__okButton: QPushButton = QPushButton("Ok")
        self.__okButton.setDefault(True)
        self.__okButton.clicked.connect(self._confirm)
        self.__cancelButton: QPushButton = QPushButton("Cancel")
        self.__cancelButton.clicked.connect(self._cancel)

        self.__buttonBar: QHBoxLayout = QHBoxLayout()
        self.__buttonBar.addWidget(self.__okButton)
        self.__buttonBar.addWidget(self.__cancelButton)

        self.__dialog.layout().addWidget(self.__availableFilters, 0, 0, 5, 3)
        self.__dialog.layout().addWidget(self.__addFilterButton, 0, 3)
        self.__dialog.layout().addWidget(self.__filterTypeComboBox, 0, 4)
        self.__dialog.layout().addWidget(self.__removeFilterButton, 6, 0, 1, 3)
        self.__dialog.layout().addLayout(self.__buttonBar, 7, 0)

    def _addFilterToAvailableFiltersTable(self, filterName: str) -> None:
        rows: int = self.__availableFilters.rowCount()
        self.__availableFilters.setRowCount(rows + 1)
        self.__availableFilters.setItem(rows, 0, QTableWidgetItem(filterName))

    def _addFilterOptionToView(self, optionName: str) -> None:
        self.__filterTypeComboBox.addItem(optionName)

    def _removeFilterFromAvailableFiltersTable(self, index: int) -> None:
        self.__availableFilters.removeRow(index)

    def _getSelectedFilterIndexFromView(self) -> int:
        indexes: List[QModelIndex] = self.__availableFilters.selectedIndexes()
        if indexes:
            return indexes[0].row()
        return -1

    def _showSubView(self, view: FilterCreationView) -> None:
        if self.__subView is not None:
            self.__subView.setParent(None)
            self.__subView.deleteLater()

        self.__subView = view.getWidget()
        self.__dialog.layout().addWidget(self.__subView, 1, 3, 4, 4)
        self.__dialog.repaint()

    def _closeSubView(self, view: FilterCreationView) -> None:
        widget = view.getWidget()
        widget.setParent(None)
        if widget is self.__subView:
            self.__subView = None

        widget.deleteLater()
        self.__dialog.repaint()

    def _close(self) -> None:
        self.__dialog.done(0)

    def show(self) -> DialogResult:
        self.__dialog.exec()

        return self._result
