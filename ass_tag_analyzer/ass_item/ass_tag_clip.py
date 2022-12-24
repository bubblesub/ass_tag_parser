from .ass_item import AssTag
from dataclasses import dataclass


@dataclass
class AssTagClipRectangle(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L685-L704
    invert: bool

    @property
    def tag(self) -> str:
        if self.invert:
            return "iclip"
        return "clip"


@dataclass
class AssTagClipVector(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L685-L704
    invert: bool

    @property
    def tag(self) -> str:
        if self.invert:
            return "iclip"
        return "clip"
