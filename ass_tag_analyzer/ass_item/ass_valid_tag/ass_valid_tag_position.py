from ass_tag_analyzer.ass_format import Format
from ..ass_tag_position import AssTagMove, AssTagPosition
from dataclasses import dataclass
from typing import Optional


@dataclass
class AssValidTagMove(AssTagMove):
    x1: float
    y1: float
    x2: float
    y2: float
    __time1: Optional[int] = None
    __time2: Optional[int] = None

    def __init__(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        time1: Optional[int] = None,
        time2: Optional[int] = None,
    ):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.time1 = time1
        self.time2 = time2

    @property
    def time1(self):
        return self.__time1

    @time1.setter
    def time1(self, value: int):
        if self.time2 is not None and value is not None and value > self.time2:
            self.__time1 = self.time2
            self.__time2 = value
        else:
            self.__time1 = value

    @property
    def time2(self):
        return self.__time2

    @time2.setter
    def time2(self, value: int):
        if self.time1 is not None and value is not None and value < self.time1:
            self.__time2 = self.time1
            self.__time1 = value
        else:
            self.__time2 = value

    def __str__(self):
        if self.time1 is not None and self.time2 is not None:
            return f"\\{self.tag}({Format.format_float(self.x1)},{Format.format_float(self.y1)},{Format.format_float(self.x2)},{Format.format_float(self.y2)},{self.time1},{self.time2})"
        return f"\\{self.tag}({Format.format_float(self.x1)},{Format.format_float(self.y1)},{Format.format_float(self.x2)},{Format.format_float(self.y2)})"


@dataclass
class AssValidTagPosition(AssTagPosition):
    x: float
    y: float

    def __str__(self):
        return (
            f"\\{self.tag}({Format.format_float(self.x)},{Format.format_float(self.y)})"
        )
