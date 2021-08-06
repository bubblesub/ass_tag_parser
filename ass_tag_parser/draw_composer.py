from typing import Any

from ass_tag_parser.common import smart_float
from ass_tag_parser.draw_struct import (
    AssDrawCmd,
    AssDrawCmdBezier,
    AssDrawCmdCloseSpline,
    AssDrawCmdExtendSpline,
    AssDrawCmdLine,
    AssDrawCmdMove,
    AssDrawCmdSpline,
)
from ass_tag_parser.errors import BaseError


class Composer:
    def visit(self, draw_commands: list[AssDrawCmd]) -> str:
        ret = []
        for cmd in draw_commands:
            assert isinstance(cmd, AssDrawCmd)

            visitor = getattr(self, "visit_" + cmd.__class__.__name__, None)
            if not visitor:
                raise NotImplementedError(f"not implemented ({cmd})")

            try:
                result = visitor(cmd)
            except (IndexError, KeyError, ValueError, TypeError) as exc:
                raise BaseError(exc) from exc

            result = [
                smart_float(item) if isinstance(item, (int, float)) else item
                for item in result
            ]

            ret.append(" ".join(result))

        return " ".join(ret)

    def visit_AssDrawCmdMove(self, cmd: AssDrawCmdMove) -> tuple[Any, ...]:
        return ("m" if cmd.close else "n", cmd.pos.x, cmd.pos.y)

    def visit_AssDrawCmdLine(self, cmd: AssDrawCmdLine) -> tuple[Any, ...]:
        return ("l", *sum([(point.x, point.y) for point in cmd.points], ()))

    def visit_AssDrawCmdBezier(self, cmd: AssDrawCmdBezier) -> tuple[Any, ...]:
        assert len(cmd.points) == 3
        return (
            "b",
            cmd.points[0].x,
            cmd.points[0].y,
            cmd.points[1].x,
            cmd.points[1].y,
            cmd.points[2].x,
            cmd.points[2].y,
        )

    def visit_AssDrawCmdSpline(self, cmd: AssDrawCmdSpline) -> tuple[Any, ...]:
        assert len(cmd.points) >= 3
        return ("s", *sum([(point.x, point.y) for point in cmd.points], ()))

    def visit_AssDrawCmdExtendSpline(
        self, cmd: AssDrawCmdExtendSpline
    ) -> tuple[Any, ...]:
        return ("p", *sum([(point.x, point.y) for point in cmd.points], ()))

    def visit_AssDrawCmdCloseSpline(
        self, _cmd: AssDrawCmdCloseSpline
    ) -> tuple[Any, ...]:
        return ("c",)


def compose_draw_commands(commands: list[AssDrawCmd]) -> str:
    return Composer().visit(commands)
