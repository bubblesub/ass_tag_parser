from ass_tag_analyzer.ass_item.ass_valid_tag.ass_valid_tag_general import (
    AssValidTagAnimation,
    AssValidTagBaselineOffset,
    AssValidTagBold,
    AssValidTagDraw,
    AssValidTagFontEncoding,
    AssValidTagFontName,
    AssValidTagFontSize,
    AssValidTagItalic,
    AssValidTagLetterSpacing,
    AssValidTagResetStyle,
    AssValidTagRotationOrigin,
    AssValidTagStrikeout,
    AssValidTagUnderline,
)


def test_ass_valid_tag_animation():
    assert str(AssValidTagAnimation([AssValidTagBold(0)])) == "\\t(\\b0)"

    assert (
        str(AssValidTagAnimation([AssValidTagBold(0)], acceleration=5)) == "\\t(5,\\b0)"
    )

    assert (
        str(AssValidTagAnimation([AssValidTagBold(0)], time1=20, time2=40))
        == "\\t(20,40,\\b0)"
    )
    assert str(AssValidTagAnimation([AssValidTagBold(0)], time1=20)) == "\\t(\\b0)"

    assert (
        str(
            AssValidTagAnimation(
                [AssValidTagBold(0)], acceleration=2, time1=20, time2=40
            )
        )
        == "\\t(20,40,2,\\b0)"
    )
    assert (
        str(AssValidTagAnimation([AssValidTagBold(0)], acceleration=2, time1=20))
        == "\\t(2,\\b0)"
    )


def test_ass_valid_tag_baseline_offset():
    assert str(AssValidTagBaselineOffset(20.2)) == "\\pbo20.2"


def test_ass_valid_tag_bold():
    assert str(AssValidTagBold(0)) == "\\b0"
    assert AssValidTagBold(0).weight == 400
    assert AssValidTagBold(1).weight == 700
    assert str(AssValidTagBold(100)) == "\\b100"


def test_ass_valid_tag_draw():
    assert str(AssValidTagDraw(0)) == "\\p0"
    assert str(AssValidTagDraw(-1)) == "\\p0"


def test_ass_valid_tag_font_encoding():
    assert str(AssValidTagFontEncoding(0)) == "\\fe0"


def test_ass_valid_tag_font_name():
    assert str(AssValidTagFontName("   \tJester\t  ")) == "\\fnJester"


def test_ass_valid_tag_font_size():
    assert str(AssValidTagFontSize(20)) == "\\fs20"


def test_ass_valid_tag_italic():
    assert str(AssValidTagItalic(True)) == "\\i1"
    assert str(AssValidTagItalic(False)) == "\\i0"


def test_ass_valid_tag_letter_spacing():
    assert str(AssValidTagLetterSpacing(20.320)) == "\\fsp20.32"


def test_ass_valid_tag_reset_style():
    assert str(AssValidTagResetStyle()) == "\\r"
    assert str(AssValidTagResetStyle("Test")) == "\\rTest"


def test_ass_valid_tag_rotation_origin():
    assert str(AssValidTagRotationOrigin(20.43, 21.43)) == "\\org(20.43,21.43)"


def test_ass_valid_tag_strikeout():
    assert str(AssValidTagStrikeout(True)) == "\\s1"
    assert str(AssValidTagStrikeout(False)) == "\\s0"


def test_ass_valid_tag_underline():
    assert str(AssValidTagUnderline(True)) == "\\u1"
    assert str(AssValidTagUnderline(False)) == "\\u0"
