import csv
from typing import Set, Dict


class SemiColonDialect(csv.excel):
    delimiter = ";"

    def __init__(self):
        super().__init__()


class IbmbExperimentReader:

    def __init__(self):
        self.__ignore: str = '#'
        self.__categories = ['Org.', 'Serie', 'Version', 'Test', 'Nr.']
        self.__values: Set[str] = {"Messfühler", "PEAK", "PEACOCK", "Median_EXP", "Median_SIM"}

    def read(self, filepath: str) -> Dict:
        import csv

        with open(filepath, newline='', encoding='ISO-8859-1') as csvfile:
            dictReader = csv.DictReader(csvfile, dialect=SemiColonDialect())

            finalDict: dict = {}

            for orderedDict in dictReader:
                currentItem = finalDict
                for i in range(0, len(self.__categories)):
                    key = self.__categories[i]
                    if key in orderedDict:

                        if not orderedDict[key] in currentItem:
                            if i < len(self.__categories) - 1:
                                currentItem[orderedDict[key]] = {}
                            else:
                                currentItem[orderedDict[key]] = []

                        currentItem = currentItem[orderedDict[key]]

                resultDict = {}
                for key in self.__values:
                    resultDict[key] = orderedDict[key]
                currentItem.append(resultDict)

        return finalDict

    def readMany(self, filepaths: list) -> Dict:
        finalDict: dict = {}
        for path in filepaths:
            tmpDict: dict = self.read(path)
            self.__merge(finalDict, tmpDict)
        return finalDict

    def __merge(self, finalDict, partialDict: Dict) -> None:
        for key in partialDict:
            if not key in finalDict:
                finalDict[key] = partialDict[key]
                continue

            if type(partialDict[key]) is dict:
                self.__merge(finalDict[key], partialDict[key])