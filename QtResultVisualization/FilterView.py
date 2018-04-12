from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QLayout, QLineEdit, QDialogButtonBox, QGridLayout, QLabel

from ResultVisualization.DialogResult import DialogResult


class FilterView(QDialog):

    def __init__(self, presenter=None):
        super().__init__()
        self.__presenter = presenter
        self.__initWidgets()

    def __initWidgets(self) -> None:
        self.setWindowTitle("Create Filter")
        self.setModal(True)
        self.__layout: QLayout = QGridLayout()
        self.setLayout(self.__layout)
        self.__projectFilterBox: QLineEdit = QLineEdit()
        self.__experimentFilterBox: QLineEdit = QLineEdit()
        self.__resultFilterBox: QLineEdit = QLineEdit()
        self.__layout.addWidget(QLabel("Project"), 0, 0)
        self.__layout.addWidget(self.__projectFilterBox, 0, 1)
        self.__layout.addWidget(QLabel("Experiment"), 1, 0)
        self.__layout.addWidget(self.__experimentFilterBox, 1, 1)
        self.__layout.addWidget(QLabel("Result"), 2, 0)
        self.__layout.addWidget(self.__resultFilterBox, 2, 1)
        self.__buttonBox: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                                              | QDialogButtonBox.Cancel)
        self.__layout.addWidget(self.__buttonBox, 3, 1)
        self.__connectSignals()

    def show(self) -> None:
        self.showNormal()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.__presenter.handleCancel()

    def setPresenter(self, presenter) -> None:
        self.__presenter = presenter

    def __connectSignals(self) -> None:
        self.__projectFilterBox.textChanged.connect(
            lambda: self.__presenter.setProjectFilter(self.__projectFilterBox.text()))
        self.__experimentFilterBox.textChanged.connect(
            lambda: self.__presenter.setExperimentFilter(self.__experimentFilterBox.text()))
        self.__resultFilterBox.textChanged.connect(
            lambda: self.__presenter.setResultFilter(self.__resultFilterBox.text()))

        self.__buttonBox.button(QDialogButtonBox.Ok).clicked.connect(
            lambda: self.__presenter.handleAccept())
        self.__buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(
            lambda: self.__presenter.handleCancel())

    def __closeWithResult(self, result: DialogResult) -> None:
        self.__presenter.setDialogResult(result)
        self.close()
