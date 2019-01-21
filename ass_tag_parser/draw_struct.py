import typing as T
from dataclasses import dataclass

from ass_tag_parser.common import Meta


@dataclass
class AssDrawPoint:
    x: float
    y: float


class AssDrawCmd:
    meta: T.Optional[Meta] = None


@dataclass
class AssDrawCmdMove(AssDrawCmd):
    pos: AssDrawPoint
    close: bool


@dataclass
class AssDrawCmdLine(AssDrawCmd):
    points: T.List[AssDrawPoint]


@dataclass
class AssDrawCmdBezier(AssDrawCmd):
    points: T.Tuple[AssDrawPoint, AssDrawPoint, AssDrawPoint]


@dataclass
class AssDrawCmdSpline(AssDrawCmd):
    points: T.List[AssDrawPoint]


@dataclass
class AssDrawCmdExtendSpline(AssDrawCmd):
    points: T.List[AssDrawPoint]


@dataclass
class AssDrawCmdCloseSpline(AssDrawCmd):
    pass
