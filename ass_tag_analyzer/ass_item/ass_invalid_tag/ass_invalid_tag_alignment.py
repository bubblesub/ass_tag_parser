from .ass_invalid_tag import AssInvalidTag
from ..ass_tag_alignment import AssTagAlignment
from dataclasses import dataclass


@dataclass
class AssInvalidTagAlignment(AssTagAlignment, AssInvalidTag):
    pass
