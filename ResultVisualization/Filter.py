from abc import abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class Filter(Generic[T]):

    @abstractmethod
    def appliesTo(self, arg: T) -> bool:
        pass
