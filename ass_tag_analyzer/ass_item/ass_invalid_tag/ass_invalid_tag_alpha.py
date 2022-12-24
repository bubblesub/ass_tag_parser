from .ass_invalid_tag import AssInvalidTag
from ..ass_tag_alpha import (
    AssTagAlpha,
    AssTagPrimaryAlpha,
    AssTagSecondaryAlpha,
    AssTagOutlineAlpha,
    AssTagBackgroundAlpha,
)
from dataclasses import dataclass


@dataclass
class AssInvalidTagAlpha(AssTagAlpha, AssInvalidTag):
    pass


@dataclass
class AssInvalidTagPrimaryAlpha(AssTagPrimaryAlpha, AssInvalidTag):
    pass


@dataclass
class AssInvalidTagSecondaryAlpha(AssTagSecondaryAlpha, AssInvalidTag):
    pass


@dataclass
class AssInvalidTagOutlineAlpha(AssTagOutlineAlpha, AssInvalidTag):
    pass


@dataclass
class AssInvalidTagBackgroundAlpha(AssTagBackgroundAlpha, AssInvalidTag):
    pass
