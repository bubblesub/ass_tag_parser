from .ass_item import AssTag
from dataclasses import dataclass


@dataclass
class AssTagPrimaryColor(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L705-L711
    is_short_tag: bool

    @property
    def tag(self) -> str:
        return "1c"

    @property
    def short_tag(self) -> str:
        return "c"


@dataclass
class AssTagSecondaryColor(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L712-L718

    @property
    def tag(self) -> str:
        return "2c"


@dataclass
class AssTagOutlineColor(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L719-L725

    @property
    def tag(self) -> str:
        return "3c"


@dataclass
class AssTagBackgroundColor(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L726-L732

    @property
    def tag(self) -> str:
        return "4c"
