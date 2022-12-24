from .ass_item import AssTag
from dataclasses import dataclass


@dataclass
class AssTagBorder(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L433-L444

    @property
    def tag(self) -> str:
        return "bord"


@dataclass
class AssTagXBorder(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L311-L319

    @property
    def tag(self) -> str:
        return "xbord"


@dataclass
class AssTagYBorder(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L320-L328

    @property
    def tag(self) -> str:
        return "ybord"
