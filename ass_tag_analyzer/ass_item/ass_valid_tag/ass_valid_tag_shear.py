from ass_tag_analyzer.ass_format import Format
from ..ass_tag_shear import AssTagXShear, AssTagYShear
from dataclasses import dataclass


@dataclass
class AssValidTagXShear(AssTagXShear):
    value: float

    def __str__(self):
        return f"\\{self.tag}{Format.format_float(self.value)}"


@dataclass
class AssValidTagYShear(AssTagYShear):
    value: float

    def __str__(self):
        return f"\\{self.tag}{Format.format_float(self.value)}"
