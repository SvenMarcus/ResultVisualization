from typing import List

from PyQt5.QtWidgets import (QComboBox, QDialog, QGridLayout, QLabel,
                             QLineEdit, QMessageBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QWidget)

from QtResultVisualization.Dialogs import QtChooseMultipleFilesDialog
from ResultVisualization.Dialogs import ChooseMultipleFilesDialog, DialogResult
from ResultVisualization.GraphView import GraphView
from ResultVisualization.LoadFromTemplateDialog import LoadFromTemplateDialog
from ResultVisualization.SeriesRepository import SeriesRepository
from ResultVisualization.TemplateRepository import TemplateRepository


class QtLoadFromTemplateDialog(LoadFromTemplateDialog):

    def __init__(self, templateRepository: TemplateRepository, graphView: GraphView, seriesRepo: SeriesRepository, parent: QWidget = None):
        self.__dialog: QDialog = QDialog(parent)
        self.__dialog.setLayout(QGridLayout())

        addFilesButton: QPushButton = QPushButton("Add files")
        addFilesButton.clicked.connect(self._selectFiles)

        removeFilesButton: QPushButton = QPushButton("Remove selected files")
        removeFilesButton.clicked.connect(self._removeFiles)

        confirmButton: QPushButton = QPushButton("Ok")
        confirmButton.clicked.connect(self._confirm)

        cancelButton: QPushButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self._close)

        self.__templates: QComboBox = QComboBox()

        self.__fileList: QTableWidget = QTableWidget()
        self.__fileList.setColumnCount(1)
        self.__fileList.setHorizontalHeaderLabels(["Files"])
        self.__fileList.setEditTriggers(QTableWidget.NoEditTriggers)

        self.__dialog.layout().addWidget(self.__fileList, 0, 2, -1, 1)

        self.__dialog.layout().addWidget(QLabel("Templates:"), 0, 0)
        self.__dialog.layout().addWidget(self.__templates, 0, 1)

        self.__dialog.layout().addWidget(addFilesButton, 1, 0)
        self.__dialog.layout().addWidget(removeFilesButton, 1, 1)

        self.__dialog.layout().addWidget(confirmButton, 2, 0)
        self.__dialog.layout().addWidget(cancelButton, 2, 1)
        self.__dialog.layout().setRowStretch(3, 5)

        super().__init__(templateRepository, graphView, seriesRepo)

    def _addFileToListView(self, file: str) -> None:
        rows: int = self.__fileList.rowCount()
        self.__fileList.setRowCount(rows + 1)
        self.__fileList.setItem(rows, 0, QTableWidgetItem(file))

    def _removeFileFromListView(self, index: int) -> None:
        self.__fileList.removeRow(index)

    def _getSelectedFileIndexes(self) -> List[int]:
        return [idx.row() for idx in self.__styleList.selectedIndexes()]

    def _addTemplateToComboBox(self, template: str) -> None:
        self.__templates.addItem(template)

    def _removeTemplateFromComboBox(self, index: int) -> None:
        self.__templates.removeItem(index)

    def _getSelectedTemplateIndex(self) -> int:
        return self.__templates.currentIndex()

    def _makeChooseMultipleFilesDialog(self) -> ChooseMultipleFilesDialog:
        return QtChooseMultipleFilesDialog("*.csv", self.__dialog)

    def _showMessage(self, msg: str) -> None:
        QMessageBox.information(self.__dialog, "Error", msg)

    def show(self) -> DialogResult:
        self.__dialog.setModal(True)
        self.__dialog.exec()

        return self._result

    def _close(self) -> None:
        self.__dialog.done(0)
