from ass_tag_analyzer.ass_item.ass_valid_tag.ass_valid_tag_border import (
    AssValidTagBorder,
    AssValidTagXBorder,
    AssValidTagYBorder,
)


def test_ass_valid_tag_border():

    assert str(AssValidTagBorder(20)) == "\\bord20"
    assert str(AssValidTagBorder(-20)) == "\\bord0"


def test_ass_valid_tag_x_border():

    assert str(AssValidTagXBorder(20)) == "\\xbord20"
    assert str(AssValidTagXBorder(-20)) == "\\xbord0"


def test_ass_valid_tag_y_border():

    assert str(AssValidTagYBorder(20)) == "\\ybord20"
    assert str(AssValidTagYBorder(-20)) == "\\ybord0"
