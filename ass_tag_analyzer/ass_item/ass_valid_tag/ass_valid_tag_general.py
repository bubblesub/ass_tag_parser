from ass_tag_analyzer.ass_item.ass_item import AssItem
from ass_tag_analyzer.ass_format import Format
from ..ass_tag_general import (
    AssTagAnimation,
    AssTagBaselineOffset,
    AssTagBold,
    AssTagDraw,
    AssTagFontEncoding,
    AssTagFontName,
    AssTagFontSize,
    AssTagItalic,
    AssTagLetterSpacing,
    AssTagResetStyle,
    AssTagRotationOrigin,
    AssTagStrikeout,
    AssTagUnderline,
)
from dataclasses import dataclass
from typing import List, Optional


from ass_tag_analyzer.ass_type_parser import TypeParser


@dataclass
class AssValidTagBold(AssTagBold):
    __weight: int

    def __init__(self, weight: int):
        self.weight = weight

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, weight: int):
        weight = 400 if weight == 0 else weight
        weight = 700 if weight == 1 else weight

        if weight < 100:
            raise ValueError("Bold tag cannot be under 100 except 0 and 1")

        self.__weight = weight

    def __str__(self):
        weight = self.weight
        weight = 0 if weight == 400 else weight
        weight = 1 if weight == 700 else weight

        return f"\\{self.tag}{weight}"


@dataclass
class AssValidTagItalic(AssTagItalic):
    enabled: bool

    def __str__(self):
        return f"\\{self.tag}{int(self.enabled)}"


@dataclass
class AssValidTagUnderline(AssTagUnderline):
    enabled: bool

    def __str__(self):
        return f"\\{self.tag}{int(self.enabled)}"


@dataclass
class AssValidTagStrikeout(AssTagStrikeout):
    enabled: bool

    def __str__(self):
        return f"\\{self.tag}{int(self.enabled)}"


@dataclass
class AssValidTagFontName(AssTagFontName):
    __name: str

    def __init__(self, name: str):
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = TypeParser.strip_whitespace(name)

    def __str__(self):
        return f"\\{self.tag}{self.name}"


@dataclass
class AssValidTagFontEncoding(AssTagFontEncoding):
    encoding: int

    def __str__(self):
        return f"\\{self.tag}{self.encoding}"


@dataclass
class AssValidTagFontSize(AssTagFontSize):
    size: float

    def __str__(self):
        return f"\\{self.tag}{Format.format_float(self.size)}"


@dataclass
class AssValidTagLetterSpacing(AssTagLetterSpacing):
    spacing: float

    def __str__(self):
        return f"\\{self.tag}{Format.format_float(self.spacing)}"


@dataclass
class AssValidTagResetStyle(AssTagResetStyle):
    style: str

    def __str__(self):
        return f"\\{self.tag}{self.style}"


@dataclass
class AssValidTagAnimation(AssTagAnimation):
    tags: List[AssItem]
    acceleration: float = 1.0
    time1: Optional[int] = None
    time2: Optional[int] = None

    def __str__(self):
        tags_text = "".join([str(tag) for tag in self.tags])

        if (
            self.time1 is not None
            and self.time2 is not None
            and self.acceleration is not None
            and self.acceleration != 1
        ):
            return f"\\{self.tag}({self.time1},{self.time2},{Format.format_float(self.acceleration)},{tags_text})"
        elif self.time1 is not None and self.time2 is not None:
            return f"\\{self.tag}({self.time1},{self.time2},{tags_text})"
        elif self.acceleration is not None and self.acceleration != 1:
            return f"\\{self.tag}({Format.format_float(self.acceleration)},{tags_text})"
        else:
            return f"\\{self.tag}({tags_text})"


@dataclass
class AssValidTagBaselineOffset(AssTagBaselineOffset):
    offset: float

    def __str__(self):
        return f"\\{self.tag}{Format.format_float(self.offset)}"


@dataclass
class AssValidTagRotationOrigin(AssTagRotationOrigin):
    x: float
    y: float

    def __str__(self):
        return (
            f"\\{self.tag}({Format.format_float(self.x)},{Format.format_float(self.y)})"
        )


@dataclass
class AssValidTagDraw(AssTagDraw):
    __scale: int

    def __init__(self, scale: int):
        self.scale = scale

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, value: int):
        self.__scale = 0 if value < 0 else value

    def __str__(self):
        return f"\\{self.tag}{self.scale}"
