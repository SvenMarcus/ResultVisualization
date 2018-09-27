from abc import abstractmethod
from numbers import Number
from typing import Generic, TypeVar


T = TypeVar("T")


class Filter(Generic[T]):

    @abstractmethod
    def appliesTo(self, arg: T) -> bool:
        raise NotImplementedError()
