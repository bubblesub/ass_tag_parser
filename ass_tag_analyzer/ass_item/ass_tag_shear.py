from .ass_item import AssTag
from dataclasses import dataclass


@dataclass
class AssTagXShear(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L345-L352

    @property
    def tag(self) -> str:
        return "fax"


@dataclass
class AssTagYShear(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L353-L360

    @property
    def tag(self) -> str:
        return "fay"
