from ass_tag_analyzer.ass_item.ass_valid_tag.ass_valid_tag_font_scale import (
    AssValidTagFontScale,
    AssValidTagFontXScale,
    AssValidTagFontYScale,
)


def test_ass_valid_tag_font_scale():

    assert str(AssValidTagFontScale()) == "\\fsc"


def test_ass_valid_tag_font_x_scale():

    assert str(AssValidTagFontXScale(20)) == "\\fscx20"


def test_ass_valid_tag_font_y_scale():

    assert str(AssValidTagFontYScale(20)) == "\\fscy20"
