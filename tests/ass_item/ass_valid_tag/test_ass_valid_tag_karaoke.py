from ass_tag_analyzer.ass_item.ass_valid_tag.ass_valid_tag_karaoke import (
    AssValidTagKaraoke,
    AssValidTagKaraokeFill,
    AssValidTagKaraokeOutline,
)


def test_ass_valid_tag_karaoke():
    assert str(AssValidTagKaraoke(200)) == "\\k20"


def test_ass_valid_tag_karaoke_fill():
    assert str(AssValidTagKaraokeFill(True, 200)) == "\\K20"
    assert str(AssValidTagKaraokeFill(False, 200)) == "\\kf20"


def test_ass_valid_tag_karaoke_outline():
    assert str(AssValidTagKaraokeOutline(200)) == "\\ko20"
