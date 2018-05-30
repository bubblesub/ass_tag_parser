import pytest
import ass_tag_parser


GOOD_TEST_DATA = \
    [
        ([], ''),

        (
            [
                {
                    'type': 'text',
                    'text': 'test',
                },
            ],
            r'test',
        ),

        (
            [
                {
                    'type': 'tags',
                    'children': [],
                },
            ],
            '{}',
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'comment',
                            'text': 'asdasd',
                        },
                    ],
                },
            ],
            r'{asdasd}',
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                        'type': 'drawing-mode',
                        'value': 2
                        }
                    ]
                },
                {
                    'type': 'text',
                    'text': 'm 3 4',
                },
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'drawing-mode',
                            'value': 0,
                        },
                    ]
                },
            ],
            r'{\p2}m 3 4{\p0}',
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False,
                        },
                        {
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False,
                        }
                    ],
                },
            ],
            r'{\an5\an5}',
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False
                        },
                    ]
                },
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False,
                        },
                    ]
                },
            ],
            r'{\an5}{\an5}',
        ),

        (
            [
                {
                    'type': 'text',
                    'text': 'abc def'
                },
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False
                        },
                    ]
                },
                {
                    'type': 'text',
                    'text': 'ghi jkl'
                },
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False
                        },
                    ]
                },
                {
                    'type': 'text',
                    'text': '123 456'
                },
            ],
            r'abc def{\an5}ghi jkl{\an5}123 456'
        ),

        (
            [
                {
                    'type': 'text',
                    'text': 'I am '
                },
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'bold',
                            'enabled': True
                        },
                    ]
                },
                {
                    'type': 'text',
                    'text': 'not'
                },
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'bold',
                            'enabled': False
                        },
                    ]
                },
                {
                    'type': 'text',
                    'text': ' amused.'
                },
            ],
            r'I am {\b1}not{\b0} amused.'
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'bold',
                            'weight': 100
                        },
                    ]},
                {
                    'type': 'text',
                    'text': 'How '
                },
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'bold',
                            'weight': 300
                        },
                    ]},
                {
                    'type': 'text',
                    'text': 'bold '
                },
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'bold',
                            'weight': 500
                        },
                    ]
                },
                {
                    'type': 'text',
                    'text': 'can '
                },
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'bold',
                            'weight': 700
                        },
                    ]
                },
                {
                    'type': 'text',
                    'text': 'you ',
                },
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'bold',
                            'weight': 900
                        },
                    ]
                },
                {
                    'type': 'text',
                    'text': 'get?',
                },
            ],
            r'{\b100}How {\b300}bold {\b500}can {\b700}you {\b900}get?',
        ),

        (
            [
                {
                    'type': 'text',
                    'text': '-Hey\\N',
                },
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'reset-style',
                            'style': 'Alternate',
                        },
                    ],
                },
                {
                    'type': 'text',
                    'text': '-Huh?\\N'
                },
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'reset-style',
                            'style': None,
                        },
                    ],
                },
                {
                    'type': 'text',
                    'text': '-Who are you?'
                },
            ],
            r'-Hey\N{\rAlternate}-Huh?\N{\r}-Who are you?'
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'color-primary',
                            'red': 0,
                            'green': 0,
                            'blue': 255
                        },
                        {
                            'type': 'animation',
                            'start': None,
                            'end': None,
                            'accel': None,
                            'children':
                            [
                                {
                                    'type': 'color-primary',
                                    'red': 255,
                                    'green': 0,
                                    'blue': 0,
                                },
                            ],
                        },
                    ]
                },
                {
                    'type': 'text',
                    'text': 'Hello!'
                },
            ],
            r'{\1c&HFF0000&\t(\1c&H0000FF&)}Hello!'
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False,
                        },
                        {
                            'type': 'animation',
                            'start': 0,
                            'end': 5000,
                            'accel': None,
                            'children':
                            [
                                {
                                    'type': 'rotation-z',
                                    'angle': 3600
                                }
                            ],
                        },
                    ]
                },
                {
                    'type': 'text',
                    'text': 'Wheee'
                },
            ],
            r'{\an5\t(0,5000,\frz3600)}Wheee'
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False,
                        },
                        {
                            'type': 'animation',
                            'start': 0,
                            'end': 5000,
                            'accel': 0.5,
                            'children':
                            [
                                {
                                    'type': 'rotation-z',
                                    'angle': 3600
                                },
                            ],
                        },
                    ],
                },
                {
                    'type': 'text',
                    'text': 'Wheee'
                },
            ],
            r'{\an5\t(0,5000,0.5,\frz3600)}Wheee'
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False,
                        },
                        {
                            'type': 'font-scale-x',
                            'scale': 0
                        },
                        {
                            'type': 'font-scale-y',
                            'scale': 0
                        },
                        {
                            'type': 'animation',
                            'start': 0,
                            'end': 500,
                            'accel': None,
                            'children':
                            [
                                {
                                    'type': 'font-scale-x',
                                    'scale': 100
                                },
                                {
                                    'type': 'font-scale-y',
                                    'scale': 100
                                },
                            ],
                        },
                    ]
                },
                {
                    'type': 'text',
                    'text': 'Boo!'
                },
            ],
            r'{\an5\fscx0\fscy0\t(0,500,\fscx100\fscy100)}Boo!'
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'comment',
                            'text': 'comment'
                        },
                        {
                            'type': 'bold',
                            'enabled': True
                        },
                    ]
                },
            ],
            r'{comment\b1}'
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'bold',
                            'enabled': True
                        },
                        {
                            'type': 'comment',
                            'text': 'comment'
                        },
                    ]
                },
            ],
            r'{\b1comment}'
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'alpha-secondary',
                            'value': 0xFF
                        },
                        {
                            'type': 'comment',
                            'text': 'comment'
                        },
                    ]
                },
            ],
            r'{\2a&HFF&comment}'
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'blur-edges',
                            'value': 2
                        },
                        {
                            'type': 'comment',
                            'text': '.2'
                        },
                    ]
                },
            ],
            r'{\be2.2}'
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'font-size',
                            'size': 5
                        },
                        {
                            'type': 'comment',
                            'text': '.4'
                        },
                    ]
                },
            ],
            r'{\fs5.4}'
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'karaoke-1',
                            'duration': 500
                        },
                        {
                            'type': 'comment',
                            'text': '.5'
                        },
                    ]
                },
            ],
            r'{\k50.5}'
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'karaoke-2',
                            'duration': 500
                        },
                        {
                            'type': 'comment',
                            'text': '.5'
                        },
                    ]
                },
            ],
            r'{\K50.5}'
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'karaoke-3',
                            'duration': 500
                        },
                        {
                            'type': 'comment',
                            'text': '.5'
                        },
                    ]
                },
            ],
            r'{\kf50.5}'
        ),

        (
            [
                {
                    'type': 'tags',
                    'children':
                    [
                        {
                            'type': 'karaoke-4',
                            'duration': 500
                        },
                        {
                            'type': 'comment',
                            'text': '.5'
                        },
                    ]
                },
            ],
            r'{\ko50.5}'
        ),
    ]

GOOD_TEST_DATA_SINGLE_TAG = \
    [
        (
            {'type': 'italics', 'enabled': True},
            r'{\i1}',
        ),

        (
            {'type': 'italics', 'enabled': False},
            r'{\i0}'
        ),

        (
            {'type': 'bold', 'weight': 300},
            r'{\b300}'
        ),

        (
            {'type': 'bold', 'enabled': True},
            r'{\b1}'
        ),

        (
            {'type': 'bold', 'enabled': False},
            r'{\b0}'
        ),

        (
            {'type': 'underline', 'enabled': True},
            r'{\u1}'
        ),

        (
            {'type': 'underline', 'enabled': False},
            r'{\u0}'
        ),

        (
            {'type': 'strikeout', 'enabled': True},
            r'{\s1}'
        ),

        (
            {'type': 'strikeout', 'enabled': False},
            r'{\s0}'
        ),

        (
            {'type': 'border', 'size': 0},
            r'{\bord0}'
        ),

        (
            {'type': 'border-x', 'size': 0},
            r'{\xbord0}'
        ),

        (
            {'type': 'border-y', 'size': 0},
            r'{\ybord0}'
        ),

        (
            {'type': 'border', 'size': 4.4},
            r'{\bord4.4}'
        ),

        (
            {'type': 'border-x', 'size': 4.4},
            r'{\xbord4.4}'
        ),

        (
            {'type': 'border-y', 'size': 4.4},
            r'{\ybord4.4}'
        ),

        (
            {'type': 'shadow', 'size': 0},
            r'{\shad0}'
        ),

        (
            {'type': 'shadow-x', 'size': 0},
            r'{\xshad0}'
        ),

        (
            {'type': 'shadow-y', 'size': 0},
            r'{\yshad0}'
        ),

        (
            {'type': 'shadow', 'size': 4.4},
            r'{\shad4.4}'
        ),

        (
            {'type': 'shadow-x', 'size': 4.4},
            r'{\xshad4.4}'
        ),

        (
            {'type': 'shadow-y', 'size': 4.4},
            r'{\yshad4.4}'
        ),

        (
            {'type': 'blur-edges', 'value': 2},
            r'{\be2}'
        ),

        (
            {'type': 'blur-edges-gauss', 'value': 4.4},
            r'{\blur4.4}'
        ),

        (
            {'type': 'font-name', 'name': 'Arial'},
            r'{\fn(Arial)}'
        ),

        (
            {'type': 'font-name', 'name': 'Comic Sans'},
            r'{\fn(Comic Sans)}'
        ),

        (
            {'type': 'font-name', 'name': 'Comic Sans'},
            r'{\fn(Comic Sans)}'
        ),

        (
            {'type': 'font-encoding', 'encoding': 5},
            r'{\fe5}'
        ),

        (
            {'type': 'font-size', 'size': 15},
            r'{\fs15}'
        ),

        (
            {'type': 'font-scale-x', 'scale': 5.5},
            r'{\fscx5.5}'
        ),

        (
            {'type': 'font-scale-y', 'scale': 5.5},
            r'{\fscy5.5}'
        ),

        (
            {'type': 'letter-spacing', 'value': 5.5},
            r'{\fsp5.5}'
        ),

        (
            {'type': 'letter-spacing', 'value': -5.5},
            r'{\fsp-5.5}'
        ),

        (
            {'type': 'rotation-x', 'angle': 5.5},
            r'{\frx5.5}'
        ),

        (
            {'type': 'rotation-x', 'angle': -5.5},
            r'{\frx-5.5}'
        ),

        (
            {'type': 'rotation-y', 'angle': 5.5},
            r'{\fry5.5}'
        ),

        (
            {'type': 'rotation-y', 'angle': -5.5},
            r'{\fry-5.5}'
        ),

        (
            {'type': 'rotation-z', 'angle': 5.5},
            r'{\frz5.5}'
        ),

        (
            {'type': 'rotation-z', 'angle': -5.5},
            r'{\frz-5.5}'
        ),

        (
            {'type': 'rotation-origin', 'x': 1, 'y': 2},
            r'{\org(1,2)}'
        ),

        (
            {'type': 'rotation-origin', 'x': -1, 'y': -2},
            r'{\org(-1,-2)}'
        ),

        (
            {'type': 'shear-x', 'value': -1.5},
            r'{\fax-1.5}'
        ),

        (
            {'type': 'shear-y', 'value': -1.5},
            r'{\fay-1.5}'
        ),

        (
            {
                'type': 'color-primary',
                'red': 0x56,
                'green': 0x34,
                'blue': 0x12,
            },
            r'{\1c&H123456&}',
        ),

        (
            {
                'type': 'color-secondary',
                'red': 0x56,
                'green': 0x34,
                'blue': 0x12,
            },
            r'{\2c&H123456&}',
        ),

        (
            {
                'type': 'color-border',
                'red': 0x56,
                'green': 0x34,
                'blue': 0x12,
            },
            r'{\3c&H123456&}'
        ),

        (
            {
                'type': 'color-shadow',
                'red': 0x56,
                'green': 0x34,
                'blue': 0x12,
            },
            r'{\4c&H123456&}'
        ),

        (
            {'type': 'alpha-all', 'value': 0x12},
            r'{\alpha&H12&}'
        ),

        (
            {'type': 'alpha-primary', 'value': 0x12},
            r'{\1a&H12&}'
        ),

        (
            {'type': 'alpha-secondary', 'value': 0x12},
            r'{\2a&H12&}'
        ),

        (
            {'type': 'alpha-border', 'value': 0x12},
            r'{\3a&H12&}'
        ),

        (
            {'type': 'alpha-shadow', 'value': 0x12},
            r'{\4a&H12&}'
        ),

        (
            {'type': 'karaoke-1', 'duration': 500},
            r'{\k50}'
        ),

        (
            {'type': 'karaoke-2', 'duration': 500},
            r'{\K50}'
        ),

        (
            {'type': 'karaoke-3', 'duration': 500},
            r'{\kf50}'
        ),

        (
            {'type': 'karaoke-4', 'duration': 500},
            r'{\ko50}'
        ),

        (
            {'type': 'alignment', 'alignment': 5, 'legacy': False},
            r'{\an5}'
        ),

        (
            {'type': 'alignment', 'alignment': 1, 'legacy': True},
            r'{\a1}'
        ),

        (
            {'type': 'alignment', 'alignment': 2, 'legacy': True},
            r'{\a2}'
        ),

        (
            {'type': 'alignment', 'alignment': 3, 'legacy': True},
            r'{\a3}'
        ),

        (
            {'type': 'alignment', 'alignment': 4, 'legacy': True},
            r'{\a5}'
        ),

        (
            {'type': 'alignment', 'alignment': 5, 'legacy': True},
            r'{\a6}'
        ),

        (
            {'type': 'alignment', 'alignment': 6, 'legacy': True},
            r'{\a7}'
        ),

        (
            {'type': 'alignment', 'alignment': 7, 'legacy': True},
            r'{\a9}'
        ),

        (
            {'type': 'alignment', 'alignment': 8, 'legacy': True},
            r'{\a10}'
        ),

        (
            {'type': 'alignment', 'alignment': 9, 'legacy': True},
            r'{\a11}'
        ),

        (
            {'type': 'wrap-style', 'value': 0},
            r'{\q0}'
        ),

        (
            {'type': 'wrap-style', 'value': 1},
            r'{\q1}'
        ),

        (
            {'type': 'wrap-style', 'value': 2},
            r'{\q2}'
        ),

        (
            {'type': 'wrap-style', 'value': 3},
            r'{\q3}'
        ),

        (
            {'type': 'reset-style', 'style': None},
            r'{\r}'
        ),

        (
            {'type': 'reset-style', 'style': 'Some style'},
            r'{\rSome style}'
        ),

        (
            {'type': 'position', 'x': 1, 'y': 2},
            r'{\pos(1,2)}'
        ),

        (
            {
                'type': 'movement',
                'x1': 1, 'y1': 2,
                'x2': 3, 'y2': 4,
                'start': None, 'end': None,
            },
            r'{\move(1,2,3,4)}',
        ),

        (
            {
                'type': 'movement',
                'x1': 1, 'y1': 2,
                'x2': 3, 'y2': 4,
                'start': 100, 'end': 300,
            },
            r'{\move(1,2,3,4,100,300)}',
        ),

        (
            {'type': 'fade-simple', 'start': 100, 'end': 200},
            r'{\fad(100,200)}',
        ),

        (
            {
                'type': 'fade-complex',
                'alpha1': 1,
                'alpha2': 2,
                'alpha3': 3,
                'time1': 4,
                'time2': 5,
                'time3': 6,
                'time4': 7,
            },
            r'{\fade(1,2,3,4,5,6,7)}',
        ),

        (
            {
                'type': 'animation',
                'start': 50,
                'end': 100,
                'accel': 1.2,
                'children':
                [
                    {
                        'type': 'blur-edges',
                        'value': 5,
                    },
                    {
                        'type': 'font-size',
                        'size': 40,
                    },
                ],
            },
            r'{\t(50,100,1.2,\be5\fs40)}',
        ),

        (
            {
                'type': 'animation',
                'start': None,
                'end': None,
                'accel': 1.2,
                'children':
                [
                    {
                        'type': 'blur-edges',
                        'value': 5
                    },
                    {
                        'type': 'font-size',
                        'size': 40
                    },
                ],
            },
            r'{\t(1.2,\be5\fs40)}',
        ),

        (
            {
                'type': 'animation',
                'start': 50,
                'end': 100,
                'accel': None,
                'children':
                [
                    {
                        'type': 'blur-edges',
                        'value': 5
                    },
                    {
                        'type': 'font-size',
                        'size': 40
                    },
                ],
            },
            r'{\t(50,100,\be5\fs40)}'
        ),

        (
            {
                'type': 'animation',
                'start': None,
                'end': None,
                'accel': None,
                'children':
                [
                    {
                        'type': 'blur-edges',
                        'value': 5
                    },
                    {
                        'type': 'font-size',
                        'size': 40
                    },
                ],
            },
            r'{\t(\be5\fs40)}'
        ),

        (
            {
                'type': 'clip-rectangle',
                'x1': 1, 'y1': 2,
                'x2': 3, 'y2': 4,
                'inverse': False,
            },
            r'{\clip(1,2,3,4)}'
        ),

        (
            {
                'type': 'clip-rectangle',
                'x1': 1, 'y1': 2,
                'x2': 3, 'y2': 4,
                'inverse': True,
            },
            r'{\iclip(1,2,3,4)}',
        ),

        (
            {
                'type': 'clip-vector',
                'scale': 1,
                'inverse': False,
                'commands': 'm 50 0',
            },
            r'{\clip(1,m 50 0)}',
        ),

        (
            {
                'type': 'clip-vector',
                'scale': 1,
                'inverse': True,
                'commands': 'm 50 0',
            },
            r'{\iclip(1,m 50 0)}',
        ),

        (
            {
                'type': 'clip-vector',
                'scale': None,
                'inverse': False,
                'commands': 'm 50 0',
            },
            r'{\clip(m 50 0)}',
        ),

        (
            {
                'type': 'clip-vector',
                'scale': None,
                'inverse': True,
                'commands': 'm 50 0',
            },
            r'{\iclip(m 50 0)}'
        ),
    ]

BAD_TEST_DATA = [
    [{'type': 'derp'}],
    [{'type': 'tags'}],
    [{'type': 'tags', 'children': 0}],
    [{'type': 'tags', 'children': [{}]}],
    [{'type': 'tags', 'children': [{'type': 'derp'}]}],
]


@pytest.mark.parametrize('source_tree,expected_line', GOOD_TEST_DATA)
def test_parsing_valid_ass_line(source_tree, expected_line):
    assert expected_line == ass_tag_parser.serialize_ass(source_tree)


@pytest.mark.parametrize('source_tag,expected_line', GOOD_TEST_DATA_SINGLE_TAG)
def test_parsing_valid_single_tag(source_tag, expected_line):
    source_tree = [{'type': 'tags', 'children': [source_tag]}]
    assert expected_line == ass_tag_parser.serialize_ass(source_tree)


@pytest.mark.parametrize('source_tree', BAD_TEST_DATA)
def test_parsing_invalid_ass_line(source_tree):
    with pytest.raises(ass_tag_parser.ParsingError):
        ass_tag_parser.serialize_ass(source_tree)
