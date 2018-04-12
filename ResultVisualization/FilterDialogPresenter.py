from typing import List, Dict

from QtResultVisualization.FilterView import FilterView
from ResultVisualization.DialogResult import DialogResult
from ResultVisualization.Filter import Filter
from ResultVisualization.TreeItem import TreeItem


class FilterDialogPresenter:

    def __init__(self, view: FilterView):
        self.__view = view
        self.__projectFilter: str = ""
        self.__experimentFilter: str = ""
        self.__resultFilter: str = ""
        self.__dialogResult = DialogResult.Cancel

    def showDialog(self) -> DialogResult:
        self.__view.show()
        return self.__dialogResult

    def setProjectFilter(self, name: str) -> None:
        self.__projectFilter = name

    def setExperimentFilter(self, name: str) -> None:
        self.__experimentFilter = name

    def setResultFilter(self, name: str) -> None:
        self.__resultFilter = name

    def handleAccept(self):
        if self.__validateFilter():
            self.__dialogResult = DialogResult.Ok
            self.__view.close()

    def handleCancel(self):
        self.__dialogResult = DialogResult.Cancel
        self.__view.close()

    def getFilter(self) -> Filter[TreeItem]:
        filterList: List[Dict[str, str]] = [
            {"tag": "Project", "text": self.__projectFilter},
            {"tag": "Experiment", "text": self.__experimentFilter},
            {"tag": "Result", "text": self.__resultFilter}
        ]

        return TreeNodeFilter(filterList)

    def __validateFilter(self) -> bool:
        return bool(self.__projectFilter or self.__experimentFilter or self.__resultFilter)


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

