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
    ParseError,
    parse_draw_commands,
)


@pytest.mark.parametrize(
    "source,expected",
    [
        ("m 0 0", [AssDrawCmdMove(AssDrawPoint(0, 0), close=True)]),
        ("m0 0", [AssDrawCmdMove(AssDrawPoint(0, 0), close=True)]),
        (
            "m0 0c",
            [
                AssDrawCmdMove(AssDrawPoint(0, 0), close=True),
                AssDrawCmdCloseSpline(),
            ],
        ),
        (
            "m0 0m0 0",
            [
                AssDrawCmdMove(AssDrawPoint(0, 0), close=True),
                AssDrawCmdMove(AssDrawPoint(0, 0), close=True),
            ],
        ),
        ("m 1.1 2.2", [AssDrawCmdMove(AssDrawPoint(1.1, 2.2), close=True)]),
        ("m -1 2", [AssDrawCmdMove(AssDrawPoint(-1, 2), close=True)]),
        ("n 1 2", [AssDrawCmdMove(AssDrawPoint(1, 2), close=False)]),
        ("l 1 2", [AssDrawCmdLine([AssDrawPoint(1, 2)])]),
        (
            "l 1 2 3 4",
            [AssDrawCmdLine([AssDrawPoint(1, 2), AssDrawPoint(3, 4)])],
        ),
        (
            "b 1 2 3 4 5 6",
            [
                AssDrawCmdBezier(
                    (
                        AssDrawPoint(1, 2),
                        AssDrawPoint(3, 4),
                        AssDrawPoint(5, 6),
                    )
                )
            ],
        ),
        (
            "s 1 2 3 4 5 6",
            [
                AssDrawCmdSpline(
                    [
                        AssDrawPoint(1, 2),
                        AssDrawPoint(3, 4),
                        AssDrawPoint(5, 6),
                    ]
                )
            ],
        ),
        (
            "s 1 2 3 4 5 6 7 8 9 10",
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
        ),
        ("p 1 2", [AssDrawCmdExtendSpline([AssDrawPoint(1, 2)])]),
        (
            "p 1 2 3 4",
            [AssDrawCmdExtendSpline([AssDrawPoint(1, 2), AssDrawPoint(3, 4)])],
        ),
        ("c", [AssDrawCmdCloseSpline()]),
        (
            "m 0 0 l 100 0 100 100 0 100",
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
        ),
        (
            "m 0 0 s 100 0 100 100 0 100 c",
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
        ),
        (
            "m 0 0 s 100 0 100 100 0 100 p 0 0 100 0 100 100",
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
        ),
    ],
)
def test_parsing_valid_text(source: str, expected: list[AssDrawCmd]) -> None:
    assert expected == parse_draw_commands(source)


@pytest.mark.parametrize(
    "source,error_msg",
    [
        ("m 1", "syntax error at pos 3: expected number"),
        ("m 1 2 3", "syntax error at pos 6: unknown draw command 3"),
        ("l", "syntax error at pos 1: expected number"),
        ("l 1", "syntax error at pos 3: expected number"),
        ("l 1 2 3", "syntax error at pos 7: expected number"),
        ("l 1 2 3 4 5", "syntax error at pos 11: expected number"),
        ("b", "syntax error at pos 1: expected number"),
        ("b 1", "syntax error at pos 3: expected number"),
        ("b 1 2", "syntax error at pos 5: expected number"),
        ("b 1 2 3", "syntax error at pos 7: expected number"),
        ("b 1 2 3 4", "syntax error at pos 9: expected number"),
        ("b 1 2 3 4 5", "syntax error at pos 11: expected number"),
        ("b 1 2 3 4 5 6 7", "syntax error at pos 14: unknown draw command 7"),
        (
            "b 1 2 3 4 5 6 7 8",
            "syntax error at pos 14: unknown draw command 7",
        ),
        ("s", "syntax error at pos 1: expected number"),
        ("s 1", "syntax error at pos 3: expected number"),
        ("s 1 2", "syntax error at pos 5: expected number"),
        ("s 1 2 3", "syntax error at pos 7: expected number"),
        ("s 1 2 3 4", "syntax error at pos 9: expected number"),
        ("s 1 2 3 4 5", "syntax error at pos 11: expected number"),
        ("p 1 2 3 4 5 6 7", "syntax error at pos 15: expected number"),
        ("p 1", "syntax error at pos 3: expected number"),
        ("p 1 2 3", "syntax error at pos 7: expected number"),
        ("p 1 2 3 4 5", "syntax error at pos 11: expected number"),
    ],
)
def test_parsing_invalid_text(source: str, error_msg: str) -> None:
    with pytest.raises(ParseError) as exc_info:
        parse_draw_commands(source)
    assert error_msg == str(exc_info.value)
