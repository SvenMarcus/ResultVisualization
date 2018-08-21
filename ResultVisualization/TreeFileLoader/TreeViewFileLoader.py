import csv

from ResultVisualization.Reader.IbmbExperimentReader import IbmbExperimentReader
from ResultVisualization.TreeItem import CategoryItem, ResultTreeItem
from ResultVisualization.TreeView import TreeIndex
from ResultVisualization.TreeViewController import TreeViewController


class SemiColonDialect(csv.excel):
    delimiter = ";"

    def __init__(self):
        super().__init__()


class TreeViewFileLoader:

    def __init__(self, treeView: TreeViewController):
        self.__treeView = treeView
        self.__fileReader: IbmbExperimentReader = IbmbExperimentReader()

    def readFile(self, filepath: str) -> None:
        resultDict: dict = self.__fileReader.read(filepath)
        self.__insertIntoTree(resultDict)

    def readFiles(self, paths: list) -> None:
        resultDict: dict = self.__fileReader.readMany(paths)
        self.__insertIntoTree(resultDict)

    def __insertIntoTree(self, dict_, index=None):
        for key in dict_:
            tree_index = TreeIndex(index)
            if type(dict_[key]) is list:
                self.__treeView.insertItem(CategoryItem(key), tree_index)
                tree_index = TreeIndex(tree_index)
                for result in dict_[key]:
                    item = ResultTreeItem(result["Messfühler"])
                    item.results["PEAK"] = float(result["PEAK"])
                    item.results["PEACOCK"] = float(result["PEACOCK"])
                    item.results["Median_EXP"] = float(result["Median_EXP"])
                    item.results["Median_SIM"] = float(result["Median_SIM"])
                    self.__treeView.insertItem(item, tree_index)
            elif type(dict_[key]) is dict:
                self.__treeView.insertItem(CategoryItem(key), tree_index)
                self.__insertIntoTree(dict_[key], tree_index)
