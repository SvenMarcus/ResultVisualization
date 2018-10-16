import numpy as np

from typing import Any, List


def isNumber(obj: Any) -> bool:
    return isinstance(obj, (float, int, np.number, np.int_, np.int8, np.int16, np.int32, np.int64, np.float_))


def tryConvertToFloat(obj: Any) -> float:
    """Tries to convert an object to a floating point number. Returns None if the conversion failed."""

    try:
        return float(obj)
    except:
        return None


def tryConvertToInt(obj: Any) -> int:
    """Tries to convert an object to an integer. Returns None if the conversion failed."""

    try:
        return int(obj)
    except:
        return None


def transposeList(data: List[List]) -> List[List]:
    return list(map(list, zip(*data)))
