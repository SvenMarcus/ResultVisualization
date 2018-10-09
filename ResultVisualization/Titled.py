from abc import ABC, abstractmethod

class Titled(ABC):

    @property
    @abstractmethod
    def title(self) -> str:
        raise NotImplementedError()

    @title.setter
    @abstractmethod
    def title(self, value: str) -> None:
        raise NotImplementedError()
