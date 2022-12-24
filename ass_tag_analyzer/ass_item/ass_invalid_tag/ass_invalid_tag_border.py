from .ass_invalid_tag import AssInvalidTag
from ..ass_tag_border import AssTagBorder, AssTagXBorder, AssTagYBorder
from dataclasses import dataclass


@dataclass
class AssInvalidTagBorder(AssTagBorder, AssInvalidTag):
    pass


@dataclass
class AssInvalidTagXBorder(AssTagXBorder, AssInvalidTag):
    pass


@dataclass
class AssInvalidTagYBorder(AssTagYBorder, AssInvalidTag):
    pass
