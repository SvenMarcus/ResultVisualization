from typing import List, Dict

from ResultVisualization.Filter import Filter
from ResultVisualization.TreeItem import TreeItem


class FilterDialogPresenter:

    def __init__(self):
        self.__projectFilter: str = ""
        self.__experimentFilter: str = ""
        self.__resultFilter: str = ""

    def setProjectFilter(self, name: str) -> None:
        self.__projectFilter = name

    def setExperimentFilter(self, name: str) -> None:
        self.__experimentFilter = name

    def setResultFilter(self, name: str) -> None:
        self.__resultFilter = name

    def getFilter(self) -> Filter[TreeItem]:
        filterList: List[Dict[str, str]] = [
            {"tag": "Project", "text": self.__projectFilter},
            {"tag": "Experiment", "text": self.__experimentFilter},
            {"tag": "Result", "text": self.__resultFilter}
        ]

        return TreeNodeFilter(filterList)


class TreeNodeFilter(Filter[TreeItem]):

    def __init__(self, filters: List[Dict[str, str]]):
        self.__filters = filters

    def appliesTo(self, arg: TreeItem) -> bool:
        for filter in self.__filters:
            tag: str = filter["tag"]
            text: str = filter["text"]
            if (arg.tag == tag) and (text in arg.text):
                return True
        return False
