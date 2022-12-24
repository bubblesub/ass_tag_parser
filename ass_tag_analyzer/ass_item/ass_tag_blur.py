from .ass_item import AssTag
from dataclasses import dataclass


@dataclass
class AssTagBlurEdges(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L768-L780

    @property
    def tag(self) -> str:
        return "be"


@dataclass
class AssTagBlurEdgesGauss(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L381-L391

    @property
    def tag(self) -> str:
        return "blur"
