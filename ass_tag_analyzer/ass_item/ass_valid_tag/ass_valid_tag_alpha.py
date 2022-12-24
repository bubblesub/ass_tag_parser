from ..ass_tag_alpha import (
    AssTagAlpha,
    AssTagPrimaryAlpha,
    AssTagSecondaryAlpha,
    AssTagOutlineAlpha,
    AssTagBackgroundAlpha,
)
from dataclasses import dataclass


@dataclass
class AssValidTagAlpha(AssTagAlpha):
    value: int

    def __str__(self):
        return f"\\{self.tag}&H{self.value:02X}&"

@dataclass
class AssValidTagPrimaryAlpha(AssTagPrimaryAlpha):
    value: int

    def __str__(self):
        return f"\\{self.tag}&H{self.value:02X}&"


@dataclass
class AssValidTagSecondaryAlpha(AssTagSecondaryAlpha):
    value: int

    def __str__(self):
        return f"\\{self.tag}&H{self.value:02X}&"


@dataclass
class AssValidTagOutlineAlpha(AssTagOutlineAlpha):
    value: int

    def __str__(self):
        return f"\\{self.tag}&H{self.value:02X}&"


@dataclass
class AssValidTagBackgroundAlpha(AssTagBackgroundAlpha):
    value: int

    def __str__(self):
        return f"\\{self.tag}&H{self.value:02X}&"
