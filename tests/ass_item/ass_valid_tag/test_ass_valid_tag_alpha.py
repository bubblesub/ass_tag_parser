from ass_tag_analyzer.ass_item.ass_valid_tag import (
    AssValidTagAlpha,
    AssValidTagPrimaryAlpha,
    AssValidTagSecondaryAlpha,
    AssValidTagOutlineAlpha,
    AssValidTagBackgroundAlpha,
)


def test_ass_valid_tag_alpha():

    assert str(AssValidTagAlpha(254)) == "\\alpha&HFE&"


def test_ass_valid_tag_primary_alpha():

    assert str(AssValidTagPrimaryAlpha(254)) == "\\1a&HFE&"


def test_ass_valid_tag_secondary_alpha():

    assert str(AssValidTagSecondaryAlpha(254)) == "\\2a&HFE&"


def test_ass_valid_tag_outline_alpha():

    assert str(AssValidTagOutlineAlpha(254)) == "\\3a&HFE&"


def test_ass_valid_tag_background_alpha():

    assert str(AssValidTagBackgroundAlpha(254)) == "\\4a&HFE&"
