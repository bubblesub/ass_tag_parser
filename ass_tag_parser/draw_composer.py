import typing as T

from ass_tag_parser.common import smart_float
from ass_tag_parser.draw_struct import *
from ass_tag_parser.errors import BaseError


class Composer:
    def visit(self, draw_commands: T.List[AssDrawCmd]) -> str:
        ret = []
        for cmd in draw_commands:
            assert isinstance(cmd, AssDrawCmd)

            visitor = getattr(self, "visit_" + cmd.__class__.__name__, None)
            if not visitor:
                raise NotImplementedError(f"not implemented ({cmd})")

            try:
                result = visitor(cmd)
            except (IndexError, KeyError, ValueError, TypeError) as ex:
                raise BaseError(ex)

            result = [
                smart_float(item) if isinstance(item, (int, float)) else item
                for item in result
            ]

            ret.append(" ".join(result))

        return " ".join(ret)

    def visit_AssDrawCmdMove(self, cmd: AssDrawCmdMove) -> T.Tuple[T.Any, ...]:
        return ("m" if cmd.close else "n", cmd.pos.x, cmd.pos.y)

    def visit_AssDrawCmdLine(self, cmd: AssDrawCmdLine) -> T.Tuple[T.Any, ...]:
        return ("l", *sum([(point.x, point.y) for point in cmd.points], ()))

    def visit_AssDrawCmdBezier(
        self, cmd: AssDrawCmdBezier
    ) -> T.Tuple[T.Any, ...]:
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

    def visit_AssDrawCmdSpline(
        self, cmd: AssDrawCmdSpline
    ) -> T.Tuple[T.Any, ...]:
        assert len(cmd.points) >= 3
        return ("s", *sum([(point.x, point.y) for point in cmd.points], ()))

    def visit_AssDrawCmdExtendSpline(
        self, cmd: AssDrawCmdExtendSpline
    ) -> T.Tuple[T.Any, ...]:
        return ("p", *sum([(point.x, point.y) for point in cmd.points], ()))

    def visit_AssDrawCmdCloseSpline(
        self, cmd: AssDrawCmdCloseSpline
    ) -> T.Tuple[T.Any, ...]:
        return ("c",)


def compose_draw_commands(commands: T.List[AssDrawCmd]) -> str:
    return Composer().visit(commands)
