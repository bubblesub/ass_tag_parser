from ass_tag_analyzer.ass_item.ass_valid_tag.ass_valid_tag_shadow import (
    AssValidTagShadow,
    AssValidTagXShadow,
    AssValidTagYShadow,
)


def test_ass_valid_tag_shadow():
    assert str(AssValidTagShadow(20.1)) == "\\shad20.1"


def test_ass_valid_tag_x_shadow():
    assert str(AssValidTagXShadow(20.1)) == "\\xshad20.1"


def test_ass_valid_tag_y_shadow():
    assert str(AssValidTagYShadow(20.1)) == "\\yshad20.1"
