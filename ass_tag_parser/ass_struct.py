from dataclasses import dataclass, field
from typing import Optional

from ass_tag_parser.common import Meta
from ass_tag_parser.draw_struct import AssDrawCmd


class AssItem:
    meta: Optional[Meta] = None


class AssTag(AssItem):
    pass


@dataclass
class AssTagComment(AssTag):
    text: str


@dataclass
class AssTagBold(AssTag):
    enabled: Optional[bool] = None
    weight: Optional[int] = None


@dataclass
class AssTagItalic(AssTag):
    enabled: Optional[bool] = None


@dataclass
class AssTagUnderline(AssTag):
    enabled: Optional[bool] = None


@dataclass
class AssTagStrikeout(AssTag):
    enabled: Optional[bool] = None


@dataclass
class AssTagBorder(AssTag):
    size: Optional[float] = None


@dataclass
class AssTagXBorder(AssTag):
    size: Optional[float] = None


@dataclass
class AssTagYBorder(AssTag):
    size: Optional[float] = None


@dataclass
class AssTagShadow(AssTag):
    size: Optional[float] = None


@dataclass
class AssTagXShadow(AssTag):
    size: Optional[float] = None


@dataclass
class AssTagYShadow(AssTag):
    size: Optional[float] = None


@dataclass
class AssTagBlurEdges(AssTag):
    times: Optional[int] = None


@dataclass
class AssTagBlurEdgesGauss(AssTag):
    weight: Optional[float] = None


@dataclass
class AssTagFontName(AssTag):
    name: Optional[str] = None


@dataclass
class AssTagFontEncoding(AssTag):
    encoding: Optional[int] = None


@dataclass
class AssTagFontSize(AssTag):
    size: Optional[int] = None


@dataclass
class AssTagFontXScale(AssTag):
    scale: Optional[float] = None


@dataclass
class AssTagFontYScale(AssTag):
    scale: Optional[float] = None


@dataclass
class AssTagLetterSpacing(AssTag):
    spacing: Optional[float] = None


@dataclass
class AssTagMove(AssTag):
    x1: float
    y1: float
    x2: float
    y2: float
    time1: Optional[float] = None
    time2: Optional[float] = None


@dataclass
class AssTagPosition(AssTag):
    x: Optional[float] = None
    y: Optional[float] = None


@dataclass
class AssTagRotationOrigin(AssTag):
    x: Optional[float] = None
    y: Optional[float] = None


@dataclass
class AssTagXRotation(AssTag):
    angle: Optional[float] = None


@dataclass
class AssTagYRotation(AssTag):
    angle: Optional[float] = None


@dataclass
class AssTagZRotation(AssTag):
    angle: Optional[float] = None
    short: bool = False


@dataclass
class AssTagAlignment(AssTag):
    alignment: Optional[int] = None
    legacy: bool = False


@dataclass
class AssTagResetStyle(AssTag):
    style: Optional[str] = None


@dataclass
class AssTagKaraoke(AssTag):
    duration: float
    karaoke_type: int


@dataclass
class AssTagColor(AssTag):
    red: Optional[int]
    green: Optional[int]
    blue: Optional[int]
    target: int
    short: bool = False


@dataclass
class AssTagAlpha(AssTag):
    value: Optional[int]
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
    value: Optional[float] = None


@dataclass
class AssTagYShear(AssTag):
    value: Optional[float] = None


@dataclass
class AssTagAnimation(AssTag):
    tags: list[AssTag]
    time1: Optional[float] = None
    time2: Optional[float] = None
    acceleration: Optional[float] = None


@dataclass
class AssTagBaselineOffset(AssTag):
    y: float


@dataclass
class AssTagDraw(AssTag):
    scale: int
    path: list[AssDrawCmd] = field(default_factory=list)


@dataclass
class AssTagClipRectangle(AssTag):
    x1: float
    y1: float
    x2: float
    y2: float
    inverse: bool


@dataclass
class AssTagClipVector(AssTag):
    scale: Optional[int]
    path: list[AssDrawCmd]
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
