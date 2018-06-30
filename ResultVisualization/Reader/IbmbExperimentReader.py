import csv
from typing import Set, Dict


class SemiColonDialect(csv.excel):
    delimiter = ";"

    def __init__(self):
        super().__init__()


class IbmbExperimentReader:

    def __init__(self):
        self.__ignore: str = '#'
        self.__categories = ['Org.', 'Serie', 'Version', 'Test', 'Nr.', "Messfühler"]
        self.__values: Set[str] = {"PEAK", "PEACOCK", "Median_EXP", "Median_SIM"}

    def read(self, filepath: str) -> Dict:
        import csv

        with open(filepath, newline='', encoding='ISO-8859-1') as csvfile:
            dictReader = csv.DictReader(csvfile, dialect=SemiColonDialect())

            finalDict: dict = {}
            currentDict: dict
            for orderedDict in dictReader:
                currentDict = finalDict
                for key in self.__categories:
                    if key in orderedDict:
                        if not orderedDict[key] in currentDict:
                            currentDict[orderedDict[key]] = {}

                        currentDict = currentDict[orderedDict[key]]

                for key in self.__values:
                    currentDict[key] = orderedDict[key]

        return finalDict


    def readMany(self, filepaths: list) -> Dict:
        finalDict: dict = {}
        for path in filepaths:
            tmpDict: dict = self.read(path)
            self.__merge(finalDict, tmpDict)
        return finalDict


    def __merge(self, finalDict, partialDict):
        for key in partialDict:
            if not key in finalDict:
                finalDict[key] = partialDict[key]
                continue

            if type(partialDict[key]) is dict:
                self.__merge(finalDict[key], partialDict[key])