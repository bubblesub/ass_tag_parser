from .ass_item import AssTag
from dataclasses import dataclass


@dataclass
class AssTagAlpha(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L523-L539

    @property
    def tag(self) -> str:
        return "alpha"


@dataclass
class AssTagPrimaryAlpha(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L733-L739

    @property
    def tag(self) -> str:
        return "1a"


@dataclass
class AssTagSecondaryAlpha(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L740-L746

    @property
    def tag(self) -> str:
        return "2a"


@dataclass
class AssTagOutlineAlpha(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L747-L753

    @property
    def tag(self) -> str:
        return "3a"


@dataclass
class AssTagBackgroundAlpha(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L754-L760

    @property
    def tag(self) -> str:
        return "4a"
