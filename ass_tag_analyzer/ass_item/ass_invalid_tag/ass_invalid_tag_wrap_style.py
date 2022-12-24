from .ass_invalid_tag import AssInvalidTag
from ..ass_tag_wrap_style import AssTagWrapStyle
from dataclasses import dataclass


@dataclass
class AssInvalidTagWrapStyle(AssTagWrapStyle, AssInvalidTag):
    pass
