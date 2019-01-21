import typing as T
from dataclasses import dataclass

from ass_tag_parser.common import Meta


class AssItem:
    meta: T.Optional[Meta] = None


class AssTag(AssItem):
    pass


@dataclass
class AssTagComment(AssTag):
    text: str


@dataclass
class AssTagBold(AssTag):
    enabled: T.Optional[bool] = None
    weight: T.Optional[int] = None


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
    times: T.Optional[int] = None


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
    x1: float
    y1: float
    x2: float
    y2: float
    time1: T.Optional[float] = None
    time2: T.Optional[float] = None


@dataclass
class AssTagPosition(AssTag):
    x: T.Optional[float] = None
    y: T.Optional[float] = None


@dataclass
class AssTagRotationOrigin(AssTag):
    x: T.Optional[float] = None
    y: T.Optional[float] = None


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
class AssTagKaraoke(AssTag):
    duration: float
    karaoke_type: int


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
    time1: float
    time2: float


@dataclass
class AssTagFadeComplex(AssTag):
    alpha1: int
    alpha2: int
    alpha3: int
    time1: float
    time2: float
    time3: float
    time4: float


@dataclass
class AssTagXShear(AssTag):
    value: T.Optional[float] = None


@dataclass
class AssTagYShear(AssTag):
    value: T.Optional[float] = None


@dataclass
class AssTagAnimation(AssTag):
    tags: T.List[AssTag]
    time1: T.Optional[float] = None
    time2: T.Optional[float] = None
    acceleration: T.Optional[float] = None


@dataclass
class AssTagBaselineOffset(AssTag):
    y: float


@dataclass
class AssTagDrawingMode(AssTag):
    scale: int


@dataclass
class AssTagClipRectangle(AssTag):
    x1: float
    y1: float
    x2: float
    y2: float
    inverse: bool


@dataclass
class AssTagClipVector(AssTag):
    scale: T.Optional[int]
    path: str
    inverse: bool


@dataclass
class AssTagListOpening(AssItem):
    pass


@dataclass
class AssTagListEnding(AssItem):
    pass


@dataclass
class AssText(AssItem):
    text: str
