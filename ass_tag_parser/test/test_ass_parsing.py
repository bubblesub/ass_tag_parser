import pytest
import ass_tag_parser


GOOD_TEST_DATA = \
    [
        (
            r'test',
            [
                {
                    'pos': (0, 4),
                    'type': 'text',
                    'text': 'test',
                },
            ],
        ),

        (
            '',
            [],
        ),

        (
            '{}',
            [
                {
                    'pos': (0, 2),
                    'type': 'tags',
                    'children': [],
                },
            ],
        ),

        (
            r'{asdasd}',
            [
                {
                    'pos': (0, 8),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 7),
                            'type': 'comment',
                            'text': 'asdasd',
                        },
                    ],
                },
            ],
        ),

        (
            r'{asd\\asd}',
            [
                {
                    'pos': (0, 10),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 9),
                            'type': 'comment',
                            'text': r'asd\\asd',
                        },
                    ],
                },
            ],
        ),

        (
            r'{asd\Nasd}',
            [
                {
                    'pos': (0, 10),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 9),
                            'type': 'comment',
                            'text': r'asd\Nasd',
                        },
                    ],
                },
            ],
        ),

        (
            r'{asd\Nasd\nasd\hasd}',
            [
                {
                    'pos': (0, 20),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 19),
                            'type': 'comment',
                            'text': r'asd\Nasd\nasd\hasd',
                        },
                    ],
                },
            ],
        ),

        (
            r'{\p2}m 3 4{\p0}',
            [
                {
                    'pos': (0, 5),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 4),
                            'type': 'drawing-mode',
                            'value': 2,
                        },
                    ],
                },
                {
                    'pos': (5, 10),
                    'type': 'text',
                    'text': 'm 3 4',
                },
                {
                    'pos': (10, 15),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (11, 14),
                            'type': 'drawing-mode',
                            'value': 0,
                        },
                    ],
                },
            ],
        ),

        (
            r'{\an5\an5}',
            [
                {
                    'pos': (0, 10),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 5),
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False,
                        },
                        {
                            'pos': (5, 9),
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False,
                        },
                    ],
                },
            ],
        ),

        (
            r'{\an5}{\an5}',
            [
                {
                    'pos': (0, 6),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 5),
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False,
                        },
                    ],
                },
                {
                    'pos': (6, 12),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (7, 11),
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False,
                        },
                    ],
                },
            ],
        ),

        (
            r'abc def{\an5}ghi jkl{\an5}123 456',
            [
                {
                    'pos': (0, 7),
                    'type': 'text',
                    'text': 'abc def',
                },
                {
                    'pos': (7, 13),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (8, 12),
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False,
                        },
                    ],
                },
                {
                    'pos': (13, 20),
                    'type': 'text',
                    'text': 'ghi jkl',
                },
                {
                    'pos': (20, 26),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (21, 25),
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False,
                        },
                    ],
                },
                {
                    'pos': (26, 33),
                    'type': 'text',
                    'text': '123 456',
                },
            ],
        ),

        (
            r'I am {\b1}not{\b0} amused.',
            [
                {
                    'pos': (0, 5),
                    'type': 'text',
                    'text': 'I am ',
                },
                {
                    'pos': (5, 10),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (6, 9),
                            'type': 'bold',
                            'enabled': True
                        },
                    ],
                },
                {
                    'pos': (10, 13),
                    'type': 'text',
                    'text': 'not',
                },
                {
                    'pos': (13, 18),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (14, 17),
                            'type': 'bold',
                            'enabled': False
                        },
                    ],
                },
                {
                    'pos': (18, 26),
                    'type': 'text',
                    'text': ' amused.',
                },
            ],
        ),

        (
            r'{\b100}How {\b300}bold {\b500}can {\b700}you {\b900}get?',
            [
                {
                    'pos': (0, 7),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 6),
                            'type': 'bold',
                            'weight': 100
                        },
                    ],
                },
                {
                    'pos': (7, 11),
                    'type': 'text',
                    'text': 'How ',
                },
                {
                    'pos': (11, 18),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (12, 17),
                            'type': 'bold',
                            'weight': 300
                        },
                    ],
                },
                {
                    'pos': (18, 23),
                    'type': 'text',
                    'text': 'bold ',
                },
                {
                    'pos': (23, 30),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (24, 29),
                            'type': 'bold',
                            'weight': 500
                        },
                    ],
                },
                {
                    'pos': (30, 34),
                    'type': 'text',
                    'text': 'can ',
                },
                {
                    'pos': (34, 41),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (35, 40),
                            'type': 'bold',
                            'weight': 700
                        },
                    ],
                },
                {
                    'pos': (41, 45),
                    'type': 'text',
                    'text': 'you ',
                },
                {
                    'pos': (45, 52),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (46, 51),
                            'type': 'bold',
                            'weight': 900
                        },
                    ],
                },
                {
                    'pos': (52, 56),
                    'type': 'text',
                    'text': 'get?',
                },
            ],
        ),

        (
            r'-Hey\N{\rAlternate}-Huh?\N{\r}-Who are you?',
            [
                {
                    'pos': (0, 6),
                    'type': 'text',
                    'text': '-Hey\\N',
                },
                {
                    'pos': (6, 19),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (7, 18),
                            'type': 'reset-style',
                            'style': 'Alternate',
                        },
                    ],
                },
                {
                    'pos': (19, 26),
                    'type': 'text',
                    'text': '-Huh?\\N',
                },
                {
                    'pos': (26, 30),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (27, 29),
                            'type': 'reset-style',
                            'style': None
                        },
                    ],
                },
                {
                    'pos': (30, 43),
                    'type': 'text',
                    'text': '-Who are you?',
                },
            ],
        ),

        (
            r'{\1c&HFF0000&\t(\1c&H0000FF&)}Hello!',
            [
                {
                    'pos': (0, 30),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 13),
                            'type': 'color-primary',
                            'red': 0,
                            'green': 0,
                            'blue': 255,
                        },
                        {
                            'pos': (13, 29),
                            'type': 'animation',
                            'start': None,
                            'end': None,
                            'accel': None,
                            'children':
                            [
                                {
                                    'pos': (16, 28),
                                    'type': 'color-primary',
                                    'red': 255,
                                    'green': 0,
                                    'blue': 0,
                                },
                            ],
                        },
                    ],
                },
                {
                    'pos': (30, 36),
                    'type': 'text',
                    'text': 'Hello!',
                },
            ],
        ),

        (
            r'{\an5\t(0,5000,\frz3600)}Wheee',
            [
                {
                    'pos': (0, 25),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 5),
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False,
                        },
                        {
                            'pos': (5, 24),
                            'type': 'animation',
                            'start': 0,
                            'end': 5000,
                            'accel': None,
                            'children':
                            [
                                {
                                    'pos': (15, 23),
                                    'type': 'rotation-z',
                                    'angle': 3600,
                                },
                            ],
                        },
                    ],
                },
                {
                    'pos': (25, 30),
                    'type': 'text',
                    'text': 'Wheee',
                },
            ],
        ),

        (
            r'{\an5\t(0,5000,0.5,\frz3600)}Wheee',
            [
                {
                    'pos': (0, 29),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 5),
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False,
                        },
                        {
                            'pos': (5, 28),
                            'type': 'animation',
                            'start': 0,
                            'end': 5000,
                            'accel': 0.5,
                            'children':
                            [
                                {
                                    'pos': (19, 27),
                                    'type': 'rotation-z',
                                    'angle': 3600,
                                },
                            ],
                        },
                    ],
                },
                {
                    'pos': (29, 34),
                    'type': 'text',
                    'text': 'Wheee',
                },
            ],
        ),

        (
            r'{\an5\fscx0\fscy0\t(0,500,\fscx100\fscy100)}Boo!',
            [
                {
                    'pos': (0, 44),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 5),
                            'type': 'alignment',
                            'alignment': 5,
                            'legacy': False,
                        },
                        {
                            'pos': (5, 11),
                            'type': 'font-scale-x',
                            'scale': 0,
                        },
                        {
                            'pos': (11, 17),
                            'type': 'font-scale-y',
                            'scale': 0,
                        },
                        {
                            'pos': (17, 43),
                            'type': 'animation',
                            'start': 0,
                            'end': 500,
                            'accel': None,
                            'children':
                            [
                                {
                                    'pos': (26, 34),
                                    'type': 'font-scale-x',
                                    'scale': 100,
                                },
                                {
                                    'pos': (34, 42),
                                    'type': 'font-scale-y',
                                    'scale': 100,
                                },
                            ],
                        },
                    ],
                },
                {
                    'pos': (44, 48),
                    'type': 'text',
                    'text': 'Boo!',
                },
            ],
        ),

        (
            r'{comment\b1}',
            [
                {
                    'pos': (0, 12),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 8),
                            'type': 'comment',
                            'text': 'comment',
                        },
                        {
                            'pos': (8, 11),
                            'type': 'bold',
                            'enabled': True,
                        },
                    ],
                },
            ],
        ),

        (
            r'{\b1comment}',
            [
                {
                    'pos': (0, 12),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 4),
                            'type': 'bold',
                            'enabled': True,
                        },
                        {
                            'pos': (4, 11),
                            'type': 'comment',
                            'text': 'comment',
                        },
                    ],
                },
            ],
        ),

        (
            r'{\2a&HFF&comment}',
            [
                {
                    'pos': (0, 17),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 9),
                            'type': 'alpha-secondary',
                            'value': 0xFF,
                        },
                        {
                            'pos': (9, 16),
                            'type': 'comment',
                            'text': 'comment',
                        },
                    ],
                },
            ],
        ),

        (
            r'{\be2.2}',
            [
                {
                    'pos': (0, 8),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 5),
                            'type': 'blur-edges',
                            'value': 2
                        },
                        {
                            'pos': (5, 7),
                            'type': 'comment',
                            'text': '.2',
                        },
                    ],
                },
            ],
        ),

        (
            r'{\fs5.4}',
            [
                {
                    'pos': (0, 8),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 5),
                            'type': 'font-size',
                            'size': 5
                        },
                        {
                            'pos': (5, 7),
                            'type': 'comment',
                            'text': '.4',
                        },
                    ],
                },
            ],
        ),

        (
            r'{\k50.5}',
            [
                {
                    'pos': (0, 8),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 5),
                            'type': 'karaoke-1',
                            'duration': 500
                        },
                        {
                            'pos': (5, 7),
                            'type': 'comment',
                            'text': '.5',
                        },
                    ],
                },
            ],
        ),

        (
            r'{\K50.5}',
            [
                {
                    'pos': (0, 8),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 5),
                            'type': 'karaoke-2',
                            'duration': 500
                        },
                        {
                            'pos': (5, 7),
                            'type': 'comment',
                            'text': '.5',
                        },
                    ],
                },
            ],
        ),

        (
            r'{\kf50.5}',
            [
                {
                    'pos': (0, 9),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 6),
                            'type': 'karaoke-3',
                            'duration': 500
                        },
                        {
                            'pos': (6, 8),
                            'type': 'comment',
                            'text': '.5',
                        },
                    ],
                },
            ],
        ),

        (
            r'{\ko50.5}',
            [
                {
                    'pos': (0, 9),
                    'type': 'tags',
                    'children':
                    [
                        {
                            'pos': (1, 6),
                            'type': 'karaoke-4',
                            'duration': 500
                        },
                        {
                            'pos': (6, 8),
                            'type': 'comment',
                            'text': '.5',
                        },
                    ],
                },
            ],
        ),
    ]

GOOD_TEST_DATA_SINGLE_TAG = \
    [
        (
            r'{\i1}',
            {'pos': (1, 4), 'type': 'italics', 'enabled': True}
        ),

        (
            r'{\i0}',
            {'pos': (1, 4), 'type': 'italics', 'enabled': False}
        ),

        (
            r'{\b300}',
            {'pos': (1, 6), 'type': 'bold', 'weight': 300}
        ),

        (
            r'{\b1}',
            {'pos': (1, 4), 'type': 'bold', 'enabled': True}
        ),

        (
            r'{\b0}',
            {'pos': (1, 4), 'type': 'bold', 'enabled': False}
        ),

        (
            r'{\u1}',
            {'pos': (1, 4), 'type': 'underline', 'enabled': True}
        ),

        (
            r'{\u0}',
            {'pos': (1, 4), 'type': 'underline', 'enabled': False}
        ),

        (
            r'{\s1}',
            {'pos': (1, 4), 'type': 'strikeout', 'enabled': True}
        ),

        (
            r'{\s0}',
            {'pos': (1, 4), 'type': 'strikeout', 'enabled': False}
        ),

        (
            r'{\bord0}',
            {'pos': (1, 7), 'type': 'border', 'size': 0}
        ),

        (
            r'{\xbord0}',
            {'pos': (1, 8), 'type': 'border-x', 'size': 0}
        ),

        (
            r'{\ybord0}',
            {'pos': (1, 8), 'type': 'border-y', 'size': 0}
        ),

        (
            r'{\bord4.4}',
            {'pos': (1, 9), 'type': 'border', 'size': 4.4}
        ),

        (
            r'{\xbord4.4}',
            {'pos': (1, 10), 'type': 'border-x', 'size': 4.4}
        ),

        (
            r'{\ybord4.4}',
            {'pos': (1, 10), 'type': 'border-y', 'size': 4.4}
        ),

        (
            r'{\shad0}',
            {'pos': (1, 7), 'type': 'shadow', 'size': 0}
        ),

        (
            r'{\xshad0}',
            {'pos': (1, 8), 'type': 'shadow-x', 'size': 0}
        ),

        (
            r'{\yshad0}',
            {'pos': (1, 8), 'type': 'shadow-y', 'size': 0}
        ),

        (
            r'{\shad4.4}',
            {'pos': (1, 9), 'type': 'shadow', 'size': 4.4}
        ),

        (
            r'{\xshad4.4}',
            {'pos': (1, 10), 'type': 'shadow-x', 'size': 4.4}
        ),

        (
            r'{\yshad4.4}',
            {'pos': (1, 10), 'type': 'shadow-y', 'size': 4.4}
        ),

        (
            r'{\be2}',
            {'pos': (1, 5), 'type': 'blur-edges', 'value': 2}
        ),

        (
            r'{\blur4.4}',
            {'pos': (1, 9), 'type': 'blur-edges-gauss', 'value': 4.4}
        ),

        (
            r'{\fnArial}',
            {'pos': (1, 9), 'type': 'font-name', 'name': 'Arial'}
        ),

        (
            r'{\fnComic Sans}',
            {'pos': (1, 14), 'type': 'font-name', 'name': 'Comic Sans'}
        ),

        (
            r'{\fn(Comic Sans)}',
            {'pos': (1, 16), 'type': 'font-name', 'name': 'Comic Sans'}
        ),

        (
            r'{\fe5}',
            {'pos': (1, 5), 'type': 'font-encoding', 'encoding': 5}
        ),

        (
            r'{\fs15}',
            {'pos': (1, 6), 'type': 'font-size', 'size': 15}
        ),

        (
            r'{\fscx5.5}',
            {'pos': (1, 9), 'type': 'font-scale-x', 'scale': 5.5}
        ),

        (
            r'{\fscy5.5}',
            {'pos': (1, 9), 'type': 'font-scale-y', 'scale': 5.5}
        ),

        (
            r'{\fsp5.5}',
            {'pos': (1, 8), 'type': 'letter-spacing', 'value': 5.5}
        ),

        (
            r'{\fsp-5.5}',
            {'pos': (1, 9), 'type': 'letter-spacing', 'value': -5.5}
        ),

        (
            r'{\frx5.5}',
            {'pos': (1, 8), 'type': 'rotation-x', 'angle': 5.5}
        ),

        (
            r'{\frx-5.5}',
            {'pos': (1, 9), 'type': 'rotation-x', 'angle': -5.5}
        ),

        (
            r'{\fry5.5}',
            {'pos': (1, 8), 'type': 'rotation-y', 'angle': 5.5}
        ),

        (
            r'{\fry-5.5}',
            {'pos': (1, 9), 'type': 'rotation-y', 'angle': -5.5}
        ),

        (
            r'{\frz5.5}',
            {'pos': (1, 8), 'type': 'rotation-z', 'angle': 5.5}
        ),

        (
            r'{\frz-5.5}',
            {'pos': (1, 9), 'type': 'rotation-z', 'angle': -5.5}
        ),

        (
            r'{\fr5.5}',
            {'pos': (1, 7), 'type': 'rotation-z', 'angle': 5.5}
        ),

        (
            r'{\fr-5.5}',
            {'pos': (1, 8), 'type': 'rotation-z', 'angle': -5.5}
        ),

        (
            r'{\org(1,2)}',
            {'pos': (1, 10), 'type': 'rotation-origin', 'x': 1, 'y': 2}
        ),

        (
            r'{\org(-1,-2)}',
            {'pos': (1, 12), 'type': 'rotation-origin', 'x': -1, 'y': -2}
        ),

        (
            r'{\fax-1.5}',
            {'pos': (1, 9), 'type': 'shear-x', 'value': -1.5}
        ),

        (
            r'{\fay-1.5}',
            {'pos': (1, 9), 'type': 'shear-y', 'value': -1.5}
        ),

        (
            r'{\c&H123456&}',
            {
                'pos': (1, 12),
                'type': 'color-primary',
                'red': 0x56,
                'green': 0x34,
                'blue': 0x12,
            }
        ),

        (
            r'{\1c&H123456&}',
            {
                'pos': (1, 13),
                'type': 'color-primary',
                'red': 0x56,
                'green': 0x34,
                'blue': 0x12,
            }
        ),

        (
            r'{\2c&H123456&}',
            {
                'pos': (1, 13),
                'type': 'color-secondary',
                'red': 0x56,
                'green': 0x34,
                'blue': 0x12,
            }
        ),

        (
            r'{\3c&H123456&}',
            {
                'pos': (1, 13),
                'type': 'color-border',
                'red': 0x56,
                'green': 0x34,
                'blue': 0x12,
            }
        ),

        (
            r'{\4c&H123456&}',
            {
                'pos': (1, 13),
                'type': 'color-shadow',
                'red': 0x56,
                'green': 0x34,
                'blue': 0x12,
            }
        ),

        (
            r'{\alpha&H12&}',
            {'pos': (1, 12), 'type': 'alpha-all', 'value': 0x12}
        ),

        (
            r'{\1a&H12&}',
            {'pos': (1, 9), 'type': 'alpha-primary', 'value': 0x12}
        ),

        (
            r'{\2a&H12&}',
            {'pos': (1, 9), 'type': 'alpha-secondary', 'value': 0x12}
        ),

        (
            r'{\3a&H12&}',
            {'pos': (1, 9), 'type': 'alpha-border', 'value': 0x12}
        ),

        (
            r'{\4a&H12&}',
            {'pos': (1, 9), 'type': 'alpha-shadow', 'value': 0x12}
        ),

        (
            r'{\k50}',
            {'pos': (1, 5), 'type': 'karaoke-1', 'duration': 500}
        ),

        (
            r'{\K50}',
            {'pos': (1, 5), 'type': 'karaoke-2', 'duration': 500}
        ),

        (
            r'{\kf50}',
            {'pos': (1, 6), 'type': 'karaoke-3', 'duration': 500}
        ),

        (
            r'{\ko50}',
            {'pos': (1, 6), 'type': 'karaoke-4', 'duration': 500}
        ),

        (
            r'{\an5}',
            {
                'pos': (1, 5),
                'type': 'alignment',
                'alignment': 5,
                'legacy': False,
            }
        ),

        (
            r'{\a1}',
            {
                'pos': (1, 4),
                'type': 'alignment',
                'alignment': 1,
                'legacy': True,
            }
        ),

        (
            r'{\a2}',
            {
                'pos': (1, 4),
                'type': 'alignment',
                'alignment': 2,
                'legacy': True,
            }
        ),

        (
            r'{\a3}',
            {
                'pos': (1, 4),
                'type': 'alignment',
                'alignment': 3,
                'legacy': True,
            }
        ),

        (
            r'{\a5}',
            {
                'pos': (1, 4),
                'type': 'alignment',
                'alignment': 4,
                'legacy': True,
            }
        ),

        (
            r'{\a6}',
            {
                'pos': (1, 4),
                'type': 'alignment',
                'alignment': 5,
                'legacy': True,
            }
        ),

        (
            r'{\a7}',
            {
                'pos': (1, 4),
                'type': 'alignment',
                'alignment': 6,
                'legacy': True,
            }
        ),

        (
            r'{\a9}',
            {
                'pos': (1, 4),
                'type': 'alignment',
                'alignment': 7,
                'legacy': True,
            }
        ),

        (
            r'{\a10}',
            {
                'pos': (1, 5),
                'type': 'alignment',
                'alignment': 8,
                'legacy': True,
            }
        ),

        (
            r'{\a11}',
            {
                'pos': (1, 5),
                'type': 'alignment',
                'alignment': 9,
                'legacy': True,
            }
        ),

        (
            r'{\q0}',
            {'pos': (1, 4), 'type': 'wrap-style', 'value': 0}
        ),

        (
            r'{\q1}',
            {'pos': (1, 4), 'type': 'wrap-style', 'value': 1}
        ),

        (
            r'{\q2}',
            {'pos': (1, 4), 'type': 'wrap-style', 'value': 2}
        ),

        (
            r'{\q3}',
            {'pos': (1, 4), 'type': 'wrap-style', 'value': 3}
        ),

        (
            r'{\r}',
            {'pos': (1, 3), 'type': 'reset-style', 'style': None}
        ),

        (
            r'{\rSome style}',
            {'pos': (1, 13), 'type': 'reset-style', 'style': 'Some style'}
        ),

        (
            r'{\pos(1,2)}',
            {'pos': (1, 10), 'type': 'position', 'x': 1, 'y': 2}
        ),

        (
            r'{\move(1,2,3,4)}',
            {
                'pos': (1, 15),
                'type': 'movement',
                'x1': 1, 'y1': 2,
                'x2': 3, 'y2': 4,
                'start': None, 'end': None,
            }
        ),

        (
            r'{\move(1,2,3,4,100,300)}',
            {
                'pos': (1, 23),
                'type': 'movement',
                'x1': 1, 'y1': 2,
                'x2': 3, 'y2': 4,
                'start': 100, 'end': 300,
            }
        ),

        (
            r'{\fad(100,200)}',
            {
                'pos': (1, 14),
                'type': 'fade-simple',
                'start': 100,
                'end': 200,
            }
        ),

        (
            r'{\fade(1,2,3,4,5,6,7)}',
            {
                'pos': (1, 21),
                'type': 'fade-complex',
                'alpha1': 1,
                'alpha2': 2,
                'alpha3': 3,
                'time1': 4,
                'time2': 5,
                'time3': 6,
                'time4': 7,
            }
        ),

        (
            r'{\t(50,100,1.2,\be5\fs40)}',
            {
                'pos': (1, 25),
                'type': 'animation',
                'start': 50,
                'end': 100,
                'accel': 1.2,
                'children':
                [
                    {
                        'pos': (15, 19),
                        'type': 'blur-edges',
                        'value': 5,
                    },
                    {
                        'pos': (19, 24),
                        'type': 'font-size',
                        'size': 40,
                    },
                ],
            }
        ),

        (
            r'{\t(1.2,\be5\fs40)}',
            {
                'pos': (1, 18),
                'type': 'animation',
                'start': None,
                'end': None,
                'accel': 1.2,
                'children':
                [
                    {
                        'pos': (8, 12),
                        'type': 'blur-edges',
                        'value': 5,
                    },
                    {
                        'pos': (12, 17),
                        'type': 'font-size',
                        'size': 40,
                    },
                ],
            }
        ),

        (
            r'{\t(50,100,\be5\fs40)}',
            {
                'pos': (1, 21),
                'type': 'animation',
                'start': 50,
                'end': 100,
                'accel': None,
                'children':
                [
                    {
                        'pos': (11, 15),
                        'type': 'blur-edges',
                        'value': 5,
                    },
                    {
                        'pos': (15, 20),
                        'type': 'font-size',
                        'size': 40,
                    },
                ],
            }
        ),

        (
            r'{\t(\be5\fs40)}',
            {
                'pos': (1, 14),
                'type': 'animation',
                'start': None,
                'end': None,
                'accel': None,
                'children':
                [
                    {
                        'pos': (4, 8),
                        'type': 'blur-edges',
                        'value': 5,
                    },
                    {
                        'pos': (8, 13),
                        'type': 'font-size',
                        'size': 40,
                    },
                ],
            }
        ),

        (
            r'{\clip(1,2,3,4)}',
            {
                'pos': (1, 15),
                'type': 'clip-rectangle',
                'x1': 1, 'y1': 2,
                'x2': 3, 'y2': 4,
                'inverse': False,
            }
        ),

        (
            r'{\iclip(1,2,3,4)}',
            {
                'pos': (1, 16),
                'type': 'clip-rectangle',
                'x1': 1, 'y1': 2,
                'x2': 3, 'y2': 4,
                'inverse': True,
            }
        ),

        (
            r'{\clip(1,m 50 0)}',
            {
                'pos': (1, 16),
                'type': 'clip-vector',
                'scale': 1,
                'inverse': False,
                'commands': 'm 50 0',
            }
        ),

        (
            r'{\iclip(1,m 50 0)}',
            {
                'pos': (1, 17),
                'type': 'clip-vector',
                'scale': 1,
                'inverse': True,
                'commands': 'm 50 0',
            }
        ),

        (
            r'{\clip(m 50 0)}',
            {
                'pos': (1, 14),
                'type': 'clip-vector',
                'scale': None,
                'inverse': False,
                'commands': 'm 50 0',
            }
        ),

        (
            r'{\iclip(m 50 0)}',
            {
                'pos': (1, 15),
                'type': 'clip-vector',
                'scale': None,
                'inverse': True,
                'commands': 'm 50 0',
            }
        ),
    ]

BAD_TEST_DATA = \
    [
        r'{',
        r'}',
        r'test{',
        r'test}',
        r'}test{',
        r'{{asd}',
        r'{asd}}',
        r'{{asd}}',

        r'{\junk}',
        r'{\garbage}',
        r'{\trash}',

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
    expected_tree = \
        [
            {
                'pos': (0, len(source_line)),
                'type': 'tags',
                'children':
                [
                    expected_tag
                ],
            }
        ]
    assert expected_tree == ass_tag_parser.parse_ass(source_line)


@pytest.mark.parametrize('source_line', BAD_TEST_DATA)
def test_parsing_invalid_ass_line(source_line):
    with pytest.raises(ass_tag_parser.ParsingError):
        ass_tag_parser.parse_ass(source_line)
