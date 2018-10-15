from typing import Any


def isNumber(obj: Any) -> bool:
    return isinstance(obj, (float, int))


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
