import ass_tag_parser.common
import parsimonious


GRAMMAR_TEXT = (ass_tag_parser.common.DATA_DIR / 'draw_bnf.txt').read_text()
GRAMMAR = parsimonious.Grammar(GRAMMAR_TEXT)


class NodeVisitor(parsimonious.NodeVisitor):
    def generic_visit(self, node, visited_nodes):
        return visited_nodes

    def visit_draw_commands(self, node, visited_nodes):
        return ass_tag_parser.common.flatten(visited_nodes)

    def visit_draw_command(self, node, visited_nodes):
        return visited_nodes

    def visit_pos(self, node, visited_nodes):
        return int(node.text)

    def visit_draw_command_move(self, node, visited_nodes):
        return {
            'type': 'move',
            'x': visited_nodes[2],
            'y': visited_nodes[4],
        }

    def visit_draw_command_move_no_close(self, node, visited_nodes):
        return {
            'type': 'move-no-close',
            'x': visited_nodes[2],
            'y': visited_nodes[4],
        }

    def visit_draw_command_line(self, node, visited_nodes):
        return {
            'type': 'line',
            'points': [
                {'x': item[1], 'y': item[3]}
                for item in visited_nodes[1]
            ],
        }

    def visit_draw_command_bezier(self, node, visited_nodes):
        return {
            'type': 'bezier',
            'points': [
                {'x': visited_nodes[2], 'y': visited_nodes[4]},
                {'x': visited_nodes[6], 'y': visited_nodes[8]},
                {'x': visited_nodes[10], 'y': visited_nodes[12]},
            ],
        }

    def visit_draw_command_cubic_spline(self, node, visited_nodes):
        return {
            'type': 'cubic-bspline',
            'points': [
                {'x': visited_nodes[2], 'y': visited_nodes[4]},
                {'x': visited_nodes[6], 'y': visited_nodes[8]}
            ] + [
                {'x': item[1], 'y': item[3]}
                for item in visited_nodes[9]
            ],
        }

    def visit_draw_command_extend_spline(self, node, visited_nodes):
        return {
            'type': 'extend-bspline',
            'points': [
                {'x': item[1], 'y': item[3]}
                for item in visited_nodes[1]
            ],
        }

    def visit_draw_command_close_spline(self, node, visited_nodes):
        return {'type': 'close-bspline'}


def parse_draw_commands(text):
    try:
        node = GRAMMAR.parse(text)
        return NodeVisitor().visit(node)
    except parsimonious.exceptions.ParseError as ex:
        raise ass_tag_parser.common.ParsingError(ex)
