from ass_tag_analyzer.ass_item.ass_valid_tag.ass_valid_tag_fade import (
    AssValidTagFade,
    AssValidTagFadeComplex,
)


def test_ass_valid_tag_fade():

    assert str(AssValidTagFade(0, 20)) == "\\fad(0,20)"


def test_ass_valid_tag_fade_complex():

    assert str(AssValidTagFadeComplex(1, 2, 3, 4, 5, 6, 7)) == "\\fade(1,2,3,4,5,6,7)"
