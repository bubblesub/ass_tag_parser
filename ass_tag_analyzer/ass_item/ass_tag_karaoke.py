from .ass_item import AssTag
from dataclasses import dataclass


@dataclass
class AssTagKaraoke(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L809-L816

    @property
    def tag(self) -> str:
        return "k"


@dataclass
class AssTagKaraokeFill(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L793-L800
    is_short_tag: bool

    @property
    def tag(self) -> str:
        return "kf"

    @property
    def short_tag(self) -> str:
        return "K"


@dataclass
class AssTagKaraokeOutline(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L801-L808

    @property
    def tag(self) -> str:
        return "ko"
