from ass_tag_analyzer.ass_item.ass_valid_tag.ass_valid_tag_clip import (
    AssValidTagClipRectangle,
    AssValidTagClipVector,
)


def test_ass_valid_tag_clip_rectangle():

    assert str(AssValidTagClipRectangle(True, 20, 20, 20, 20)) == "\\iclip(20,20,20,20)"
    assert str(AssValidTagClipRectangle(False, 20, 20, 20, 20)) == "\\clip(20,20,20,20)"


def test_ass_valid_tag_clip_vector():
    assert (
        str(AssValidTagClipVector(True, "m 187 365 l 215 341 249 301", 20))
        == "\\iclip(20,m 187 365 l 215 341 249 301)"
    )
    assert (
        str(AssValidTagClipVector(True, "m 187 365 l 215 341 249 301"))
        == "\\iclip(m 187 365 l 215 341 249 301)"
    )
    assert (
        str(AssValidTagClipVector(False, "m 187 365 l 215 341 249 301"))
        == "\\clip(m 187 365 l 215 341 249 301)"
    )
