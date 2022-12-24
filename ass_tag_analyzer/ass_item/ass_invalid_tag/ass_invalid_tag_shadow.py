from .ass_invalid_tag import AssInvalidTag
from ..ass_tag_shadow import AssTagShadow, AssTagXShadow, AssTagYShadow
from dataclasses import dataclass


@dataclass
class AssInvalidTagShadow(AssTagShadow, AssInvalidTag):
    pass


@dataclass
class AssInvalidTagXShadow(AssTagXShadow, AssInvalidTag):
    pass


@dataclass
class AssInvalidTagYShadow(AssTagYShadow, AssInvalidTag):
    pass
