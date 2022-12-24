from ass_tag_analyzer.ass_format import Format
from ..ass_tag_border import AssTagBorder, AssTagXBorder, AssTagYBorder
from dataclasses import dataclass


@dataclass
class AssValidTagBorder(AssTagBorder):
    __size: float

    def __init__(self, size: float):
        self.size = size

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value: float):
        self.__size = 0 if value < 0 else value

    def __str__(self):
        return f"\\{self.tag}{Format.format_float(self.size)}"


@dataclass
class AssValidTagXBorder(AssTagXBorder):
    __size: float

    def __init__(self, size: float):
        self.size = size

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value: float):
        self.__size = 0 if value < 0 else value

    def __str__(self):
        return f"\\{self.tag}{Format.format_float(self.size)}"


@dataclass
class AssValidTagYBorder(AssTagYBorder):
    __size: float

    def __init__(self, size: float):
        self.size = size

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value: float):
        self.__size = 0 if value < 0 else value

    def __str__(self):
        return f"\\{self.tag}{Format.format_float(self.size)}"
