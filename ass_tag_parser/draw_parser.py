import parsimonious

from ass_tag_parser.common import DATA_DIR, flatten
from ass_tag_parser.draw_struct import *
from ass_tag_parser.errors import ParseError

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
        if "." in node.text:
            return float(node.text)
        return int(node.text)

    def visit_draw_command_move(self, node, visited_nodes):
        ret = AssDrawCmdMove(
            AssDrawPoint(x=visited_nodes[2], y=visited_nodes[4]), close=True
        )
        ret.meta = Meta(node.start, node.end, node.text)
        return ret

    def visit_draw_command_move_no_close(self, node, visited_nodes):
        ret = AssDrawCmdMove(
            AssDrawPoint(x=visited_nodes[2], y=visited_nodes[4]), close=False
        )
        ret.meta = Meta(node.start, node.end, node.text)
        return ret

    def visit_draw_command_line(self, node, visited_nodes):
        ret = AssDrawCmdLine(
            [AssDrawPoint(x=item[1], y=item[3]) for item in visited_nodes[1]]
        )
        ret.meta = Meta(node.start, node.end, node.text)
        return ret

    def visit_draw_command_bezier(self, node, visited_nodes):
        ret = AssDrawCmdBezier(
            (
                AssDrawPoint(visited_nodes[2], visited_nodes[4]),
                AssDrawPoint(visited_nodes[6], visited_nodes[8]),
                AssDrawPoint(visited_nodes[10], visited_nodes[12]),
            )
        )
        ret.meta = Meta(node.start, node.end, node.text)
        return ret

    def visit_draw_command_cubic_spline(self, node, visited_nodes):
        ret = AssDrawCmdSpline(
            [
                AssDrawPoint(visited_nodes[2], visited_nodes[4]),
                AssDrawPoint(visited_nodes[6], visited_nodes[8]),
            ]
            + [AssDrawPoint(item[1], item[3]) for item in visited_nodes[9]]
        )
        ret.meta = Meta(node.start, node.end, node.text)
        return ret

    def visit_draw_command_extend_spline(self, node, visited_nodes):
        ret = AssDrawCmdExtendSpline(
            [AssDrawPoint(item[1], item[3]) for item in visited_nodes[1]]
        )
        ret.meta = Meta(node.start, node.end, node.text)
        return ret

    def visit_draw_command_close_spline(self, node, _visited_nodes):
        ret = AssDrawCmdCloseSpline()
        ret.meta = Meta(node.start, node.end, node.text)
        return ret


def parse_draw_commands(text: str) -> T.List[AssDrawCmd]:
    try:
        node = GRAMMAR.parse(text)
        node_visitor = NodeVisitor()
        node_visitor.unwrapped_exceptions = (ParseError,)
        return node_visitor.visit(node)
    except parsimonious.exceptions.ParseError as ex:
        raise ParseError(ex.pos)
