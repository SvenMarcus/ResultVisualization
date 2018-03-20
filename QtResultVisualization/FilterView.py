from PyQt5.QtWidgets import QDialog, QLayout, QVBoxLayout, QLineEdit


class FilterView(QDialog):

    def __init__(self, presenter=None):
        super().__init__()
        self.__presenter = presenter
        self.__layout: QLayout = QVBoxLayout()
        self.setLayout(self.__layout)
        self.__projectFilterBox: QLineEdit = QLineEdit()
        self.__experimentFilterBox: QLineEdit = QLineEdit()
        self.__resultFilterBox: QLineEdit = QLineEdit()
        self.__layout.addWidget(self.__projectFilterBox)
        self.__layout.addWidget(self.__experimentFilterBox)
        self.__layout.addWidget(self.__resultFilterBox)

    def show(self):
        self.showNormal()

    def setPresenter(self, presenter) -> None:
        self.__presenter = presenter

    def __connectSignals(self):
        self.__projectFilterBox.textChanged.connect(
            lambda: self.__presenter.setProjectFilter(self.__projectFilterBox.text()))
        self.__experimentFilterBox.textChanged.connect(
            lambda: self.__presenter.setExperimentFilter(self.__experimentFilterBox.text()))
        self.__resultFilterBox.textChanged.connect(
            lambda: self.__presenter.setResultFilter(self.__resultFilterBox.text()))
