from ass_tag_analyzer.ass_format import Format
from ..ass_tag_font_scale import AssTagFontScale, AssTagFontXScale, AssTagFontYScale
from dataclasses import dataclass


@dataclass
class AssValidTagFontScale(AssTagFontScale):
    def __str__(self):
        return f"\\{self.tag}"


@dataclass
class AssValidTagFontXScale(AssTagFontXScale):
    __scale: float

    def __init__(self, scale: float):
        self.scale = scale

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, value: float):
        self.__scale = 0 if value < 0 else value

    def __str__(self):
        return f"\\{self.tag}{Format.format_float(self.scale)}"


@dataclass
class AssValidTagFontYScale(AssTagFontYScale):
    __scale: float

    def __init__(self, scale: float):
        self.scale = scale

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, value: float):
        self.__scale = 0 if value < 0 else value

    def __str__(self):
        return f"\\{self.tag}{Format.format_float(self.scale)}"
