from ass_tag_analyzer.ass_item.ass_valid_tag.ass_valid_tag_wrap_style import (
    AssValidTagWrapStyle,
    WrapStyle,
)


def test_ass_valid_tag_wrap_style():
    assert str(AssValidTagWrapStyle(WrapStyle(2))) == "\\q2"
