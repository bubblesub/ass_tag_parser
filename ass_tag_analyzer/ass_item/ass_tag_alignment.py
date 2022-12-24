from .ass_item import AssTag
from dataclasses import dataclass
from enum import IntEnum


class Alignment(IntEnum):
    # https://aeg-dev.github.io/AegiSite/docs/3.2/ass_tags/#:~:text=Line%20alignment

    BOTTOM_LEFT = 1
    BOTTOM_CENTER = 2
    BOTTOM_RIGHT = 3
    MIDDLE_LEFT = 4
    MIDDLE_CENTER = 5
    MIDDLE_RIGHT = 6
    TOP_LEFT = 7
    TOP_CENTER = 8
    TOP_RIGHT = 9


class LegacyAlignment(IntEnum):
    # https://aeg-dev.github.io/AegiSite/docs/3.2/ass_tags/#:~:text=Line%20alignment%20(legacy)

    BOTTOM_LEFT = 1
    BOTTOM_CENTER = 2
    BOTTOM_RIGHT = 3
    MIDDLE_LEFT = 9
    MIDDLE_CENTER = 10
    MIDDLE_RIGHT = 11
    TOP_LEFT = 5
    TOP_CENTER = 6
    TOP_RIGHT = 7


@dataclass
class AssTagAlignment(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L540-L561
    is_legacy_tag: bool

    @property
    def tag(self) -> str:
        return "an"

    @property
    def legacy_tag(self) -> str:
        return "a"
