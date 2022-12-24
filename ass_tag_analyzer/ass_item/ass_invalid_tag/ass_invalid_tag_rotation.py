from .ass_invalid_tag import AssInvalidTag
from ..ass_tag_rotation import AssTagZRotation
from dataclasses import dataclass


@dataclass
class AssInvalidTagZRotation(AssTagZRotation, AssInvalidTag):
    pass
