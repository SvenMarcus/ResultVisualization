import pandas as pd
from typing import List


def readFile(filePath: str, delimiter=None) -> List[List[str]]:
    dataFrame: pd.DataFrame = pd.read_csv(filePath, sep=delimiter, encoding='ISO-8859-1')
    dataFrame.dropna(inplace=True)
    values = list(dataFrame.values)
    values.insert(0, dataFrame.columns)
    return values
