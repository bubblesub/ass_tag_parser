import parsimonious

from ass_tag_parser.common import ParsingError


class Serializer:
    def visit(self, draw_commands):
        ret = []
        for item in draw_commands:
            if "type" not in item:
                raise ParsingError("Item has no type")

            visitor = getattr(
                self, "visit_" + item["type"].replace("-", "_"), None
            )
            if not visitor:
                raise ParsingError("Unknown type %r" % item["type"])

            try:
                result = visitor(item)
            except (IndexError, KeyError, ValueError, TypeError) as ex:
                raise ParsingError(ex)

            ret.append(" ".join(str(item) for item in result))
        return " ".join(ret)

    def visit_move(self, item):
        return ("m", int(item["x"]), int(item["y"]))

    def visit_move_no_close(self, item):
        return ("n", int(item["x"]), int(item["y"]))

    def visit_line(self, item):
        return (
            "l",
            *sum(
                [
                    (int(point["x"]), int(point["y"]))
                    for point in item["points"]
                ],
                (),
            ),
        )

    def visit_bezier(self, item):
        if len(item["points"]) < 3:
            raise ValueError("Too few points in Bezier path")
        if len(item["points"]) > 3:
            raise ValueError("Too many points in Bezier path")
        return (
            "b",
            item["points"][0]["x"],
            item["points"][0]["y"],
            item["points"][1]["x"],
            item["points"][1]["y"],
            item["points"][2]["x"],
            item["points"][2]["y"],
        )

    def visit_cubic_bspline(self, item):
        if len(item["points"]) < 3:
            raise ValueError("Too few points in cubic b-spline")
        return (
            "s",
            *sum(
                [
                    (int(point["x"]), int(point["y"]))
                    for point in item["points"]
                ],
                (),
            ),
        )

    def visit_extend_bspline(self, item):
        return (
            "p",
            *sum(
                [
                    (int(point["x"]), int(point["y"]))
                    for point in item["points"]
                ],
                (),
            ),
        )

    def visit_close_bspline(self, item):
        return ("c",)


def compose_draw_commands(commands):
    return Serializer().visit(commands)
