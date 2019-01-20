import parsimonious

from ass_tag_parser.common import DATA_DIR, ParsingError, flatten

GRAMMAR_TEXT = (DATA_DIR / "draw_bnf.txt").read_text()
GRAMMAR = parsimonious.Grammar(GRAMMAR_TEXT)


class NodeVisitor(parsimonious.NodeVisitor):
    def generic_visit(self, _node, visited_nodes):
        return visited_nodes

    def visit_draw_commands(self, _node, visited_nodes):
        return flatten(visited_nodes)

    def visit_draw_command(self, _node, visited_nodes):
        return visited_nodes

    def visit_pos(self, node, _visited_nodes):
        return int(node.text)

    def visit_draw_command_move(self, node, visited_nodes):
        return {
            "pos": (node.start, node.end),
            "type": "move",
            "x": visited_nodes[2],
            "y": visited_nodes[4],
        }

    def visit_draw_command_move_no_close(self, node, visited_nodes):
        return {
            "pos": (node.start, node.end),
            "type": "move-no-close",
            "x": visited_nodes[2],
            "y": visited_nodes[4],
        }

    def visit_draw_command_line(self, node, visited_nodes):
        return {
            "pos": (node.start, node.end),
            "type": "line",
            "points": [
                {"x": item[1], "y": item[3]} for item in visited_nodes[1]
            ],
        }

    def visit_draw_command_bezier(self, node, visited_nodes):
        return {
            "pos": (node.start, node.end),
            "type": "bezier",
            "points": [
                {"x": visited_nodes[2], "y": visited_nodes[4]},
                {"x": visited_nodes[6], "y": visited_nodes[8]},
                {"x": visited_nodes[10], "y": visited_nodes[12]},
            ],
        }

    def visit_draw_command_cubic_spline(self, node, visited_nodes):
        return {
            "pos": (node.start, node.end),
            "type": "cubic-bspline",
            "points": [
                {"x": visited_nodes[2], "y": visited_nodes[4]},
                {"x": visited_nodes[6], "y": visited_nodes[8]},
            ]
            + [{"x": item[1], "y": item[3]} for item in visited_nodes[9]],
        }

    def visit_draw_command_extend_spline(self, node, visited_nodes):
        return {
            "pos": (node.start, node.end),
            "type": "extend-bspline",
            "points": [
                {"x": item[1], "y": item[3]} for item in visited_nodes[1]
            ],
        }

    def visit_draw_command_close_spline(self, node, _visited_nodes):
        return {"pos": (node.start, node.end), "type": "close-bspline"}


def parse_draw_commands(text):
    try:
        node = GRAMMAR.parse(text)
        return NodeVisitor().visit(node)
    except parsimonious.exceptions.ParseError as ex:
        raise ParsingError(ex)
