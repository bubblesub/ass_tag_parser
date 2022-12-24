from ass_tag_analyzer.ass_item.ass_valid_tag.ass_valid_tag_shear import (
    AssValidTagXShear,
    AssValidTagYShear,
)


def test_ass_valid_tag_x_shear():
    assert str(AssValidTagXShear(20.1)) == "\\fax20.1"


def test_ass_valid_tag_y_shear():
    assert str(AssValidTagYShear(20.1)) == "\\fay20.1"
