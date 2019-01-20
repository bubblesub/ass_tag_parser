import pytest

from ass_tag_parser import *


@pytest.mark.parametrize(
    "source_line,expected_chunks",
    [
        (r"", []),
        (r"{}", [AssTagList([])]),
        (r"test", [AssText("test")]),
        (r"(test)", [AssText("(test)")]),
        (r"{(test)}", [AssTagList([AssTagComment("(test)")])]),
        (r"{\b1()}", [AssTagList([AssTagBold(True), AssTagComment("()")])]),
        (r"{\b1(}", [AssTagList([AssTagBold(True), AssTagComment("(")])]),
        (r"{\b1)}", [AssTagList([AssTagBold(True), AssTagComment(")")])]),
        (
            r"{\t(test)}",
            [AssTagList([AssTagAnimation([AssTagComment("test")])])],
        ),
        (
            r"{\t(test()test)}",
            [AssTagList([AssTagAnimation([AssTagComment("test()test")])])],
        ),
        (
            r"{\t(\t(test))}",
            [
                AssTagList(
                    [
                        AssTagAnimation(
                            [AssTagAnimation([AssTagComment("test")])]
                        )
                    ]
                )
            ],
        ),
        ("{garbage}", [AssTagList([AssTagComment("garbage")])]),
        (r"{asd\Nasd}", [AssTagList([AssTagComment(r"asd\Nasd")])]),
        (
            r"{asd\Nasd\nasd\hasd}",
            [AssTagList([AssTagComment(r"asd\Nasd\nasd\hasd")])],
        ),
        (
            r"{\p2}m 3 4{\p0}",
            [
                AssTagList([AssTagDrawingMode(2)]),
                AssText("m 3 4"),
                AssTagList([AssTagDrawingMode(0)]),
            ],
        ),
        (
            r"{\an5\an5}",
            [
                AssTagList(
                    [AssTagAlignment(5, False), AssTagAlignment(5, False)]
                )
            ],
        ),
        (
            r"{\an5}{\an5}",
            [
                AssTagList([AssTagAlignment(5, False)]),
                AssTagList([AssTagAlignment(5, False)]),
            ],
        ),
        (
            r"abc def{\an5}ghi jkl{\an5}123 456",
            [
                AssText("abc def"),
                AssTagList([AssTagAlignment(5, False)]),
                AssText("ghi jkl"),
                AssTagList([AssTagAlignment(5, False)]),
                AssText("123 456"),
            ],
        ),
        (
            r"I am {\b1}not{\b0} amused.",
            [
                AssText("I am "),
                AssTagList([AssTagBold(True)]),
                AssText("not"),
                AssTagList([AssTagBold(False)]),
                AssText(" amused."),
            ],
        ),
        (
            r"{\b100}How {\b300}bold {\b500}can {\b700}you {\b900}get?",
            [
                AssTagList([AssTagBold(True, 100)]),
                AssText("How "),
                AssTagList([AssTagBold(True, 300)]),
                AssText("bold "),
                AssTagList([AssTagBold(True, 500)]),
                AssText("can "),
                AssTagList([AssTagBold(True, 700)]),
                AssText("you "),
                AssTagList([AssTagBold(True, 900)]),
                AssText("get?"),
            ],
        ),
        (
            r"-Hey\N{\rAlternate}-Huh?\N{\r}-Who are you?",
            [
                AssText(r"-Hey\N"),
                AssTagList([AssTagResetStyle("Alternate")]),
                AssText(r"-Huh?\N"),
                AssTagList([AssTagResetStyle(None)]),
                AssText("-Who are you?"),
            ],
        ),
        (
            r"{\1c&HFF0000&\t(\1c&H0000FF&)}Hello!",
            [
                AssTagList(
                    [
                        AssTagColor(0, 0, 255, 1),
                        AssTagAnimation(tags=[AssTagColor(255, 0, 0, 1)]),
                    ]
                ),
                AssText("Hello!"),
            ],
        ),
        (
            r"{\an5\t(0,5000,\frz3600)}Wheee",
            [
                AssTagList(
                    [
                        AssTagAlignment(5),
                        AssTagAnimation(
                            tags=[AssTagZRotation(3600)], time1=0, time2=5000
                        ),
                    ]
                ),
                AssText("Wheee"),
            ],
        ),
        (
            r"{\an5\t(0,5000,0.5,\frz3600)}Wheee",
            [
                AssTagList(
                    [
                        AssTagAlignment(5),
                        AssTagAnimation(
                            acceleration=0.5,
                            time1=0,
                            time2=5000,
                            tags=[AssTagZRotation(3600)],
                        ),
                    ]
                ),
                AssText("Wheee"),
            ],
        ),
        (
            r"{\an5\fscx0\fscy0\t(0,500,\fscx100\fscy100)}Boo!",
            [
                AssTagList(
                    [
                        AssTagAlignment(5),
                        AssTagFontXScale(0),
                        AssTagFontYScale(0),
                        AssTagAnimation(
                            tags=[
                                AssTagFontXScale(100),
                                AssTagFontYScale(100),
                            ],
                            time1=0,
                            time2=500,
                            acceleration=None,
                        ),
                    ]
                ),
                AssText("Boo!"),
            ],
        ),
        (
            r"{comment\b1}",
            [AssTagList([AssTagComment("comment"), AssTagBold(True, None)])],
        ),
    ],
)
def test_parsing_valid_ass_line(
    source_line: str, expected_chunks: T.List[AssBlock]
) -> None:
    assert AssLine(expected_chunks) == parse_ass(source_line)


@pytest.mark.parametrize(
    "source_line,expected_tag",
    [
        (r"{\i1}", AssTagItalic(enabled=True)),
        (r"{\i0}", AssTagItalic(enabled=False)),
        (r"{\i}", AssTagItalic(enabled=None)),
        (r"{\b300}", AssTagBold(enabled=True, weight=300)),
        (r"{\b1}", AssTagBold(enabled=True, weight=None)),
        (r"{\b0}", AssTagBold(enabled=False, weight=None)),
        (r"{\b}", AssTagBold(enabled=None, weight=None)),
        (r"{\u1}", AssTagUnderline(enabled=True)),
        (r"{\u0}", AssTagUnderline(enabled=False)),
        (r"{\u}", AssTagUnderline(enabled=None)),
        (r"{\s1}", AssTagStrikeout(enabled=True)),
        (r"{\s0}", AssTagStrikeout(enabled=False)),
        (r"{\s}", AssTagStrikeout(enabled=None)),
        (r"{\bord0}", AssTagBorder(size=0)),
        (r"{\xbord0}", AssTagXBorder(size=0)),
        (r"{\ybord0}", AssTagYBorder(size=0)),
        (r"{\bord4.4}", AssTagBorder(size=4.4)),
        (r"{\xbord4.4}", AssTagXBorder(size=4.4)),
        (r"{\ybord4.4}", AssTagYBorder(size=4.4)),
        (r"{\bord}", AssTagBorder(size=None)),
        (r"{\xbord}", AssTagXBorder(size=None)),
        (r"{\ybord}", AssTagYBorder(size=None)),
        (r"{\shad0}", AssTagShadow(size=0)),
        (r"{\xshad0}", AssTagXShadow(size=0)),
        (r"{\yshad0}", AssTagYShadow(size=0)),
        (r"{\shad4.4}", AssTagShadow(size=4.4)),
        (r"{\xshad4.4}", AssTagXShadow(size=4.4)),
        (r"{\yshad4.4}", AssTagYShadow(size=4.4)),
        (r"{\shad}", AssTagShadow(size=None)),
        (r"{\xshad}", AssTagXShadow(size=None)),
        (r"{\yshad}", AssTagYShadow(size=None)),
        (r"{\be2}", AssTagBlurEdges(times=2)),
        (r"{\be}", AssTagBlurEdges(times=None)),
        (r"{\blur4}", AssTagBlurEdgesGauss(weight=4)),
        (r"{\blur4.4}", AssTagBlurEdgesGauss(weight=4.4)),
        (r"{\blur}", AssTagBlurEdgesGauss(weight=None)),
        (r"{\fnArial}", AssTagFontName(name="Arial")),
        (r"{\fnComic Sans}", AssTagFontName(name="Comic Sans")),
        (r"{\fe5}", AssTagFontEncoding(encoding=5)),
        (r"{\fe}", AssTagFontEncoding(encoding=None)),
        (r"{\fs15}", AssTagFontSize(size=15)),
        (r"{\fs}", AssTagFontSize(size=None)),
        (r"{\fscx5.5}", AssTagFontXScale(scale=5.5)),
        (r"{\fscy5.5}", AssTagFontYScale(scale=5.5)),
        (r"{\fscx}", AssTagFontXScale(scale=None)),
        (r"{\fscy}", AssTagFontYScale(scale=None)),
        (r"{\fsp5.5}", AssTagLetterSpacing(spacing=5.5)),
        (r"{\fsp-5.5}", AssTagLetterSpacing(spacing=-5.5)),
        (r"{\fsp}", AssTagLetterSpacing(spacing=None)),
        (r"{\frx5.5}", AssTagXRotation(angle=5.5)),
        (r"{\frx-5.5}", AssTagXRotation(angle=-5.5)),
        (r"{\frx}", AssTagXRotation(angle=None)),
        (r"{\fry5.5}", AssTagYRotation(angle=5.5)),
        (r"{\fry-5.5}", AssTagYRotation(angle=-5.5)),
        (r"{\fry}", AssTagYRotation(angle=None)),
        (r"{\frz5.5}", AssTagZRotation(angle=5.5)),
        (r"{\frz-5.5}", AssTagZRotation(angle=-5.5)),
        (r"{\frz}", AssTagZRotation(angle=None)),
        (r"{\fr5.5}", AssTagZRotation(angle=5.5, short=True)),
        (r"{\fr-5.5}", AssTagZRotation(angle=-5.5, short=True)),
        (r"{\fr}", AssTagZRotation(angle=None, short=True)),
        (r"{\org(1,2)}", AssTagRotationOrigin(x=1, y=2)),
        (r"{\org(-1,-2)}", AssTagRotationOrigin(x=-1, y=-2)),
        (r"{\fax-1.5}", AssTagXShear(value=-1.5)),
        (r"{\fay-1.5}", AssTagYShear(value=-1.5)),
        (r"{\c&H123456&}", AssTagColor(0x56, 0x34, 0x12, 1, short=True)),
        (r"{\1c&H123456&}", AssTagColor(0x56, 0x34, 0x12, 1)),
        (r"{\2c&H123456&}", AssTagColor(0x56, 0x34, 0x12, 2)),
        (r"{\3c&H123456&}", AssTagColor(0x56, 0x34, 0x12, 3)),
        (r"{\4c&H123456&}", AssTagColor(0x56, 0x34, 0x12, 4)),
        (r"{\c}", AssTagColor(None, None, None, 1, short=True)),
        (r"{\1c}", AssTagColor(None, None, None, 1)),
        (r"{\2c}", AssTagColor(None, None, None, 2)),
        (r"{\3c}", AssTagColor(None, None, None, 3)),
        (r"{\4c}", AssTagColor(None, None, None, 4)),
        (r"{\alpha&H12&}", AssTagAlpha(0x12, 0)),
        (r"{\1a&H12&}", AssTagAlpha(0x12, 1)),
        (r"{\2a&H12&}", AssTagAlpha(0x12, 2)),
        (r"{\3a&H12&}", AssTagAlpha(0x12, 3)),
        (r"{\4a&H12&}", AssTagAlpha(0x12, 4)),
        (r"{\alpha}", AssTagAlpha(None, 0)),
        (r"{\1a}", AssTagAlpha(None, 1)),
        (r"{\2a}", AssTagAlpha(None, 2)),
        (r"{\3a}", AssTagAlpha(None, 3)),
        (r"{\4a}", AssTagAlpha(None, 4)),
        (r"{\K50}", AssTagKaraoke1(duration=500)),
        (r"{\k50}", AssTagKaraoke2(duration=500)),
        (r"{\kf50}", AssTagKaraoke3(duration=500)),
        (r"{\ko50}", AssTagKaraoke4(duration=500)),
        (r"{\an5}", AssTagAlignment(alignment=5, legacy=False)),
        (r"{\an}", AssTagAlignment(alignment=None, legacy=False)),
        (r"{\a1}", AssTagAlignment(alignment=1, legacy=True)),
        (r"{\a2}", AssTagAlignment(alignment=2, legacy=True)),
        (r"{\a3}", AssTagAlignment(alignment=3, legacy=True)),
        (r"{\a5}", AssTagAlignment(alignment=4, legacy=True)),
        (r"{\a6}", AssTagAlignment(alignment=5, legacy=True)),
        (r"{\a7}", AssTagAlignment(alignment=6, legacy=True)),
        (r"{\a9}", AssTagAlignment(alignment=7, legacy=True)),
        (r"{\a10}", AssTagAlignment(alignment=8, legacy=True)),
        (r"{\a11}", AssTagAlignment(alignment=9, legacy=True)),
        (r"{\a}", AssTagAlignment(alignment=None, legacy=True)),
        (r"{\q0}", AssTagWrapStyle(style=0)),
        (r"{\q1}", AssTagWrapStyle(style=1)),
        (r"{\q2}", AssTagWrapStyle(style=2)),
        (r"{\q3}", AssTagWrapStyle(style=3)),
        (r"{\r}", AssTagResetStyle(style=None)),
        (r"{\rSome style}", AssTagResetStyle(style="Some style")),
        (r"{\p1}", AssTagDrawingMode(scale=1)),
        (r"{\pbo-50}", AssTagBaselineOffset(y=-50)),
        (r"{\pos(1,2)}", AssTagPosition(x=1, y=2)),
        (
            r"{\move(1,2,3,4)}",
            AssTagMove(x1=1, y1=2, x2=3, y2=4, time1=None, time2=None),
        ),
        (
            r"{\move(1,2,3,4,100,300)}",
            AssTagMove(x1=1, y1=2, x2=3, y2=4, time1=100, time2=300),
        ),
        (r"{\fad(100,200)}", AssTagFade(time1=100, time2=200)),
        (
            r"{\fade(1,2,3,4,5,6,7)}",
            AssTagFadeComplex(
                alpha1=1,
                alpha2=2,
                alpha3=3,
                time1=4,
                time2=5,
                time3=6,
                time4=7,
            ),
        ),
        (
            r"{\t(50,100,1.2,\be5\fs40)}",
            AssTagAnimation(
                tags=[AssTagBlurEdges(5), AssTagFontSize(40)],
                time1=50,
                time2=100,
                acceleration=1.2,
            ),
        ),
        (
            r"{\t(1.2,\be5\fs40)}",
            AssTagAnimation(
                tags=[AssTagBlurEdges(5), AssTagFontSize(40)],
                time1=None,
                time2=None,
                acceleration=1.2,
            ),
        ),
        (
            r"{\t(50,100,\be5\fs40)}",
            AssTagAnimation(
                tags=[AssTagBlurEdges(5), AssTagFontSize(40)],
                time1=50,
                time2=100,
                acceleration=None,
            ),
        ),
        (
            r"{\t(\be5\fs40)}",
            AssTagAnimation(
                tags=[AssTagBlurEdges(5), AssTagFontSize(40)],
                time1=None,
                time2=None,
                acceleration=None,
            ),
        ),
        (
            r"{\clip(1,2,3,4)}",
            AssTagClipRectangle(x1=1, y1=2, x2=3, y2=4, inverse=False),
        ),
        (
            r"{\iclip(1,2,3,4)}",
            AssTagClipRectangle(x1=1, y1=2, x2=3, y2=4, inverse=True),
        ),
        (
            r"{\clip(1,m 50 0)}",
            AssTagClipVector(scale=1, path="m 50 0", inverse=False),
        ),
        (
            r"{\iclip(1,m 50 0)}",
            AssTagClipVector(scale=1, path="m 50 0", inverse=True),
        ),
        (
            r"{\clip(m 50 0)}",
            AssTagClipVector(scale=None, path="m 50 0", inverse=False),
        ),
        (
            r"{\iclip(m 50 0)}",
            AssTagClipVector(scale=None, path="m 50 0", inverse=True),
        ),
    ],
)
def test_parsing_valid_single_tag(
    source_line: str, expected_tag: AssTag
) -> None:
    expected_tree = AssLine([AssTagList(tags=[expected_tag])])
    assert expected_tree == parse_ass(source_line)


@pytest.mark.parametrize(
    "source_line,error_msg",
    [
        (r"{", "syntax error at pos 1: unterminated curly brace"),
        (r"}", "syntax error at pos 0: unexpected curly brace"),
        (r"{\t({)}", "syntax error at pos 4: unexpected curly brace"),
        (r"{\t(})}", "syntax error at pos 4: unexpected curly brace"),
        (r"test{", "syntax error at pos 5: unterminated curly brace"),
        (r"test}", "syntax error at pos 4: unexpected curly brace"),
        (r"}test{", "syntax error at pos 0: unexpected curly brace"),
        (r"{{asd}", "syntax error at pos 1: unexpected curly brace"),
        (r"{asd}}", "syntax error at pos 5: unexpected curly brace"),
        (r"{{asd}}", "syntax error at pos 1: unexpected curly brace"),
        (r"{\b-1}", r"syntax error at pos 5: \b takes only positive integers"),
        (
            r"{\bord-4}",
            r"syntax error at pos 8: \bord takes only positive decimals",
        ),
        (
            r"{\xbord-4}",
            r"syntax error at pos 9: \xbord takes only positive decimals",
        ),
        (
            r"{\ybord-4}",
            r"syntax error at pos 9: \ybord takes only positive decimals",
        ),
        (
            r"{\shad-4}",
            r"syntax error at pos 8: \shad takes only positive decimals",
        ),
        (
            r"{\xshad-4}",
            r"syntax error at pos 9: \xshad takes only positive decimals",
        ),
        (
            r"{\yshad-4}",
            r"syntax error at pos 9: \yshad takes only positive decimals",
        ),
        (
            r"{\be-2}",
            r"syntax error at pos 6: \be takes only positive integers",
        ),
        (
            r"{\blur-4}",
            r"syntax error at pos 8: \blur takes only positive decimals",
        ),
        (
            r"{\fe-5}",
            r"syntax error at pos 6: \fe takes only positive integers",
        ),
        (
            r"{\fs-5}",
            r"syntax error at pos 6: \fs takes only positive integers",
        ),
        (
            r"{\fscx-5.5}",
            r"syntax error at pos 10: \fscx takes only positive decimals",
        ),
        (
            r"{\fscy-5.5}",
            r"syntax error at pos 10: \fscy takes only positive decimals",
        ),
        (r"{\org0,0}", "syntax error at pos 6: expected brace"),
        (
            r"{\org(0)}",
            r"syntax error at pos 8: \org takes 2 arguments (got 1)",
        ),
        (
            r"{\org(0,0,0)}",
            r"syntax error at pos 12: \org takes 2 arguments (got 3)",
        ),
        (
            r"{\org(-5.5,0)}",
            r"syntax error at pos 13: \org takes only integer arguments",
        ),
        (r"{\pos0,0}", "syntax error at pos 6: expected brace"),
        (
            r"{\pos(0)}",
            r"syntax error at pos 8: \pos takes 2 arguments (got 1)",
        ),
        (
            r"{\pos(0,0,0)}",
            r"syntax error at pos 12: \pos takes 2 arguments (got 3)",
        ),
        (
            r"{\pos(-5.5,0)}",
            r"syntax error at pos 13: \pos takes only integer arguments",
        ),
        (r"{\move0,0,0,0}", "syntax error at pos 7: expected brace"),
        (
            r"{\move(0,0,0)}",
            r"syntax error at pos 13: \move takes 4 or 6 arguments (got 3)",
        ),
        (
            r"{\move(0,0,0,0,0)}",
            r"syntax error at pos 17: \move takes 4 or 6 arguments (got 5)",
        ),
        (
            r"{\move(0,0,0,5.5)}",
            r"syntax error at pos 17: \move takes only integer arguments",
        ),
        (
            r"{\move(0,0,0,0,0,5.5)}",
            r"syntax error at pos 21: \move takes only integer arguments",
        ),
        (r"{\c&123456&}", "syntax error at pos 5: expected uppercase H"),
        (
            r"{\1c&H12345&}",
            "syntax error at pos 12: expected hexadecimal number",
        ),
        (r"{\1c&H1234567&}", "syntax error at pos 13: expected ampersand"),
        (
            r"{\1c&H12345G&}",
            "syntax error at pos 12: expected hexadecimal number",
        ),
        (r"{\alpha&12&}", "syntax error at pos 9: expected uppercase H"),
        (r"{\1a&H1&}", "syntax error at pos 8: expected hexadecimal number"),
        (r"{\1a&H123&}", "syntax error at pos 9: expected ampersand"),
        (r"{\1a&H1G&}", "syntax error at pos 8: expected hexadecimal number"),
        (r"{\k-5}", r"syntax error at pos 5: \k takes only positive integers"),
        (r"{\K-5}", r"syntax error at pos 5: \K takes only positive integers"),
        (
            r"{\kf-5}",
            r"syntax error at pos 6: \kf takes only positive integers",
        ),
        (
            r"{\ko-5}",
            r"syntax error at pos 6: \ko takes only positive integers",
        ),
        (r"{\k}", r"syntax error at pos 3: \k requires an argument"),
        (r"{\K}", r"syntax error at pos 3: \K requires an argument"),
        (r"{\kf}", r"syntax error at pos 4: \kf requires an argument"),
        (r"{\ko}", r"syntax error at pos 4: \ko requires an argument"),
        (r"{\an10}", r"syntax error at pos 6: \an expects 1-9"),
        (r"{\a4}", r"syntax error at pos 4: \a expects 1-3, 5-7 or 9-11"),
        (r"{\a8}", r"syntax error at pos 4: \a expects 1-3, 5-7 or 9-11"),
        (r"{\a12}", r"syntax error at pos 5: \a expects 1-3, 5-7 or 9-11"),
        (r"{\q5}", r"syntax error at pos 4: \q expects 0, 1, 2 or 3"),
        (r"{\garbage}", "syntax error at pos 1: unrecognized tag"),
        (r"{\5c&H123456&}", "syntax error at pos 1: unrecognized tag"),
        (r"{\5a&H12&}", "syntax error at pos 1: unrecognized tag"),
        (r"{\1c&HFFFFFF&derp}", "syntax error at pos 13: extra data"),
        (r"{\1a&HFF&derp}", "syntax error at pos 9: extra data"),
        (r"{\be2a}", r"syntax error at pos 6: \be requires an integer"),
        (r"{\be2.2}", r"syntax error at pos 7: \be requires an integer"),
        (r"{\fs5.4}", r"syntax error at pos 7: \fs requires an integer"),
        (r"{\k50.5}", r"syntax error at pos 7: \k requires an integer"),
        (r"{\K50.5}", r"syntax error at pos 7: \K requires an integer"),
        (r"{\kf50.5}", r"syntax error at pos 8: \kf requires an integer"),
        (r"{\ko50.5}", r"syntax error at pos 8: \ko requires an integer"),
        (r"{\i-2}", r"syntax error at pos 5: \i requires a boolean"),
        (r"{\i2}", r"syntax error at pos 4: \i requires a boolean"),
        (r"{\u2}", r"syntax error at pos 4: \u requires a boolean"),
        (r"{\s2}", r"syntax error at pos 4: \s requires a boolean"),
        (
            r"{\c(123456)}",
            r"syntax error at pos 3: \c doesn't take complex arguments",
        ),
        (
            r"{\fn(Comic Sans)}",
            r"syntax error at pos 4: \fn doesn't take complex arguments",
        ),
        (
            r"{\a(12)}",
            r"syntax error at pos 3: \a doesn't take complex arguments",
        ),
        (r"{\b1comment}", r"syntax error at pos 11: \b requires an integer"),
        (r"{asd\asd}", r"syntax error at pos 8: \a requires an integer"),
    ],
)
def test_parsing_invalid_ass_line(source_line: str, error_msg: str) -> None:
    with pytest.raises(ParseError) as exc_info:
        parse_ass(source_line)
    assert error_msg == str(exc_info.value)
