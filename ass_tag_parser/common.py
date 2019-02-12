import pathlib
import typing as T
from dataclasses import dataclass

DATA_DIR = pathlib.Path(__file__).parent / "data"


@dataclass
class Meta:
    start: int
    end: int
    text: str


def flatten(items: T.Any) -> T.List[T.Any]:
    if isinstance(items, (list, tuple)):
        return [item for sublist in items for item in flatten(sublist)]
    return [items]


def smart_float(value: T.Union[int, float, None]) -> str:
    if value is None:
        return ""
    return "{}".format(float(value)).rstrip("0").rstrip(".")


def smart_int(value: T.Union[int, None]) -> str:
    if value is None:
        return ""
    return str(value)


def smart_str(value: T.Union[str, None]) -> str:
    if value is None:
        return ""
    return value


def smart_bool(value: T.Union[bool, int, None]) -> str:
    if value is None:
        return ""
    if value is True:
        return "1"
    if value is False:
        return "0"
    return "1" if value >= 1 else "0"
