from ..ass_tag_rotation import AssTagXRotation, AssTagYRotation, AssTagZRotation
from ass_tag_analyzer.ass_format import Format
from dataclasses import dataclass


@dataclass
class AssValidTagXRotation(AssTagXRotation):
    angle: float

    def __str__(self):
        return f"\\{self.tag}{Format.format_float(self.angle)}"


@dataclass
class AssValidTagYRotation(AssTagYRotation):
    angle: float

    def __str__(self):
        return f"\\{self.tag}{Format.format_float(self.angle)}"


@dataclass
class AssValidTagZRotation(AssTagZRotation):
    angle: float

    def __str__(self):
        if self.is_short_tag:
            return f"\\{self.short_tag}{Format.format_float(self.angle)}"
        return f"\\{self.tag}{Format.format_float(self.angle)}"
