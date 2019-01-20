import pytest

from ass_tag_parser import *


@pytest.mark.parametrize(
    "source_blocks,expected_line",
    [
        ([], ""),
        ([AssText("test")], r"test"),
        ([AssTagList([])], "{}"),
        ([AssTagList([AssTagComment("asdasd")])], r"{asdasd}"),
        (
            [
                AssTagList([AssTagDrawingMode(2)]),
                AssText("m 3 4"),
                AssTagList([AssTagDrawingMode(0)]),
            ],
            r"{\p2}m 3 4{\p0}",
        ),
        (
            [
                AssTagList(
                    [
                        AssTagAlignment(5, legacy=False),
                        AssTagAlignment(5, legacy=True),
                    ]
                )
            ],
            r"{\an5\a6}",
        ),
        (
            [
                AssTagList([AssTagAlignment(5, legacy=False)]),
                AssTagList([AssTagAlignment(5, legacy=False)]),
            ],
            r"{\an5}{\an5}",
        ),
        (
            [
                AssText("abc def"),
                AssTagList([AssTagAlignment(5, legacy=False)]),
                AssText("ghi jkl"),
                AssTagList([AssTagAlignment(5, legacy=False)]),
                AssText("123 456"),
            ],
            r"abc def{\an5}ghi jkl{\an5}123 456",
        ),
        (
            [
                AssText("I am "),
                AssTagList([AssTagBold(enabled=True)]),
                AssText("not"),
                AssTagList([AssTagBold(enabled=False)]),
                AssText(" amused."),
            ],
            r"I am {\b1}not{\b0} amused.",
        ),
        (
            [
                AssTagList([AssTagBold(weight=100)]),
                AssText("How "),
                AssTagList([AssTagBold(weight=300)]),
                AssText("bold "),
                AssTagList([AssTagBold(weight=500)]),
                AssText("can "),
                AssTagList([AssTagBold(weight=700)]),
                AssText("you "),
                AssTagList([AssTagBold(weight=900)]),
                AssText("get?"),
            ],
            r"{\b100}How {\b300}bold {\b500}can {\b700}you {\b900}get?",
        ),
        (
            [
                AssText(r"-Hey\N"),
                AssTagList([AssTagResetStyle(style="Alternate")]),
                AssText(r"-Huh?\N"),
                AssTagList([AssTagResetStyle(style=None)]),
                AssText("-Who are you?"),
            ],
            r"-Hey\N{\rAlternate}-Huh?\N{\r}-Who are you?",
        ),
        (
            [
                AssTagList(
                    [
                        AssTagColor(0, 0, 255, 1),
                        AssTagAnimation(tags=[AssTagColor(255, 0, 0, 1)]),
                    ]
                ),
                AssText("Hello!"),
            ],
            r"{\1c&HFF0000&\t(\1c&H0000FF&)}Hello!",
        ),
        (
            [
                AssTagList(
                    [
                        AssTagAlignment(5, legacy=False),
                        AssTagAnimation(
                            [AssTagZRotation(angle=3600)],
                            time1=0,
                            time2=5000,
                            acceleration=None,
                        ),
                    ]
                ),
                AssText("Wheee"),
            ],
            r"{\an5\t(0,5000,\frz3600)}Wheee",
        ),
        (
            [
                AssTagList(
                    [
                        AssTagAlignment(5, legacy=False),
                        AssTagAnimation(
                            [AssTagZRotation(angle=3600)],
                            time1=0,
                            time2=5000,
                            acceleration=0.5,
                        ),
                    ]
                ),
                AssText("Wheee"),
            ],
            r"{\an5\t(0,5000,0.5,\frz3600)}Wheee",
        ),
        (
            [
                AssTagList(
                    [
                        AssTagAlignment(5, legacy=False),
                        AssTagFontXScale(0),
                        AssTagFontYScale(0),
                        AssTagAnimation(
                            [AssTagFontXScale(100), AssTagFontYScale(100)],
                            time1=0,
                            time2=500,
                            acceleration=None,
                        ),
                    ]
                ),
                AssText("Boo!"),
            ],
            r"{\an5\fscx0\fscy0\t(0,500,\fscx100\fscy100)}Boo!",
        ),
        (
            [AssTagList([AssTagComment("comment"), AssTagBold(enabled=True)])],
            r"{comment\b1}",
        ),
        (
            [
                AssTagList(
                    [AssTagBold(enabled=True), AssTagComment(text="comment")]
                )
            ],
            r"{\b1comment}",
        ),
        (
            [AssTagList([AssTagAlpha(0xFF, 2), AssTagComment("comment")])],
            r"{\2a&HFF&comment}",
        ),
        (
            [AssTagList([AssTagBlurEdges(times=2), AssTagComment(".2")])],
            r"{\be2.2}",
        ),
        (
            [AssTagList([AssTagFontSize(size=5), AssTagComment(text=".4")])],
            r"{\fs5.4}",
        ),
        (
            [AssTagList([AssTagKaraoke1(duration=500), AssTagComment(".5")])],
            r"{\k50.5}",
        ),
        (
            [AssTagList([AssTagKaraoke2(duration=500), AssTagComment(".5")])],
            r"{\K50.5}",
        ),
        (
            [AssTagList([AssTagKaraoke3(duration=500), AssTagComment(".5")])],
            r"{\kf50.5}",
        ),
        (
            [AssTagList([AssTagKaraoke4(duration=500), AssTagComment(".5")])],
            r"{\ko50.5}",
        ),
    ],
)
def test_composing_valid_ass_line(
    source_blocks: T.List[AssBlock], expected_line: str
) -> None:
    assert expected_line == compose_ass(AssLine(source_blocks))


@pytest.mark.parametrize(
    "source_tag,expected_line",
    [
        (AssTagItalic(enabled=True), r"{\i1}"),
        (AssTagItalic(enabled=False), r"{\i0}"),
        (AssTagBold(weight=300), r"{\b300}"),
        (AssTagBold(enabled=True), r"{\b1}"),
        (AssTagBold(enabled=False), r"{\b0}"),
        (AssTagUnderline(enabled=True), r"{\u1}"),
        (AssTagUnderline(enabled=False), r"{\u0}"),
        (AssTagStrikeout(enabled=True), r"{\s1}"),
        (AssTagStrikeout(enabled=False), r"{\s0}"),
        (AssTagBorder(size=0), r"{\bord0}"),
        (AssTagXBorder(size=0), r"{\xbord0}"),
        (AssTagYBorder(size=0), r"{\ybord0}"),
        (AssTagBorder(size=4.4), r"{\bord4.4}"),
        (AssTagXBorder(size=4.4), r"{\xbord4.4}"),
        (AssTagYBorder(size=4.4), r"{\ybord4.4}"),
        (AssTagShadow(size=0), r"{\shad0}"),
        (AssTagXShadow(size=0), r"{\xshad0}"),
        (AssTagYShadow(size=0), r"{\yshad0}"),
        (AssTagShadow(size=4.4), r"{\shad4.4}"),
        (AssTagXShadow(size=4.4), r"{\xshad4.4}"),
        (AssTagYShadow(size=4.4), r"{\yshad4.4}"),
        (AssTagBlurEdges(times=2), r"{\be2}"),
        (AssTagBlurEdgesGauss(weight=4.4), r"{\blur4.4}"),
        (AssTagFontName(name="Arial"), r"{\fnArial}"),
        (AssTagFontName(name="Comic Sans"), r"{\fnComic Sans}"),
        (AssTagFontName(name="Comic Sans"), r"{\fnComic Sans}"),
        (AssTagFontEncoding(encoding=5), r"{\fe5}"),
        (AssTagFontSize(size=15), r"{\fs15}"),
        (AssTagFontXScale(scale=5.5), r"{\fscx5.5}"),
        (AssTagFontYScale(scale=5.5), r"{\fscy5.5}"),
        (AssTagLetterSpacing(spacing=5.5), r"{\fsp5.5}"),
        (AssTagLetterSpacing(spacing=-5.5), r"{\fsp-5.5}"),
        (AssTagXRotation(angle=5.5), r"{\frx5.5}"),
        (AssTagXRotation(angle=-5.5), r"{\frx-5.5}"),
        (AssTagYRotation(angle=5.5), r"{\fry5.5}"),
        (AssTagYRotation(angle=-5.5), r"{\fry-5.5}"),
        (AssTagZRotation(angle=5.5), r"{\frz5.5}"),
        (AssTagZRotation(angle=-5.5), r"{\frz-5.5}"),
        (AssTagRotationOrigin(x=1, y=2), r"{\org(1,2)}"),
        (AssTagRotationOrigin(x=-1, y=-2), r"{\org(-1,-2)}"),
        (AssTagXShear(value=-1.5), r"{\fax-1.5}"),
        (AssTagYShear(value=-1.5), r"{\fay-1.5}"),
        (AssTagColor(0x56, 0x34, 0x12, 1), r"{\1c&H123456&}"),
        (AssTagColor(0x56, 0x34, 0x12, 2), r"{\2c&H123456&}"),
        (AssTagColor(0x56, 0x34, 0x12, 3), r"{\3c&H123456&}"),
        (AssTagColor(0x56, 0x34, 0x12, 4), r"{\4c&H123456&}"),
        (AssTagAlpha(0x12, 0), r"{\alpha&H12&}"),
        (AssTagAlpha(0x12, 1), r"{\1a&H12&}"),
        (AssTagAlpha(0x12, 2), r"{\2a&H12&}"),
        (AssTagAlpha(0x12, 3), r"{\3a&H12&}"),
        (AssTagAlpha(0x12, 4), r"{\4a&H12&}"),
        (AssTagKaraoke1(duration=500), r"{\k50}"),
        (AssTagKaraoke2(duration=500), r"{\K50}"),
        (AssTagKaraoke3(duration=500), r"{\kf50}"),
        (AssTagKaraoke4(duration=500), r"{\ko50}"),
        (AssTagAlignment(5, legacy=False), r"{\an5}"),
        (AssTagAlignment(1, legacy=True), r"{\a1}"),
        (AssTagAlignment(2, legacy=True), r"{\a2}"),
        (AssTagAlignment(3, legacy=True), r"{\a3}"),
        (AssTagAlignment(4, legacy=True), r"{\a5}"),
        (AssTagAlignment(5, legacy=True), r"{\a6}"),
        (AssTagAlignment(6, legacy=True), r"{\a7}"),
        (AssTagAlignment(7, legacy=True), r"{\a9}"),
        (AssTagAlignment(8, legacy=True), r"{\a10}"),
        (AssTagAlignment(9, legacy=True), r"{\a11}"),
        (AssTagWrapStyle(style=0), r"{\q0}"),
        (AssTagWrapStyle(style=1), r"{\q1}"),
        (AssTagWrapStyle(style=2), r"{\q2}"),
        (AssTagWrapStyle(style=3), r"{\q3}"),
        (AssTagResetStyle(style=None), r"{\r}"),
        (AssTagResetStyle(style="Some style"), r"{\rSome style}"),
        (AssTagDrawingMode(scale=1), r"{\p1}"),
        (AssTagBaselineOffset(y=-50), r"{\pbo-50}"),
        (AssTagPosition(x=1, y=2), r"{\pos(1,2)}"),
        (
            AssTagMove(x1=1, y1=2, x2=3, y2=4, time1=None, time2=None),
            r"{\move(1,2,3,4)}",
        ),
        (
            AssTagMove(x1=1, y1=2, x2=3, y2=4, time1=100, time2=300),
            r"{\move(1,2,3,4,100,300)}",
        ),
        (AssTagFade(time1=100, time2=200), r"{\fad(100,200)}"),
        (
            AssTagFadeComplex(
                alpha1=1,
                alpha2=2,
                alpha3=3,
                time1=4,
                time2=5,
                time3=6,
                time4=7,
            ),
            r"{\fade(1,2,3,4,5,6,7)}",
        ),
        (
            AssTagAnimation(
                [AssTagBlurEdges(5), AssTagFontSize(40)],
                time1=50,
                time2=100,
                acceleration=1.2,
            ),
            r"{\t(50,100,1.2,\be5\fs40)}",
        ),
        (
            AssTagAnimation(
                [AssTagBlurEdges(5), AssTagFontSize(40)], acceleration=1.2
            ),
            r"{\t(1.2,\be5\fs40)}",
        ),
        (
            AssTagAnimation(
                [AssTagBlurEdges(5), AssTagFontSize(40)], time1=50, time2=100
            ),
            r"{\t(50,100,\be5\fs40)}",
        ),
        (
            AssTagAnimation([AssTagBlurEdges(5), AssTagFontSize(40)]),
            r"{\t(\be5\fs40)}",
        ),
        (
            AssTagClipRectangle(x1=1, y1=2, x2=3, y2=4, inverse=False),
            r"{\clip(1,2,3,4)}",
        ),
        (
            AssTagClipRectangle(x1=1, y1=2, x2=3, y2=4, inverse=True),
            r"{\iclip(1,2,3,4)}",
        ),
        (
            AssTagClipVector(scale=1, path="m 50 0", inverse=False),
            r"{\clip(1,m 50 0)}",
        ),
        (
            AssTagClipVector(scale=1, path="m 50 0", inverse=True),
            r"{\iclip(1,m 50 0)}",
        ),
        (
            AssTagClipVector(scale=None, path="m 50 0", inverse=False),
            r"{\clip(m 50 0)}",
        ),
        (
            AssTagClipVector(scale=None, path="m 50 0", inverse=True),
            r"{\iclip(m 50 0)}",
        ),
    ],
)
def test_composing_valid_single_tag(
    source_tag: AssTag, expected_line: str
) -> None:
    source_line = AssLine([AssTagList([source_tag])])
    assert expected_line == compose_ass(source_line)
