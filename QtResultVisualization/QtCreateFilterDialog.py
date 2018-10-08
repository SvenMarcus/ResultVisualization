from typing import Dict

from PyQt5.QtWidgets import (QComboBox, QDialog, QGridLayout, QHBoxLayout,
                             QHeaderView, QLabel, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QWidget)

from ResultVisualization.CreateFilterDialog import (CreateFilterDialog,
                                                    CreateFilterDialogSubViewFactory,
                                                    FilterCreationView,
                                                    RowContainsFilterCreationView)
from ResultVisualization.Dialogs import DialogResult
from ResultVisualization.FilterRepository import FilterRepository


class QtRowContainsFilterWidget(RowContainsFilterCreationView):

    def __init__(self, parent: QWidget = None):
        super(QtRowContainsFilterWidget, self).__init__()
        self.__widget: QWidget = QWidget(parent)
        layout = QVBoxLayout()
        self.__widget.setLayout(layout)

        self.__titleBox: QLineEdit = QLineEdit()
        self.__requiredDataBox: QLineEdit = QLineEdit()
        self.__acceptButton: QPushButton = QPushButton("OK")
        self.__acceptButton.clicked.connect(lambda: self._save())

        self.__widget.layout().addWidget(QLabel("Filter Title:"))
        self.__widget.layout().addWidget(self.__titleBox)

        self.__widget.layout().addWidget(QLabel("Required meta data:"))
        self.__widget.layout().addWidget(self.__requiredDataBox)

        self.__widget.layout().addWidget(self.__acceptButton)

    def getWidget(self) -> QWidget:
        return self.__widget

    def _getTitleFromView(self) -> str:
        return self.__titleBox.text()

    def _getRequiredMetaDataFromView(self) -> str:
        return self.__requiredDataBox.text()


class Dummy:

    def __init__(self, parent: QWidget = None):
        self.__widget: QWidget = QWidget(parent)
        layout = QVBoxLayout()
        self.__widget.setLayout(layout)

        self.__widget.layout().addWidget(QLabel("DUMMY!"))

    def getWidget(self) -> QWidget:
        return self.__widget


class QtCreateFilterDialogSubViewFactory(CreateFilterDialogSubViewFactory):

    def getSubViewVariantDisplayNameToNameDict(self) -> Dict[str, str]:
        return {
            "Match meta data in row": "RowContains",
            "DummDeeDumm": "Dummy"
        }

    def makeView(self, kind: str) -> FilterCreationView:
        if kind == "RowContains":
            return QtRowContainsFilterWidget()
        elif kind == "Dummy":
            print("Creating Dummy")
            return Dummy()

class QtCreateFilterDialog(CreateFilterDialog):

    def __init__(self, filterRepository: FilterRepository, subViewFactory: CreateFilterDialogSubViewFactory, parent: QWidget):
        self.__parent: QWidget = parent
        self.__dialog: QDialog = None
        self.__availableFilters: QTableWidget = None
        self.__addFilterButton: QPushButton = None
        self.__filterTypeComboBox: QComboBox = None
        self.__subView: QWidget = None
        super(QtCreateFilterDialog, self).__init__(filterRepository, subViewFactory)

    def getWidget(self) -> QWidget:
        return self.__dialog

    def _initUI(self) -> None:
        self.__dialog: QDialog = QDialog(self.__parent)
        self.__dialog.setLayout(QGridLayout())

        self.__availableFilters: QTableWidget = QTableWidget()
        self.__availableFilters.setEditTriggers(QTableWidget.NoEditTriggers)
        self.__availableFilters.setColumnCount(1)
        self.__availableFilters.setHorizontalHeaderLabels(["Available Filters"])
        self.__availableFilters.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.__addFilterButton: QPushButton = QPushButton("Add:")
        self.__addFilterButton.clicked.connect(lambda: self._handleFilterOptionSelection(self.__filterTypeComboBox.currentText()))
        self.__filterTypeComboBox: QComboBox = QComboBox()

        self.__dialog.layout().addWidget(self.__availableFilters, 0, 0, 3, 3)
        self.__dialog.layout().addWidget(self.__addFilterButton, 3, 0)
        self.__dialog.layout().addWidget(self.__filterTypeComboBox, 3, 1, 1, 2)

    def _addFilterToAvailableFiltersTable(self, filterName: str) -> None:
        rows: int = self.__availableFilters.rowCount()
        self.__availableFilters.setRowCount(rows + 1)
        self.__availableFilters.setItem(rows, 0, QTableWidgetItem(filterName))

    def _addFilterOptionToView(self, optionName: str) -> None:
        self.__filterTypeComboBox.addItem(optionName)

    def _showSubView(self, view: FilterCreationView) -> None:
        if self.__subView is not None:
            self.__subView.setParent(None)
            del self.__subView

        self.__subView = view.getWidget()
        self.__dialog.layout().addWidget(self.__subView, 1, 4)

    def _close(self) -> None:
        self.__dialog.done(0)

    def show(self) -> DialogResult:
        self.__dialog.exec()

        return self._result
