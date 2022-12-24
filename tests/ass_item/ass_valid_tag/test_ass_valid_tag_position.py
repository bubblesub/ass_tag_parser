from ass_tag_analyzer.ass_item.ass_valid_tag.ass_valid_tag_position import (
    AssValidTagMove,
    AssValidTagPosition,
)


def test_ass_valid_tag_move():
    assert str(AssValidTagMove(0, 1, 2, 3, 5, 4)) == "\\move(0,1,2,3,4,5)"
    assert str(AssValidTagMove(0, 1, 2, 3, 4, 5)) == "\\move(0,1,2,3,4,5)"
    assert str(AssValidTagMove(0, 1, 2, 3, time1=4)) == "\\move(0,1,2,3)"
    assert str(AssValidTagMove(0, 1, 2, 3, time2=5)) == "\\move(0,1,2,3)"
    assert str(AssValidTagMove(0, 1, 2, 3)) == "\\move(0,1,2,3)"

    move_tag = AssValidTagMove(0, 1, 2, 3, 4, 5)
    move_tag.time1 = 6
    assert str(move_tag) == "\\move(0,1,2,3,5,6)"

    move_tag = AssValidTagMove(0, 1, 2, 3, 4, 5)
    move_tag.time2 = 3
    assert str(move_tag) == "\\move(0,1,2,3,3,4)"


def test_ass_valid_tag_position():
    assert str(AssValidTagPosition(0, 1)) == "\\pos(0,1)"
