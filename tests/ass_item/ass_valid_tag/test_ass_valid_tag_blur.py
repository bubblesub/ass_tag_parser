from ass_tag_analyzer.ass_item.ass_valid_tag import (
    AssValidTagBlurEdges,
    AssValidTagBlurEdgesGauss,
)


def test_ass_valid_tag_blur_edges():

    assert str(AssValidTagBlurEdges(20)) == "\\be20"


def test_ass_valid_tag_blur_edges_gauss():

    assert str(AssValidTagBlurEdgesGauss(20)) == "\\blur20"
    assert str(AssValidTagBlurEdgesGauss(-20)) == "\\blur0"
