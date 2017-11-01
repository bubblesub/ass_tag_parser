import ass_tag_parser.common
import parsimonious


GRAMMAR_TEXT = (ass_tag_parser.common.DATA_DIR / 'draw_bnf.txt').read_text()
GRAMMAR = parsimonious.Grammar(GRAMMAR_TEXT)


class NodeVisitor(parsimonious.NodeVisitor):
    def generic_visit(self, _node, visited_nodes):
        return visited_nodes

    def visit_draw_commands(self, _node, visited_nodes):
        return ass_tag_parser.common.flatten(visited_nodes)

    def visit_draw_command(self, _node, visited_nodes):
        return visited_nodes

    def visit_pos(self, node, _visited_nodes):
        return int(node.text)

    def visit_draw_command_move(self, node, visited_nodes):
        return {
            'pos': (node.start, node.end),
            'type': 'move',
            'x': visited_nodes[2],
            'y': visited_nodes[4],
        }

    def visit_draw_command_move_no_close(self, node, visited_nodes):
        return {
            'pos': (node.start, node.end),
            'type': 'move-no-close',
            'x': visited_nodes[2],
            'y': visited_nodes[4],
        }

    def visit_draw_command_line(self, node, visited_nodes):
        return {
            'pos': (node.start, node.end),
            'type': 'line',
            'points': [
                {'x': item[1], 'y': item[3]}
                for item in visited_nodes[1]
            ],
        }

    def visit_draw_command_bezier(self, node, visited_nodes):
        return {
            'pos': (node.start, node.end),
            'type': 'bezier',
            'points': [
                {'x': visited_nodes[2], 'y': visited_nodes[4]},
                {'x': visited_nodes[6], 'y': visited_nodes[8]},
                {'x': visited_nodes[10], 'y': visited_nodes[12]},
            ],
        }

    def visit_draw_command_cubic_spline(self, node, visited_nodes):
        return {
            'pos': (node.start, node.end),
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
            'pos': (node.start, node.end),
            'type': 'extend-bspline',
            'points': [
                {'x': item[1], 'y': item[3]}
                for item in visited_nodes[1]
            ],
        }

    def visit_draw_command_close_spline(self, node, _visited_nodes):
        return {
            'pos': (node.start, node.end),
            'type': 'close-bspline',
        }


class Serializer:
    def visit(self, draw_commands):
        ret = []
        for item in draw_commands:
            if 'type' not in item:
                raise ass_tag_parser.common.ParsingError('Item has no type')

            visitor = getattr(
                self,
                'visit_' + item['type'].replace('-', '_'),
                None)
            if not visitor:
                raise ass_tag_parser.common.ParsingError(
                    'Unknown type %r' % item['type'])

            try:
                result = visitor(item)
            except (IndexError, KeyError, ValueError, TypeError) as ex:
                raise ass_tag_parser.common.ParsingError(ex)

            ret.append(' '.join(str(item) for item in result))
        return ' '.join(ret)

    def visit_move(self, item):
        return ('m', int(item['x']), int(item['y']))

    def visit_move_no_close(self, item):
        return ('n', int(item['x']), int(item['y']))

    def visit_line(self, item):
        return (
            'l',
            *sum([
                (int(point['x']), int(point['y']))
                for point in item['points']
            ], ())
        )

    def visit_bezier(self, item):
        if len(item['points']) < 3:
            raise ValueError('Too few points in Bezier path')
        if len(item['points']) > 3:
            raise ValueError('Too many points in Bezier path')
        return (
            'b',
            item['points'][0]['x'], item['points'][0]['y'],
            item['points'][1]['x'], item['points'][1]['y'],
            item['points'][2]['x'], item['points'][2]['y'])

    def visit_cubic_bspline(self, item):
        if len(item['points']) < 3:
            raise ValueError('Too few points in cubic b-spline')
        return ('s', *sum([
            (int(point['x']), int(point['y']))
            for point in item['points']], ()))

    def visit_extend_bspline(self, item):
        return ('p', *sum([
            (int(point['x']), int(point['y']))
            for point in item['points']], ()))

    def visit_close_bspline(self, item):
        return ('c',)


def parse_draw_commands(text):
    try:
        node = GRAMMAR.parse(text)
        return NodeVisitor().visit(node)
    except parsimonious.exceptions.ParseError as ex:
        raise ass_tag_parser.common.ParsingError(ex)


def serialize_draw_commands(commands):
    return Serializer().visit(commands)
