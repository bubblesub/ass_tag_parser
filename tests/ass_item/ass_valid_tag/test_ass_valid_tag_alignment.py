from ass_tag_analyzer.ass_item.ass_valid_tag.ass_valid_tag_alignment import (
    AssValidTagAlignment,
    Alignment,
    LegacyAlignment,
)
import pytest


def test_ass_valid_tag_font_alignment():
    assert str(AssValidTagAlignment(Alignment(5))) == "\\an5"
    assert str(AssValidTagAlignment(LegacyAlignment(10), True)) == "\\a10"

    with pytest.raises(ValueError) as exc_info:
        AssValidTagAlignment(LegacyAlignment(5))
    assert str(exc_info.value) == "alignment need to be an Alignment instance"

    with pytest.raises(ValueError) as exc_info:
        AssValidTagAlignment(Alignment(5), True)
    assert str(exc_info.value) == "alignment need to be an LegacyAlignment instance"

    an_alignment = AssValidTagAlignment(Alignment(5))
    an_alignment.convert_to_a_tag()
    assert str(an_alignment) == "\\a10"

    an_alignment.convert_to_an_tag()
    assert str(an_alignment) == "\\an5"
