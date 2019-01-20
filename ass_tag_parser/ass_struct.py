import typing as T
from dataclasses import dataclass

from ass_tag_parser.common import Meta


class AssItem:
    pass


class AssTag(AssItem):
    meta: T.Optional[Meta] = None


@dataclass
class AssTagComment(AssTag):
    text: str


@dataclass
class AssTagBold(AssTag):
    enabled: T.Optional[bool] = None
    weight: T.Optional[float] = None


@dataclass
class AssTagItalic(AssTag):
    enabled: T.Optional[bool] = None


@dataclass
class AssTagUnderline(AssTag):
    enabled: T.Optional[bool] = None


@dataclass
class AssTagStrikeout(AssTag):
    enabled: T.Optional[bool] = None


@dataclass
class AssTagBorder(AssTag):
    size: T.Optional[float] = None


@dataclass
class AssTagXBorder(AssTag):
    size: T.Optional[float] = None


@dataclass
class AssTagYBorder(AssTag):
    size: T.Optional[float] = None


@dataclass
class AssTagShadow(AssTag):
    size: T.Optional[float] = None


@dataclass
class AssTagXShadow(AssTag):
    size: T.Optional[float] = None


@dataclass
class AssTagYShadow(AssTag):
    size: T.Optional[float] = None


@dataclass
class AssTagBlurEdges(AssTag):
    times: T.Optional[float] = None


@dataclass
class AssTagBlurEdgesGauss(AssTag):
    weight: T.Optional[float] = None


@dataclass
class AssTagFontName(AssTag):
    name: T.Optional[str] = None


@dataclass
class AssTagFontEncoding(AssTag):
    encoding: T.Optional[int] = None


@dataclass
class AssTagFontSize(AssTag):
    size: T.Optional[int] = None


@dataclass
class AssTagFontXScale(AssTag):
    scale: T.Optional[float] = None


@dataclass
class AssTagFontYScale(AssTag):
    scale: T.Optional[float] = None


@dataclass
class AssTagLetterSpacing(AssTag):
    spacing: T.Optional[float] = None


@dataclass
class AssTagMove(AssTag):
    x1: int
    y1: int
    x2: int
    y2: int
    time1: T.Optional[int] = None
    time2: T.Optional[int] = None


@dataclass
class AssTagPosition(AssTag):
    x: T.Optional[int] = None
    y: T.Optional[int] = None


@dataclass
class AssTagRotationOrigin(AssTag):
    x: T.Optional[int] = None
    y: T.Optional[int] = None


@dataclass
class AssTagXRotation(AssTag):
    angle: T.Optional[float] = None


@dataclass
class AssTagYRotation(AssTag):
    angle: T.Optional[float] = None


@dataclass
class AssTagZRotation(AssTag):
    angle: T.Optional[float] = None
    short: bool = False


@dataclass
class AssTagAlignment(AssTag):
    alignment: T.Optional[int] = None
    legacy: bool = False


@dataclass
class AssTagResetStyle(AssTag):
    style: T.Optional[str] = None


@dataclass
class AssTagKaraoke1(AssTag):
    duration: int


@dataclass
class AssTagKaraoke2(AssTag):
    duration: int


@dataclass
class AssTagKaraoke3(AssTag):
    duration: int


@dataclass
class AssTagKaraoke4(AssTag):
    duration: int


@dataclass
class AssTagColor(AssTag):
    red: T.Optional[int]
    green: T.Optional[int]
    blue: T.Optional[int]
    target: int
    short: bool = False


@dataclass
class AssTagAlpha(AssTag):
    value: T.Optional[int]
    target: int


@dataclass
class AssTagWrapStyle(AssTag):
    style: int


@dataclass
class AssTagFade(AssTag):
    time1: int
    time2: int


@dataclass
class AssTagFadeComplex(AssTag):
    alpha1: int
    alpha2: int
    alpha3: int
    time1: int
    time2: int
    time3: int
    time4: int


@dataclass
class AssTagXShear(AssTag):
    value: T.Optional[float] = None


@dataclass
class AssTagYShear(AssTag):
    value: T.Optional[float] = None


@dataclass
class AssTagAnimation(AssTag):
    tags: T.List[AssTag]
    time1: T.Optional[int] = None
    time2: T.Optional[int] = None
    acceleration: T.Optional[float] = None


@dataclass
class AssTagBaselineOffset(AssTag):
    y: int


@dataclass
class AssTagDrawingMode(AssTag):
    scale: int


@dataclass
class AssTagClipRectangle(AssTag):
    x1: int
    y1: int
    x2: int
    y2: int
    inverse: bool


@dataclass
class AssTagClipVector(AssTag):
    scale: T.Optional[int]
    path: str
    inverse: bool


class AssBlock(AssItem):
    meta: T.Optional[Meta] = None


@dataclass
class AssText(AssBlock):
    text: str


@dataclass
class AssTagList(AssBlock):
    tags: T.List[AssTag]


@dataclass
class AssLine:
    chunks: T.List[AssBlock]
