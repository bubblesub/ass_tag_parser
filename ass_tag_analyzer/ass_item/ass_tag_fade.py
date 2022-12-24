from .ass_item import AssTag
from dataclasses import dataclass


@dataclass
class AssTagFade(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L578-L612

    @property
    def tag(self) -> str:
        return "fad"


@dataclass
class AssTagFadeComplex(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L578-L612

    @property
    def tag(self) -> str:
        return "fade"
