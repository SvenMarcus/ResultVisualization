import pandas as pd
import numpy as np
from typing import List


def readFile(filePath: str, delimiter=None) -> List[List[str]]:
    dataFrame: pd.DataFrame = pd.read_csv(filePath, sep=delimiter, encoding='ISO-8859-1')
    dataFrame.dropna(inplace=True)
    values = dataFrame.values
    values = np.insert(values, 0, dataFrame.columns.values, axis=0)
    return values
