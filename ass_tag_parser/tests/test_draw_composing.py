import pytest

from ass_tag_parser import (
    AssDrawCmd,
    AssDrawCmdBezier,
    AssDrawCmdCloseSpline,
    AssDrawCmdExtendSpline,
    AssDrawCmdLine,
    AssDrawCmdMove,
    AssDrawCmdSpline,
    AssDrawPoint,
    compose_draw_commands,
)


@pytest.mark.parametrize(
    "source,expected",
    [
        ([AssDrawCmdMove(AssDrawPoint(0, 0), close=True)], "m 0 0"),
        ([AssDrawCmdMove(AssDrawPoint(1, 2), close=False)], "n 1 2"),
        ([AssDrawCmdMove(AssDrawPoint(-1, 2), close=True)], "m -1 2"),
        ([AssDrawCmdMove(AssDrawPoint(1.0, 2.0), close=True)], "m 1 2"),
        ([AssDrawCmdMove(AssDrawPoint(1.1, 2.2), close=True)], "m 1.1 2.2"),
        ([AssDrawCmdLine([AssDrawPoint(1, 2)])], "l 1 2"),
        ([AssDrawCmdLine([AssDrawPoint(1.0, 2.0)])], "l 1 2"),
        ([AssDrawCmdLine([AssDrawPoint(1.1, 2.2)])], "l 1.1 2.2"),
        (
            [AssDrawCmdLine([AssDrawPoint(1, 2), AssDrawPoint(3, 4)])],
            "l 1 2 3 4",
        ),
        (
            [AssDrawCmdLine([AssDrawPoint(1.0, 2.0), AssDrawPoint(3.0, 4.0)])],
            "l 1 2 3 4",
        ),
        (
            [AssDrawCmdLine([AssDrawPoint(1.1, 2.2), AssDrawPoint(3.3, 4.4)])],
            "l 1.1 2.2 3.3 4.4",
        ),
        (
            [
                AssDrawCmdBezier(
                    (
                        AssDrawPoint(1, 2),
                        AssDrawPoint(3, 4),
                        AssDrawPoint(5, 6),
                    )
                )
            ],
            "b 1 2 3 4 5 6",
        ),
        (
            [
                AssDrawCmdSpline(
                    [
                        AssDrawPoint(1, 2),
                        AssDrawPoint(3, 4),
                        AssDrawPoint(5, 6),
                    ]
                )
            ],
            "s 1 2 3 4 5 6",
        ),
        (
            [
                AssDrawCmdSpline(
                    [
                        AssDrawPoint(1, 2),
                        AssDrawPoint(3, 4),
                        AssDrawPoint(5, 6),
                        AssDrawPoint(7, 8),
                        AssDrawPoint(9, 10),
                    ]
                )
            ],
            "s 1 2 3 4 5 6 7 8 9 10",
        ),
        ([AssDrawCmdExtendSpline([AssDrawPoint(1, 2)])], "p 1 2"),
        (
            [AssDrawCmdExtendSpline([AssDrawPoint(1, 2), AssDrawPoint(3, 4)])],
            "p 1 2 3 4",
        ),
        ([AssDrawCmdCloseSpline()], "c"),
        (
            [
                AssDrawCmdMove(AssDrawPoint(0, 0), close=True),
                AssDrawCmdLine(
                    [
                        AssDrawPoint(100, 0),
                        AssDrawPoint(100, 100),
                        AssDrawPoint(0, 100),
                    ]
                ),
            ],
            "m 0 0 l 100 0 100 100 0 100",
        ),
        (
            [
                AssDrawCmdMove(AssDrawPoint(0, 0), close=True),
                AssDrawCmdSpline(
                    [
                        AssDrawPoint(100, 0),
                        AssDrawPoint(100, 100),
                        AssDrawPoint(0, 100),
                    ]
                ),
                AssDrawCmdCloseSpline(),
            ],
            "m 0 0 s 100 0 100 100 0 100 c",
        ),
        (
            [
                AssDrawCmdMove(AssDrawPoint(0, 0), close=True),
                AssDrawCmdSpline(
                    [
                        AssDrawPoint(100, 0),
                        AssDrawPoint(100, 100),
                        AssDrawPoint(0, 100),
                    ]
                ),
                AssDrawCmdExtendSpline(
                    [
                        AssDrawPoint(0, 0),
                        AssDrawPoint(100, 0),
                        AssDrawPoint(100, 100),
                    ]
                ),
            ],
            "m 0 0 s 100 0 100 100 0 100 p 0 0 100 0 100 100",
        ),
    ],
)
def test_parsing_valid_commands(
    source: list[AssDrawCmd], expected: str
) -> None:
    assert expected == compose_draw_commands(source)
