from dataclasses import dataclass
from typing import Iterable, Optional, Union, cast

from ass_tag_parser.common import Meta
from ass_tag_parser.draw_struct import (
    AssDrawCmd,
    AssDrawCmdBezier,
    AssDrawCmdCloseSpline,
    AssDrawCmdExtendSpline,
    AssDrawCmdLine,
    AssDrawCmdMove,
    AssDrawCmdSpline,
    AssDrawPoint,
)
from ass_tag_parser.errors import ParseError
from ass_tag_parser.io import MyIO


@dataclass
class _ParseContext:
    io: MyIO


def _read_number(io: MyIO) -> Union[int, float]:
    ret = ""
    while io.peek(1).isspace():
        io.skip(1)

    while True:
        char = io.peek(1)
        if not char or char not in ".-0123456789":
            if not ret:
                raise ParseError(io.global_pos, "expected number")
            break
        if char == "-" and ret:
            raise ParseError(io.global_pos, "unexpected dash")
        if char == "." and "." in ret:
            raise ParseError(io.global_pos, "unexpected dot")
        ret += char
        io.skip(1)

    return float(ret) if "." in ret else int(ret)


def _read_point(io: MyIO) -> AssDrawPoint:
    return AssDrawPoint(_read_number(io), _read_number(io))


def _read_points(
    io: MyIO, min_count: int, max_count: Optional[int] = None
) -> Iterable[AssDrawPoint]:
    num = 0
    while num < min_count:
        yield _read_point(io)
        num += 1

    if max_count is not None:
        while num < max_count:
            yield _read_point(io)
            num += 1
    else:
        while not io.eof:
            while io.peek(1).isspace():
                io.skip(1)
            if io.peek(1) in ".-0123456789":
                yield _read_point(io)
            else:
                break


def _parse_draw_commands(ctx: _ParseContext) -> Iterable[AssDrawCmd]:
    while not ctx.io.eof:
        start_pos = ctx.io.global_pos
        cmd = ctx.io.read(1)

        ret: AssDrawCmd
        if cmd == "m":
            ret = AssDrawCmdMove(_read_point(ctx.io), close=True)
        elif cmd == "n":
            ret = AssDrawCmdMove(_read_point(ctx.io), close=False)
        elif cmd == "l":
            ret = AssDrawCmdLine(list(_read_points(ctx.io, min_count=1)))
        elif cmd == "b":
            ret = AssDrawCmdBezier(
                cast(
                    tuple[AssDrawPoint, AssDrawPoint, AssDrawPoint],
                    tuple(_read_points(ctx.io, min_count=3, max_count=3)),
                )
            )
        elif cmd == "s":
            ret = AssDrawCmdSpline(
                list(_read_points(ctx.io, min_count=3, max_count=None))
            )
        elif cmd == "p":
            ret = AssDrawCmdExtendSpline(
                list(_read_points(ctx.io, min_count=1))
            )
        elif cmd == "c":
            ret = AssDrawCmdCloseSpline()
        elif cmd.isspace():
            continue
        else:
            raise ParseError(start_pos, "unknown draw command " + cmd)
        ret.meta = Meta(
            start_pos,
            ctx.io.global_pos,
            ctx.io.global_text[start_pos : ctx.io.global_pos],
        )
        yield ret


def parse_draw_commands(text: str) -> list[AssDrawCmd]:
    ctx = _ParseContext(io=MyIO(text))
    return list(_parse_draw_commands(ctx))
