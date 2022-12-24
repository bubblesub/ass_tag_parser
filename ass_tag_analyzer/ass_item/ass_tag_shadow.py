from .ass_item import AssTag
from dataclasses import dataclass


@dataclass
class AssTagShadow(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L817-L829

    @property
    def tag(self) -> str:
        return "shad"


@dataclass
class AssTagXShadow(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L329-L336

    @property
    def tag(self) -> str:
        return "xshad"


@dataclass
class AssTagYShadow(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L337-L344

    @property
    def tag(self) -> str:
        return "yshad"
