from .ass_invalid_tag import AssInvalidTag
from ..ass_tag_color import (
    AssTagPrimaryColor,
    AssTagSecondaryColor,
    AssTagOutlineColor,
    AssTagBackgroundColor,
)
from dataclasses import dataclass


@dataclass
class AssInvalidTagPrimaryColor(AssTagPrimaryColor, AssInvalidTag):
    pass


@dataclass
class AssInvalidTagSecondaryColor(AssTagSecondaryColor, AssInvalidTag):
    pass


@dataclass
class AssInvalidTagOutlineColor(AssTagOutlineColor, AssInvalidTag):
    pass


@dataclass
class AssInvalidTagBackgroundColor(AssTagBackgroundColor, AssInvalidTag):
    pass
