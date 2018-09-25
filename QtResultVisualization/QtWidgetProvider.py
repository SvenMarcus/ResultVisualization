from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QWidget


class QtWidgetProvider(ABC):

    @abstractmethod
    def getWidget(self) -> QWidget:
        raise NotImplementedError()
