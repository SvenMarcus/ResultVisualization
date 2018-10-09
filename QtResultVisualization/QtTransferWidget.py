from typing import List

from PyQt5.QtWidgets import (QGridLayout, QHeaderView,
                             QPushButton, QTableWidget,
                             QTableWidgetItem, QWidget)


class QtTransferWidget(QWidget):

    def __init__(self, parent: QWidget = None):
        self.__parent = parent
        super().__init__()

    def getWidget(self) -> QWidget:
        return self.__widget

    def setLeftHeader(self, header: str) -> None:
        self.__leftTable.setHorizontalHeaderLabels(header)

    def setRightHeader(self, header: str) -> None:
        self.__rightTable.setHorizontalHeaderLabels(header)

    def _initUI(self) -> None:
        self.__widget: QWidget = QWidget(self.__parent)
        self.__leftTable: QTableWidget = QTableWidget()
        self.__leftTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.__leftTable.setColumnCount(1)
        self.__leftTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.__rightTable: QTableWidget = QTableWidget()
        self.__rightTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.__rightTable.setColumnCount(1)
        self.__rightTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.__transferLeftButton: QPushButton = QPushButton("<<")
        self.__transferRightButton: QPushButton = QPushButton(">>")

        self.__transferLeftButton.clicked.connect(lambda: self.__onTransferLeftClicked())
        self.__transferRightButton.clicked.connect(lambda: self.__onTransferRightClicked())

        self.__widget.setLayout(QGridLayout())

        self.__widget.layout().addWidget(self.__leftTable, 0, 0, 4, 1)
        self.__widget.layout().addWidget(self.__transferLeftButton, 1, 1)
        self.__widget.layout().addWidget(self.__transferRightButton, 2, 1)
        self.__widget.layout().addWidget(self.__rightTable, 0, 2, 4, 1)

    def _addToLeftTable(self, item: str) -> None:
        rows: int = self.__leftTable.rowCount()
        self.__leftTable.setRowCount(rows + 1)
        self.__leftTable.setItem(rows, 0, QTableWidgetItem(item))

    def _addToRightTable(self, item: str) -> None:
        rows: int = self.__rightTable.rowCount()
        self.__rightTable.setRowCount(rows + 1)
        self.__rightTable.setItem(rows, 0, QTableWidgetItem(item))

    def _removeFromLeftTable(self, index: int) -> None:
        self.__leftTable.removeRow(index)
        self.__leftTable.clearSelection()

    def _removeFromRightTable(self, index: int) -> None:
        self.__rightTable.removeRow(index)
        self.__rightTable.clearSelection()

    def __onTransferLeftClicked(self) -> None:
        rows: List[int] = self.__getSelectedRows(self.__leftTable)
        if len(rows) == 0:
            return

        self._moveItemsToLeftTable(rows)

    def __onTransferRightClicked(self) -> None:
        rows: List[int] = self.__getSelectedRows(self.__rightTable)
        if len(rows) == 0:
            return

        self._moveItemsToRightTable(rows)

    def __getSelectedRows(self, table: QTableWidget) -> List[int]:
        indexes = table.selectedIndexes()
        if len(indexes) == 0:
            return list()

        return [index.row() for index in indexes]
