import pytest
import ass_tag_parser


GOOD_TEST_DATA = [
    (r'test', [{'type': 'text', 'text': 'test'}]),

    (r'{asdasd}', [{
        'type': 'tags',
        'children': [{'type': 'comment', 'text': 'asdasd'}],
    }]),

    (r'{\p2}m 3 4{\p0}', [
        {'type': 'tags', 'children': [{'type': 'drawing-mode', 'value': 2}]},
        {'type': 'text', 'text': 'm 3 4'},
        {'type': 'tags', 'children': [{'type': 'drawing-mode', 'value': 0}]},
    ]),

    (r'{\an5\an5}', [
        {'type': 'tags', 'children': [
            {'type': 'alignment', 'alignment': 5, 'legacy': False},
            {'type': 'alignment', 'alignment': 5, 'legacy': False}
        ]},
    ]),

    (r'{\an5}{\an5}', [
        {'type': 'tags', 'children': [
            {'type': 'alignment', 'alignment': 5, 'legacy': False},
        ]},
        {'type': 'tags', 'children': [
            {'type': 'alignment', 'alignment': 5, 'legacy': False},
        ]},
    ]),

    (r'abc def{\an5}ghi jkl{\an5}123 456', [
        {'type': 'text', 'text': 'abc def'},
        {'type': 'tags', 'children': [
            {'type': 'alignment', 'alignment': 5, 'legacy': False},
        ]},
        {'type': 'text', 'text': 'ghi jkl'},
        {'type': 'tags', 'children': [
            {'type': 'alignment', 'alignment': 5, 'legacy': False},
        ]},
        {'type': 'text', 'text': '123 456'},
    ]),

    (r'I am {\b1}not{\b0} amused.', [
        {'type': 'text', 'text': 'I am '},
        {'type': 'tags', 'children': [
            {'type': 'bold', 'enabled': True},
        ]},
        {'type': 'text', 'text': 'not'},
        {'type': 'tags', 'children': [
            {'type': 'bold', 'enabled': False},
        ]},
        {'type': 'text', 'text': ' amused.'},
    ]),

    (r'{\b100}How {\b300}bold {\b500}can {\b700}you {\b900}get?', [
        {'type': 'tags', 'children': [
            {'type': 'bold', 'weight': 100},
        ]},
        {'type': 'text', 'text': 'How '},
        {'type': 'tags', 'children': [
            {'type': 'bold', 'weight': 300},
        ]},
        {'type': 'text', 'text': 'bold '},
        {'type': 'tags', 'children': [
            {'type': 'bold', 'weight': 500},
        ]},
        {'type': 'text', 'text': 'can '},
        {'type': 'tags', 'children': [
            {'type': 'bold', 'weight': 700},
        ]},
        {'type': 'text', 'text': 'you '},
        {'type': 'tags', 'children': [
            {'type': 'bold', 'weight': 900},
        ]},
        {'type': 'text', 'text': 'get?'},
    ]),

    (r'-Hey\N{\rAlternate}-Huh?\N{\r}-Who are you?', [
        {'type': 'text', 'text': '-Hey\\N'},
        {'type': 'tags', 'children': [
            {'type': 'reset-style', 'style': 'Alternate'},
        ]},
        {'type': 'text', 'text': '-Huh?\\N'},
        {'type': 'tags', 'children': [
            {'type': 'reset-style', 'style': None},
        ]},
        {'type': 'text', 'text': '-Who are you?'},
    ]),

    (r'{\1c&HFF0000&\t(\1c&H0000FF&)}Hello!', [
        {'type': 'tags', 'children': [
            {'type': 'color-primary', 'red': 0, 'green': 0, 'blue': 255},
            {
                'type': 'animation',
                'start': None,
                'end': None,
                'accel': None,
                'children': [
                    {
                        'type': 'color-primary',
                        'red': 255,
                        'green': 0,
                        'blue': 0,
                    },
                ],
            },
        ]},
        {'type': 'text', 'text': 'Hello!'},
    ]),

    (r'{\an5\t(0,5000,\frz3600)}Wheee', [
        {'type': 'tags', 'children': [
            {'type': 'alignment', 'alignment': 5, 'legacy': False},
            {
                'type': 'animation',
                'start': 0,
                'end': 5000,
                'accel': None,
                'children': [{'type': 'rotation-z', 'angle': 3600}],
            },
        ]},
        {'type': 'text', 'text': 'Wheee'},
    ]),

    (r'{\an5\t(0,5000,0.5,\frz3600)}Wheee', [
        {'type': 'tags', 'children': [
            {'type': 'alignment', 'alignment': 5, 'legacy': False},
            {
                'type': 'animation',
                'start': 0,
                'end': 5000,
                'accel': 0.5,
                'children': [{'type': 'rotation-z', 'angle': 3600}],
            },
        ]},
        {'type': 'text', 'text': 'Wheee'},
    ]),

    (r'{\an5\fscx0\fscy0\t(0,500,\fscx100\fscy100)}Boo!', [
        {'type': 'tags', 'children': [
            {'type': 'alignment', 'alignment': 5, 'legacy': False},
            {'type': 'font-scale-x', 'scale': 0},
            {'type': 'font-scale-y', 'scale': 0},
            {
                'type': 'animation',
                'start': 0,
                'end': 500,
                'accel': None,
                'children': [
                    {'type': 'font-scale-x', 'scale': 100},
                    {'type': 'font-scale-y', 'scale': 100},
                ],
            },
        ]},
        {'type': 'text', 'text': 'Boo!'},
    ]),

    (r'{comment\b1}', [
        {'type': 'tags', 'children': [
            {'type': 'comment', 'text': 'comment'},
            {'type': 'bold', 'enabled': True},
        ]},
    ]),

    (r'{\b1comment}', [
        {'type': 'tags', 'children': [
            {'type': 'bold', 'enabled': True},
            {'type': 'comment', 'text': 'comment'},
        ]},
    ]),

    (r'{\2a&HFF&comment}', [
        {'type': 'tags', 'children': [
            {'type': 'alpha-secondary', 'value': 0xFF},
            {'type': 'comment', 'text': 'comment'},
        ]},
    ]),

    (r'{\be2.2}', [
        {'type': 'tags', 'children': [
            {'type': 'blur-edges', 'value': 2},
            {'type': 'comment', 'text': '.2'},
        ]},
    ]),

    (r'{\fs5.4}', [
        {'type': 'tags', 'children': [
            {'type': 'font-size', 'size': 5},
            {'type': 'comment', 'text': '.4'},
        ]},
    ]),

    (r'{\k50.5}', [
        {'type': 'tags', 'children': [
            {'type': 'karaoke-1', 'duration': 500},
            {'type': 'comment', 'text': '.5'},
        ]},
    ]),

    (r'{\K50.5}', [
        {'type': 'tags', 'children': [
            {'type': 'karaoke-2', 'duration': 500},
            {'type': 'comment', 'text': '.5'},
        ]},
    ]),

    (r'{\kf50.5}', [
        {'type': 'tags', 'children': [
            {'type': 'karaoke-3', 'duration': 500},
            {'type': 'comment', 'text': '.5'},
        ]},
    ]),

    (r'{\ko50.5}', [
        {'type': 'tags', 'children': [
            {'type': 'karaoke-4', 'duration': 500},
            {'type': 'comment', 'text': '.5'},
        ]},
    ]),
]

GOOD_TEST_DATA_SINGLE_TAG = [
    (r'{\i1}', {'type': 'italics', 'enabled': True}),
    (r'{\i0}', {'type': 'italics', 'enabled': False}),
    (r'{\b300}', {'type': 'bold', 'weight': 300}),
    (r'{\b1}', {'type': 'bold', 'enabled': True}),
    (r'{\b0}', {'type': 'bold', 'enabled': False}),
    (r'{\u1}', {'type': 'underline', 'enabled': True}),
    (r'{\u0}', {'type': 'underline', 'enabled': False}),
    (r'{\s1}', {'type': 'strikeout', 'enabled': True}),
    (r'{\s0}', {'type': 'strikeout', 'enabled': False}),

    (r'{\bord0}', {'type': 'border', 'size': 0}),
    (r'{\xbord0}', {'type': 'border-x', 'size': 0}),
    (r'{\ybord0}', {'type': 'border-y', 'size': 0}),
    (r'{\bord4.4}', {'type': 'border', 'size': 4.4}),
    (r'{\xbord4.4}', {'type': 'border-x', 'size': 4.4}),
    (r'{\ybord4.4}', {'type': 'border-y', 'size': 4.4}),
    (r'{\shad0}', {'type': 'shadow', 'size': 0}),
    (r'{\xshad0}', {'type': 'shadow-x', 'size': 0}),
    (r'{\yshad0}', {'type': 'shadow-y', 'size': 0}),
    (r'{\shad4.4}', {'type': 'shadow', 'size': 4.4}),
    (r'{\xshad4.4}', {'type': 'shadow-x', 'size': 4.4}),
    (r'{\yshad4.4}', {'type': 'shadow-y', 'size': 4.4}),

    (r'{\be2}', {'type': 'blur-edges', 'value': 2}),
    (r'{\blur4.4}', {'type': 'blur-edges-gauss', 'value': 4.4}),

    (r'{\fnArial}', {'type': 'font-name', 'name': 'Arial'}),
    (r'{\fnComic Sans}', {'type': 'font-name', 'name': 'Comic Sans'}),
    (r'{\fn(Comic Sans)}', {'type': 'font-name', 'name': 'Comic Sans'}),
    (r'{\fe5}', {'type': 'font-encoding', 'encoding': 5}),
    (r'{\fs15}', {'type': 'font-size', 'size': 15}),
    (r'{\fscx5.5}', {'type': 'font-scale-x', 'scale': 5.5}),
    (r'{\fscy5.5}', {'type': 'font-scale-y', 'scale': 5.5}),
    (r'{\fsp5.5}', {'type': 'letter-spacing', 'value': 5.5}),
    (r'{\fsp-5.5}', {'type': 'letter-spacing', 'value': -5.5}),

    (r'{\frx5.5}', {'type': 'rotation-x', 'angle': 5.5}),
    (r'{\frx-5.5}', {'type': 'rotation-x', 'angle': -5.5}),
    (r'{\fry5.5}', {'type': 'rotation-y', 'angle': 5.5}),
    (r'{\fry-5.5}', {'type': 'rotation-y', 'angle': -5.5}),
    (r'{\frz5.5}', {'type': 'rotation-z', 'angle': 5.5}),
    (r'{\frz-5.5}', {'type': 'rotation-z', 'angle': -5.5}),
    (r'{\fr5.5}', {'type': 'rotation-z', 'angle': 5.5}),
    (r'{\fr-5.5}', {'type': 'rotation-z', 'angle': -5.5}),
    (r'{\org(1,2)}', {'type': 'rotation-origin', 'x': 1, 'y': 2}),
    (r'{\org(-1,-2)}', {'type': 'rotation-origin', 'x': -1, 'y': -2}),
    (r'{\fax-1.5}', {'type': 'shear-x', 'value': -1.5}),
    (r'{\fay-1.5}', {'type': 'shear-y', 'value': -1.5}),

    (r'{\c&H123456&}', {
        'type': 'color-primary',
        'red': 0x56,
        'green': 0x34,
        'blue': 0x12,
    }),
    (r'{\1c&H123456&}', {
        'type': 'color-primary',
        'red': 0x56,
        'green': 0x34,
        'blue': 0x12,
    }),
    (r'{\2c&H123456&}', {
        'type': 'color-secondary',
        'red': 0x56,
        'green': 0x34,
        'blue': 0x12,
    }),
    (r'{\3c&H123456&}', {
        'type': 'color-border',
        'red': 0x56,
        'green': 0x34,
        'blue': 0x12,
    }),
    (r'{\4c&H123456&}', {
        'type': 'color-shadow',
        'red': 0x56,
        'green': 0x34,
        'blue': 0x12,
    }),

    (r'{\alpha&H12&}', {'type': 'alpha-all', 'value': 0x12}),
    (r'{\1a&H12&}', {'type': 'alpha-primary', 'value': 0x12}),
    (r'{\2a&H12&}', {'type': 'alpha-secondary', 'value': 0x12}),
    (r'{\3a&H12&}', {'type': 'alpha-border', 'value': 0x12}),
    (r'{\4a&H12&}', {'type': 'alpha-shadow', 'value': 0x12}),

    (r'{\k50}', {'type': 'karaoke-1', 'duration': 500}),
    (r'{\K50}', {'type': 'karaoke-2', 'duration': 500}),
    (r'{\kf50}', {'type': 'karaoke-3', 'duration': 500}),
    (r'{\ko50}', {'type': 'karaoke-4', 'duration': 500}),

    (r'{\an5}', {'type': 'alignment', 'alignment': 5, 'legacy': False}),
    (r'{\a1}', {'type': 'alignment', 'alignment': 1, 'legacy': True}),
    (r'{\a2}', {'type': 'alignment', 'alignment': 2, 'legacy': True}),
    (r'{\a3}', {'type': 'alignment', 'alignment': 3, 'legacy': True}),
    (r'{\a5}', {'type': 'alignment', 'alignment': 4, 'legacy': True}),
    (r'{\a6}', {'type': 'alignment', 'alignment': 5, 'legacy': True}),
    (r'{\a7}', {'type': 'alignment', 'alignment': 6, 'legacy': True}),
    (r'{\a9}', {'type': 'alignment', 'alignment': 7, 'legacy': True}),
    (r'{\a10}', {'type': 'alignment', 'alignment': 8, 'legacy': True}),
    (r'{\a11}', {'type': 'alignment', 'alignment': 9, 'legacy': True}),
    (r'{\q0}', {'type': 'wrap-style', 'value': 0}),
    (r'{\q1}', {'type': 'wrap-style', 'value': 1}),
    (r'{\q2}', {'type': 'wrap-style', 'value': 2}),
    (r'{\q3}', {'type': 'wrap-style', 'value': 3}),
    (r'{\r}', {'type': 'reset-style', 'style': None}),
    (r'{\rSome style}', {'type': 'reset-style', 'style': 'Some style'}),

    (r'{\pos(1,2)}', {'type': 'position', 'x': 1, 'y': 2}),
    (r'{\move(1,2,3,4)}', {
        'type': 'movement',
        'x1': 1, 'y1': 2,
        'x2': 3, 'y2': 4,
        'start': None, 'end': None,
    }),
    (r'{\move(1,2,3,4,100,300)}', {
        'type': 'movement',
        'x1': 1, 'y1': 2,
        'x2': 3, 'y2': 4,
        'start': 100, 'end': 300,
    }),

    (r'{\fad(100,200)}', {'type': 'fade-simple', 'start': 100, 'end': 200}),
    (r'{\fade(1,2,3,4,5,6,7)}', {
        'type': 'fade-complex',
        'alpha1': 1,
        'alpha2': 2,
        'alpha3': 3,
        'time1': 4,
        'time2': 5,
        'time3': 6,
        'time4': 7,
    }),

    (r'{\t(50,100,1.2,\be5\fs40)}', {
        'type': 'animation', 'start': 50, 'end': 100, 'accel': 1.2,
        'children': [
            {'type': 'blur-edges', 'value': 5},
            {'type': 'font-size', 'size': 40},
        ],
    }),
    (r'{\t(1.2,\be5\fs40)}', {
        'type': 'animation', 'start': None, 'end': None, 'accel': 1.2,
        'children': [
            {'type': 'blur-edges', 'value': 5},
            {'type': 'font-size', 'size': 40},
        ],
    }),
    (r'{\t(50,100,\be5\fs40)}', {
        'type': 'animation', 'start': 50, 'end': 100, 'accel': None,
        'children': [
            {'type': 'blur-edges', 'value': 5},
            {'type': 'font-size', 'size': 40},
        ],
    }),
    (r'{\t(\be5\fs40)}', {
        'type': 'animation', 'start': None, 'end': None, 'accel': None,
        'children': [
            {'type': 'blur-edges', 'value': 5},
            {'type': 'font-size', 'size': 40},
        ],
    }),

    (r'{\clip(1,2,3,4)}', {
        'type': 'clip-rectangle',
        'x1': 1, 'y1': 2,
        'x2': 3, 'y2': 4,
        'inverse': False,
    }),
    (r'{\iclip(1,2,3,4)}', {
        'type': 'clip-rectangle',
        'x1': 1, 'y1': 2,
        'x2': 3, 'y2': 4,
        'inverse': True,
    }),

    (r'{\clip(1,m 50 0)}', {
        'type': 'clip-vector',
        'scale': 1,
        'inverse': False,
        'commands': 'm 50 0',
    }),
    (r'{\iclip(1,m 50 0)}', {
        'type': 'clip-vector',
        'scale': 1,
        'inverse': True,
        'commands': 'm 50 0',
    }),
    (r'{\clip(m 50 0)}', {
        'type': 'clip-vector',
        'scale': None,
        'inverse': False,
        'commands': 'm 50 0',
    }),
    (r'{\iclip(m 50 0)}', {
        'type': 'clip-vector',
        'scale': None,
        'inverse': True,
        'commands': 'm 50 0',
    }),
]

BAD_TEST_DATA = [
    r'{}',
    r'{',
    r'}',
    r'test{',
    r'test}',
    r'}test{',
    r'{{asd}',
    r'{asd}}',
    r'{{asd}}',

    r'{\i2}',
    r'{\b-1}',
    r'{\u2}',
    r'{\s2}',

    r'{\bord-4}',
    r'{\xbord-4}',
    r'{\ybord-4}',
    r'{\shad-4}',
    r'{\xshad-4}',
    r'{\yshad-4}',

    r'{\be-2}',
    r'{\blur-4}',

    r'{\fe-5}',
    r'{\fs-5}',
    r'{\fscx-5.5}',
    r'{\fscy-5.5}',

    r'{\org(-5.5,0)}',
    r'{\org-5.5,0}',

    r'{\c(123456)}',
    r'{\c&123456&}',
    r'{\5c&H123456&}',
    r'{\1c&H12356&}',
    r'{\1c&H1234567&}',
    r'{\1c&H12345G&}',

    r'{\a(12)}',
    r'{\a&12&}',
    r'{\5a&H12&}',
    r'{\1a&H1&}',
    r'{\1a&H123&}',
    r'{\1a&H1G&}',

    r'{\k-50}',
    r'{\K-50}',
    r'{\kf-50}',
    r'{\ko-50}',

    r'{\an10}',
    r'{\a4}',
    r'{\a8}',
    r'{\a12}',
    r'{\q5}',
]


@pytest.mark.parametrize('source_line,expected_tree', GOOD_TEST_DATA)
def test_parsing_valid_ass_line(source_line, expected_tree):
    assert expected_tree == ass_tag_parser.parse_ass(source_line)


@pytest.mark.parametrize('source_line,expected_tag', GOOD_TEST_DATA_SINGLE_TAG)
def test_parsing_valid_single_tag(source_line, expected_tag):
    expected_tree = [{'type': 'tags', 'children': [expected_tag]}]
    assert expected_tree == ass_tag_parser.parse_ass(source_line)


@pytest.mark.parametrize('source_line', BAD_TEST_DATA)
def test_parsing_invalid_ass_line(source_line):
    with pytest.raises(ass_tag_parser.ParsingError):
        ass_tag_parser.parse_ass(source_line)
