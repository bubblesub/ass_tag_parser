from .ass_item import AssTag
from dataclasses import dataclass


@dataclass
class AssTagBold(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L781-L786

    @property
    def tag(self) -> str:
        return "b"


@dataclass
class AssTagItalic(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L787-L792

    @property
    def tag(self) -> str:
        return "i"


@dataclass
class AssTagUnderline(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L838-L845

    @property
    def tag(self) -> str:
        return "u"


@dataclass
class AssTagStrikeout(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L830-L837

    @property
    def tag(self) -> str:
        return "s"


@dataclass
class AssTagFontName:
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L512-L522

    @property
    def tag(self) -> str:
        return "fn"


@dataclass
class AssTagFontEncoding(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L858-L864
    # https://learn.microsoft.com/en-us/openspecs/office_file_formats/ms-one/64e2db6e-6eeb-443c-9ccf-0f72b37ba411

    @property
    def tag(self) -> str:
        return "fe"


@dataclass
class AssTagFontSize(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L421-L432

    @property
    def tag(self) -> str:
        return "fs"


@dataclass
class AssTagLetterSpacing(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L413-L420

    @property
    def tag(self) -> str:
        return "fsp"


@dataclass
class AssTagResetStyle(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L761-L767

    @property
    def tag(self) -> str:
        return "r"


@dataclass
class AssTagAnimation(AssTag):
    # https://github.com/libass/libass/blob/5f57443f1784434fe8961275da08be6d6febc688/libass/ass_parse.c#L626-L684
    @property
    def tag(self) -> str:
        return "t"


@dataclass
class AssTagBaselineOffset(AssTag):
    # https://github.com/libass/libass/blob/5f57443f1784434fe8961275da08be6d6febc688/libass/ass_parse.c#L846-L848

    @property
    def tag(self) -> str:
        return "pbo"


@dataclass
class AssTagRotationOrigin(AssTag):
    # https://github.com/libass/libass/blob/44f6532daf5eb13cb1aa95f5449a77b5df1dd85b/libass/ass_parse.c#L613-L625

    @property
    def tag(self) -> str:
        return "org"


@dataclass
class AssTagDraw(AssTag):
    # https://github.com/libass/libass/blob/5f57443f1784434fe8961275da08be6d6febc688/libass/ass_parse.c#L849-L852

    @property
    def tag(self) -> str:
        return "p"
