from .ass_item import AssTag
from dataclasses import dataclass


@dataclass
class AssTagXRotation(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L487-L494

    @property
    def tag(self) -> str:
        return "frx"


@dataclass
class AssTagYRotation(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L495-L502

    @property
    def tag(self) -> str:
        return "fry"


@dataclass
class AssTagZRotation(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L503-L511
    is_short_tag: bool

    @property
    def tag(self) -> str:
        return "frz"

    @property
    def short_tag(self) -> str:
        return "fr"
