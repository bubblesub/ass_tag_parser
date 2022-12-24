from ass_tag_analyzer.ass_format import Format
from ..ass_tag_blur import AssTagBlurEdges, AssTagBlurEdgesGauss
from dataclasses import dataclass


@dataclass
class AssValidTagBlurEdges(AssTagBlurEdges):
    weight: float

    def __str__(self):
        return f"\\{self.tag}{Format.format_float(self.weight)}"


@dataclass
class AssValidTagBlurEdgesGauss(AssTagBlurEdgesGauss):
    __weight: float

    def __init__(self, weight: float):
        self.weight = weight

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self.__weight = 0 if value < 0 else value

    def __str__(self):
        return f"\\{self.tag}{Format.format_float(self.weight)}"
