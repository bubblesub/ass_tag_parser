from ass_tag_analyzer.ass_item.ass_valid_tag import (
    AssValidTagAlpha,
    AssValidTagPrimaryAlpha,
    AssValidTagSecondaryAlpha,
    AssValidTagOutlineAlpha,
    AssValidTagBackgroundAlpha,
)


def test_ass_valid_tag_alpha():

    assert str(AssValidTagAlpha(20)) == "\\alpha&H20&"


def test_ass_valid_tag_primary_alpha():

    assert str(AssValidTagPrimaryAlpha(20)) == "\\1a&H20&"


def test_ass_valid_tag_secondary_alpha():

    assert str(AssValidTagSecondaryAlpha(20)) == "\\2a&H20&"


def test_ass_valid_tag_outline_alpha():

    assert str(AssValidTagOutlineAlpha(20)) == "\\3a&H20&"


def test_ass_valid_tag_background_alpha():

    assert str(AssValidTagBackgroundAlpha(20)) == "\\4a&H20&"
