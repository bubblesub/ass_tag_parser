import pytest
import ass_tag_parser


GOOD_TEST_DATA = [
    ('m 0 0', [{'type': 'move', 'x': 0, 'y': 0}]),
    ('m -1 2', [{'type': 'move', 'x': -1, 'y': 2}]),
    ('n 1 2', [{'type': 'move-no-close', 'x': 1, 'y': 2}]),

    ('l 1 2', [{'type': 'line', 'points': [{'x': 1, 'y': 2}]}]),
    ('l 1 2 3 4', [{
        'type': 'line',
        'points': [{'x': 1, 'y': 2}, {'x': 3, 'y': 4}],
    }]),

    ('b 1 2 3 4 5 6', [{
        'type': 'bezier',
        'points': [
            {'x': 1, 'y': 2},
            {'x': 3, 'y': 4},
            {'x': 5, 'y': 6},
        ],
    }]),

    ('s 1 2 3 4 5 6', [{
        'type': 'cubic-bspline',
        'points': [
            {'x': 1, 'y': 2},
            {'x': 3, 'y': 4},
            {'x': 5, 'y': 6},
        ],
    }]),

    ('s 1 2 3 4 5 6 7 8 9 10', [{
        'type': 'cubic-bspline',
        'points': [
            {'x': 1, 'y': 2},
            {'x': 3, 'y': 4},
            {'x': 5, 'y': 6},
            {'x': 7, 'y': 8},
            {'x': 9, 'y': 10},
        ],
    }]),

    ('p 1 2', [{'type': 'extend-bspline', 'points': [{'x': 1, 'y': 2}]}]),
    ('p 1 2 3 4', [{
        'type': 'extend-bspline',
        'points': [{'x': 1, 'y': 2}, {'x': 3, 'y': 4}],
    }]),

    ('c', [{'type': 'close-bspline'}]),

    ('m 0 0 l 100 0 100 100 0 100', [
        {'type': 'move', 'x': 0, 'y': 0},
        {'type': 'line', 'points': [
            {'x': 100, 'y': 0},
            {'x': 100, 'y': 100},
            {'x': 0, 'y': 100},
        ]},
    ]),

    ('m 0 0 s 100 0 100 100 0 100 c', [
        {'type': 'move', 'x': 0, 'y': 0},
        {'type': 'cubic-bspline', 'points': [
            {'x': 100, 'y': 0},
            {'x': 100, 'y': 100},
            {'x': 0, 'y': 100},
        ]},
        {'type': 'close-bspline'},
    ]),

    ('m 0 0 s 100 0 100 100 0 100 p 0 0 100 0 100 100', [
        {'type': 'move', 'x': 0, 'y': 0},
        {'type': 'cubic-bspline', 'points': [
            {'x': 100, 'y': 0},
            {'x': 100, 'y': 100},
            {'x': 0, 'y': 100},
        ]},
        {'type': 'extend-bspline', 'points': [
            {'x': 0, 'y': 0},
            {'x': 100, 'y': 0},
            {'x': 100, 'y': 100},
        ]},
    ]),
]

BAD_TEST_DATA = [
    'm1 2',
    'm 1',
    'm 1 2 3',

    'l',
    'l 1',
    'l 1 2 3',
    'l 1 2 3 4 5',

    'b',
    'b 1',
    'b 1 2',
    'b 1 2 3',
    'b 1 2 3 4',
    'b 1 2 3 4 5',
    'b 1 2 3 4 5 6 7',
    'b 1 2 3 4 5 6 7 8',

    's',
    's 1',
    's 1 2',
    's 1 2 3',
    's 1 2 3 4',
    's 1 2 3 4 5',
    'p 1 2 3 4 5 6 7',

    'p 1',
    'p 1 2 3',
    'p 1 2 3 4 5',
]


@pytest.mark.parametrize('source,expected', GOOD_TEST_DATA)
def test_parsing_valid_text(source, expected):
    assert expected == ass_tag_parser.parse_draw_commands(source)


@pytest.mark.parametrize('source', BAD_TEST_DATA)
def test_parsing_invalid_text(source):
    with pytest.raises(ass_tag_parser.ParsingError):
        ass_tag_parser.parse_draw_commands(source)
