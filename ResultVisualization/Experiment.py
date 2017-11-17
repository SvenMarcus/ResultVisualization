from typing import Dict


class Experiment:

    __organization: str = ""
    __experimentName: str = ""
    __run: int = 0

    __results: Dict[str, Dict[str, float]] = {}

    def __init__(self):
        pass

    @property
    def experimentRun(self) -> int:
        return self.__run

    @experimentRun.setter
    def experimentRun(self, value: int) -> None:
        self.__run = value

    @property
    def experimentName(self) -> str:
        return self.__experimentName

    @experimentName.setter
    def experimentName(self, value: str) -> None:
        self.__experimentName = value

    @property
    def organization(self) -> str:
        return self.__organization

    @organization.setter
    def organization(self, value: str) -> None:
        self.__organization = value
