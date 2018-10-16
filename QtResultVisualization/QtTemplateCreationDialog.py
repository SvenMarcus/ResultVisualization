from typing import List

from PyQt5.QtWidgets import (QDialog, QGridLayout, QLabel, QLineEdit, QMessageBox,
                             QPushButton, QWidget, QTableWidget, QTableWidgetItem)

from ResultVisualization.Dialogs import DialogResult
from ResultVisualization.TemplateCreationDialog import TemplateCreationDialog
from ResultVisualization.TemplateRepository import TemplateRepository


class QtTemplateCreationDialog(TemplateCreationDialog):

    def __init__(self, templateRepository: TemplateRepository, parent: QWidget = None):
        self.__dialog: QDialog = QDialog(parent)
        self.__dialog.setLayout(QGridLayout())

        self.__title: QLineEdit = QLineEdit()
        self.__xColumn: QLineEdit = QLineEdit()
        self.__yColumn: QLineEdit = QLineEdit()
        self.__meta: QLineEdit = QLineEdit()
        self.__xLabel: QLineEdit = QLineEdit()
        self.__yLabel: QLineEdit = QLineEdit()
        self.__style: QLineEdit = QLineEdit()

        addStyleButton: QPushButton = QPushButton("Add Style")
        addStyleButton.clicked.connect(self._addStyle)

        removeStyleButton: QPushButton = QPushButton("Remove Style")
        removeStyleButton.clicked.connect(self._removeStyle)

        confirmButton: QPushButton = QPushButton("Ok")
        confirmButton.clicked.connect(self._confirm)

        cancelButton: QPushButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self._close)

        self.__styleList: QTableWidget = QTableWidget()
        self.__styleList.setColumnCount(1)
        self.__styleList.setHorizontalHeaderLabels(["Styles"])
        self.__styleList.setEditTriggers(QTableWidget.NoEditTriggers)

        self.__dialog.layout().addWidget(self.__styleList, 0, 2, -1, 1)

        self.__dialog.layout().addWidget(QLabel("Title:"), 0, 0)
        self.__dialog.layout().addWidget(self.__title, 0, 1)
        self.__dialog.layout().addWidget(QLabel("Quick Style:"), 1, 0)
        self.__dialog.layout().addWidget(self.__style, 1, 1)
        self.__dialog.layout().addWidget(addStyleButton, 2, 0)
        self.__dialog.layout().addWidget(removeStyleButton, 2, 1)

        self.__dialog.layout().addWidget(QLabel("X Column:"), 3, 0)
        self.__dialog.layout().addWidget(self.__xColumn, 3, 1)

        self.__dialog.layout().addWidget(QLabel("Y Column:"), 4, 0)
        self.__dialog.layout().addWidget(self.__yColumn, 4, 1)

        self.__dialog.layout().addWidget(QLabel("Meta Column:"), 5, 0)
        self.__dialog.layout().addWidget(self.__meta, 5, 1)

        self.__dialog.layout().addWidget(QLabel("X Label:"), 6, 0)
        self.__dialog.layout().addWidget(self.__xLabel, 6, 1)

        self.__dialog.layout().addWidget(QLabel("Y Label:"), 7, 0)
        self.__dialog.layout().addWidget(self.__yLabel, 7, 1)

        self.__dialog.layout().addWidget(confirmButton, 8, 0)
        self.__dialog.layout().addWidget(cancelButton, 8, 1)

        self.__dialog.layout().setRowStretch(9, 5)

        super().__init__(templateRepository)

    def _addStyleToListView(self, style: str) -> None:
        rows: int = self.__styleList.rowCount()
        self.__styleList.setRowCount(rows + 1)
        self.__styleList.setItem(rows, 0, QTableWidgetItem(style))

    def _removeStyleFromListView(self, index: int) -> None:
        self.__styleList.removeRow(index)

    def _getSelectedStyleIndexes(self) -> List[int]:
        return [idx.row() for idx in self.__styleList.selectedIndexes()]

    def _getTitleFromView(self) -> str:
        return self.__title.text()

    def _getStyleStringFromView(self) -> str:
        return self.__style.text()

    def _getXColumnFromView(self) -> str:
        return self.__xColumn.text()

    def _getYColumnFromView(self) -> str:
        return self.__yColumn.text()

    def _getMetaColumnFromView(self) -> str:
        return self.__meta.text()

    def _getXLabelFromView(self) -> str:
        return self.__xLabel.text()

    def _getYLabelFromView(self) -> str:
        return self.__yLabel.text()

    def _clearStyleStringInView(self) -> str:
        self.__style.clear()

    def _showMessage(self, msg: str) -> None:
        QMessageBox.information(self.__dialog, "Error", msg)

    def show(self) -> DialogResult:
        self.__dialog.setModal(True)
        self.__dialog.exec()

        return self._result

    def _close(self) -> None:
        self.__dialog.done(0)
