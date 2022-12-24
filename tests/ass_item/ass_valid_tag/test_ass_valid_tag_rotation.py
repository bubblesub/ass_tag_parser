from ass_tag_analyzer.ass_item.ass_valid_tag.ass_valid_tag_rotation import (
    AssValidTagXRotation,
    AssValidTagYRotation,
    AssValidTagZRotation,
)


def test_ass_valid_tag_x_rotation():
    assert str(AssValidTagXRotation(20.1)) == "\\frx20.1"


def test_ass_valid_tag_y_rotation():
    assert str(AssValidTagYRotation(20.1)) == "\\fry20.1"


def test_ass_valid_tag_z_rotation():
    assert str(AssValidTagZRotation(False, 20.1)) == "\\frz20.1"
    assert str(AssValidTagZRotation(True, 20.1)) == "\\fr20.1"
