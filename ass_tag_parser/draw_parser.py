import typing as T
from dataclasses import dataclass

from ass_tag_parser.draw_struct import *
from ass_tag_parser.errors import ParseError
from ass_tag_parser.io import MyIO


@dataclass
class _ParseContext:
    io: MyIO


def _read_number(io: MyIO) -> T.Union[int, float]:
    ret = ""
    while io.peek(1).isspace():
        io.skip(1)

    while True:
        c = io.peek(1)
        if not c or c not in ".-0123456789":
            if not ret:
                raise ParseError(io.global_pos, "expected number")
            break
        if c == "-" and ret:
            raise ParseError(io.global_pos, "unexpected dash")
        if c == "." and "." in ret:
            raise ParseError(io.global_pos, "unexpected dot")
        ret += c
        io.skip(1)

    return float(ret) if "." in ret else int(ret)


def _read_point(io: MyIO) -> AssDrawPoint:
    return AssDrawPoint(_read_number(io), _read_number(io))


def _read_points(
    io: MyIO, min: int, max: T.Optional[int] = None
) -> T.Iterable[AssDrawPoint]:
    num = 0
    while num < min:
        yield _read_point(io)
        num += 1

    if max is not None:
        while num < max:
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


def _parse_draw_commands(ctx: _ParseContext) -> T.Iterable[AssDrawCmd]:
    while not ctx.io.eof:
        start_pos = ctx.io.global_pos
        cmd = ctx.io.read(1)

        ret: AssDrawCmd
        if cmd == "m":
            ret = AssDrawCmdMove(_read_point(ctx.io), close=True)
        elif cmd == "n":
            ret = AssDrawCmdMove(_read_point(ctx.io), close=False)
        elif cmd == "l":
            ret = AssDrawCmdLine(list(_read_points(ctx.io, min=1)))
        elif cmd == "b":
            ret = AssDrawCmdBezier(tuple(_read_points(ctx.io, min=3, max=3)))
        elif cmd == "s":
            ret = AssDrawCmdSpline(list(_read_points(ctx.io, min=3, max=None)))
        elif cmd == "p":
            ret = AssDrawCmdExtendSpline(list(_read_points(ctx.io, min=1)))
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


def parse_draw_commands(text: str) -> T.List[AssDrawCmd]:
    ctx = _ParseContext(io=MyIO(text))
    return list(_parse_draw_commands(ctx))
