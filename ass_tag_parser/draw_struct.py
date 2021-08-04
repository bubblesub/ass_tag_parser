from dataclasses import dataclass
from typing import Optional

from ass_tag_parser.common import Meta


@dataclass
class AssDrawPoint:
    x: float
    y: float


class AssDrawCmd:
    meta: Optional[Meta] = None


@dataclass
class AssDrawCmdMove(AssDrawCmd):
    pos: AssDrawPoint
    close: bool


@dataclass
class AssDrawCmdLine(AssDrawCmd):
    points: list[AssDrawPoint]


@dataclass
class AssDrawCmdBezier(AssDrawCmd):
    points: tuple[AssDrawPoint, AssDrawPoint, AssDrawPoint]


@dataclass
class AssDrawCmdSpline(AssDrawCmd):
    points: list[AssDrawPoint]


@dataclass
class AssDrawCmdExtendSpline(AssDrawCmd):
    points: list[AssDrawPoint]


@dataclass
class AssDrawCmdCloseSpline(AssDrawCmd):
    pass
