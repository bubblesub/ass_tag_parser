from ..ass_tag_color import (
    AssTagPrimaryColor,
    AssTagSecondaryColor,
    AssTagOutlineColor,
    AssTagBackgroundColor,
)
from dataclasses import dataclass


@dataclass
class AssValidTagPrimaryColor(AssTagPrimaryColor):
    red: int
    green: int
    blue: int

    def __str__(self):
        if self.is_short_tag:
            return f"\\{self.short_tag}&H{self.blue:02X}{self.green:02X}{self.red:02X}&"
        return f"\\{self.tag}&H{self.blue:02X}{self.green:02X}{self.red:02X}&"


@dataclass
class AssValidTagSecondaryColor(AssTagSecondaryColor):
    red: int
    green: int
    blue: int

    def __str__(self):
        return f"\\{self.tag}&H{self.blue:02X}{self.green:02X}{self.red:02X}&"


@dataclass
class AssValidTagOutlineColor(AssTagOutlineColor):
    red: int
    green: int
    blue: int

    def __str__(self):
        return f"\\{self.tag}&H{self.blue:02X}{self.green:02X}{self.red:02X}&"


@dataclass
class AssValidTagBackgroundColor(AssTagBackgroundColor):
    red: int
    green: int
    blue: int

    def __str__(self):
        return f"\\{self.tag}&H{self.blue:02X}{self.green:02X}{self.red:02X}&"
