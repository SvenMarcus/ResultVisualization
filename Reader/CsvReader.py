import csv
from typing import List

class semicolon(csv.excel):
    """An excel csv dialect using semicolons as delimiters."""

    delimiter = ";"

    def __init__(self):
        super().__init__()

def readFile(filePath: str, dialect=None) -> List[List[str]]:
    """Reads a cvs file and returns a list of lists, each representing a row within the file."""

    with open(filePath, newline='', encoding='ISO-8859-1') as csvfile:
        lst = []

        if dialect is None:
            dialect = csv.excel

        reader = csv.reader((line.replace('\0', '') for line in csvfile), dialect)

        for row in reader:
            lst.append(row)

        return lst
