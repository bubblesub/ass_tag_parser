from .ass_item import AssTag
from dataclasses import dataclass


@dataclass
class AssTagMove(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L445-L486

    @property
    def tag(self) -> str:
        return "move"


@dataclass
class AssTagPosition(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L562-L577

    @property
    def tag(self) -> str:
        return "pos"
