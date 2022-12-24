from ass_tag_analyzer.ass_item.ass_valid_tag.ass_valid_tag_color import (
    AssValidTagPrimaryColor,
    AssValidTagSecondaryColor,
    AssValidTagOutlineColor,
    AssValidTagBackgroundColor,
)


def test_ass_valid_tag_primary_color():

    assert str(AssValidTagPrimaryColor(False, 10, 50, 150)) == "\\1c&H96320A&"
    assert str(AssValidTagPrimaryColor(True, 10, 50, 150)) == "\\c&H96320A&"


def test_ass_valid_tag_secondary_color():

    assert str(AssValidTagSecondaryColor(10, 50, 150)) == "\\2c&H96320A&"


def test_ass_valid_tag_outline_color():

    assert str(AssValidTagOutlineColor(10, 50, 150)) == "\\3c&H96320A&"


def test_ass_valid_tag_background_color():

    assert str(AssValidTagBackgroundColor(10, 50, 150)) == "\\4c&H96320A&"
