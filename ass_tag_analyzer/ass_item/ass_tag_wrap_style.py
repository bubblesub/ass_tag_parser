from .ass_item import AssTag
from dataclasses import dataclass
from enum import IntEnum


class WrapStyle(IntEnum):
    # https://aeg-dev.github.io/AegiSite/docs/3.2/ass_tags/#:~:text=Wrap%20style

    SMART_TOP = 0
    END_OF_LINE = 1
    NO_WORD = 2
    SMART_BOTTOM = 3


@dataclass
class AssTagWrapStyle(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L853-L857

    @property
    def tag(self) -> str:
        return "q"
