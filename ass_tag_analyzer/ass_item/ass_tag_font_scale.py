from .ass_item import AssTag
from dataclasses import dataclass


@dataclass
class AssTagFontScale(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L410-L412

    @property
    def tag(self) -> str:
        return "fsc"


@dataclass
class AssTagFontXScale(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L392-L400

    @property
    def tag(self) -> str:
        return "fscx"


@dataclass
class AssTagFontYScale(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L401-L409

    @property
    def tag(self) -> str:
        return "fscy"
