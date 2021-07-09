import pytest

from abstracts import BoardBase
from abstracts import RequiredFig, Pattern


def test_1_req_figure():
    req_rush_r = RequiredFig(
            req_type="P", req_status={"rushed": True},
            pos=('relative_f1', (1, 0)), req_team=RequiredFig.keys['enemy']
    )


def test_2_ccp():
    req_rush_r = RequiredFig(
            req_type="P", req_status={"rushed": True},
            pos=('relative_f1', (1, 0)), req_team=RequiredFig.keys['enemy']
    )


def test_3_flip_required_object():
    req_rush_r = RequiredFig(
            req_type="P", req_status={"rushed": True},
            pos=('relative_f1', (1, 0)), req_team=RequiredFig.keys['enemy']
    )
    req_rush_r.flip_by_x()
    req_rush_r.flip_by_y()
    req_rush_r.rotate()
    req_rush_r.rotate(clockwise=False)


def test_Position_change_FLIP_ROTATE_Classic_Board():
    board = BoardBase()
    pos = Pattern('absolute', (1, 0))

    pos.flip_this_by_x(board)
    assert pos.pos == (6, 0)
    pos.flip_this_by_x(board)
    assert pos.pos == (1, 0)

    pos.flip_this_by_y(board)
    assert pos.pos == (1, 7)
    pos.flip_this_by_x(board)
    assert pos.pos == (6, 7)

    "Clockwise"
    pos = Pattern('absolute', (1, 0))
    pos.rotate_this(board)
    assert pos.pos == (0, 6)
    pos.rotate_this(board)
    assert pos.pos == (6, 7)
    pos.rotate_this(board)
    assert pos.pos == (7, 1)
    pos.rotate_this(board)
    assert pos.pos == (1, 0)

    "Counter Clockwise"
    pos = Pattern('absolute', (2, 1))
    pos.rotate_this(board, clockwise=False)
    assert pos.pos == (6, 2)
    pos.rotate_this(board, clockwise=False)
    assert pos.pos == (5, 6)
    pos.rotate_this(board, clockwise=False)
    assert pos.pos == (1, 5)
    pos.rotate_this(board, clockwise=False)
    assert pos.pos == (2, 1)


def test_Position_class_1_good():
    pos = Pattern('classic', "A5")
    pos = Pattern('absolute', "A5")

    pos = Pattern('classic', (0, 1))
    pos = Pattern('absolute', (0, 1))

    pos = Pattern('relative', (0, 1))
    pos = Pattern('relative_f1', (0, 1))
    pos = Pattern('relative_f2', (0, 1))


def test_Position_class_2_bad():
    with pytest.raises(ValueError):
        pos = Pattern('relative', "A2")
    with pytest.raises(ValueError):
        pos = Pattern('relative_f1', "A2")
    with pytest.raises(ValueError):
        pos = Pattern('relative_f2', "A2")


def test_Position_class_3_ccp_vals():
    board = BoardBase()

    check = [
            (0, 1),
            (1, 1),
            (3, 3),
            (4, 4),
            (6, 6),
            (5, 6),
            (8, 5),
    ]
    for p in check:
        pos = Pattern('relative', p)
        assert pos.get_ccp(board) == p
        pos = Pattern('relative_f1', p)
        assert pos.get_ccp(board) == p
        pos = Pattern('relative_f2', p)
        assert pos.get_ccp(board) == p


def test_Position_class_4_valid_vals():
    board = BoardBase()

    check = [
            (0, 1),
            (1, 1),
            (3, 3),
            (4, 4),
            (6, 6),
            (5, 6),
            (8, 5),
            # (None, 4),
            # (3, None),
    ]
    for p in check:
        pos = Pattern('relative', p)
        assert p == pos.get_position((0, 0), p), "This is valid move"

        pos = Pattern('relative_f1', p)
        assert p == pos.get_position((0, 0), p), "This is valid move"

        pos = Pattern('relative_f2', p)
        assert p == pos.get_position(p, (0, 0)), "This is valid move"

        pos = Pattern('absolute', p)
        assert p == pos.get_position(p, (0, 0)), "This is valid move"

        pos = Pattern('classic', p)
        assert p == pos.get_position(p, (0, 0), board=board), "This is valid move"


def test_Position_class_4_Valid_strings():
    board = BoardBase()
    check = [
            "A1",
            "A2",
            "A5",
            "A8",
            "B1",
            "B5",
            "B8",
            "G3",
            "G8",
            "H1",
            "H2",
            "H8",
    ]
    for txt in check:
        p = board.string_to_index(txt)

        pos = Pattern('absolute', txt)
        ret = pos.get_position((1, 2), (0, 0))
        assert p == ret, f"Field: {txt}, Expected: {p}, got {ret}"

        pos = Pattern('classic', txt)
        assert p == pos.get_position((1, 2), (0, 0), board=board), "This is valid move"


def test_Position_class_4_Valid_biggerBoard():
    left = 2
    bottom = 1
    board = BoardBase(left=left, right=2, bottom=bottom, top=1)
    strings = [
            "A1",
            "A2",
            "A5",
            "A8",
            "B1",
            "B5",
            "B8",
            "G3",
            "G8",
            "H1",
            "H2",
            "H8",
    ]
    indexes = [
            (0, 1),
            (1, 1),
            (3, 3),
            (4, 4),
            (6, 6),
            (5, 6),
            (8, 5),
            # (None, 4),
            # (3, None),
    ]
    for check in [strings, indexes]:
        for val in check:
            if isinstance(val, (str,)):
                p = board.string_to_index(val)
            else:
                p = val

            pos = Pattern('absolute', val)
            ret = pos.get_position((1, 2), (0, 0))
            assert p == ret, f"Field: {val}, Expected: {p}, got {ret}"

            pos = Pattern('classic', val)
            px, py = p
            p = px + left, py + bottom
            ret = pos.get_position((1, 2), (0, 0), board=board)
            assert p == ret, f"Field: {val}, Expected: {p}, got {ret}"


def test_Position_class_4_Valid_Board_Gap():
    vert = 2
    horiz = 1
    board = BoardBase(gap_vertical=vert, gap_horizontal=horiz)
    # classic = BoardBase()
    strings = [
            "A1",
            "A2",
            "A5",
            "A8",
            "B1",
            "B5",
            "B8",
            "G3",
            "G8",
            "H1",
            "H2",
            "H8",
    ]
    indexes = [
            (0, 1),
            (1, 1),
            (3, 3),
            (4, 4),
            (6, 6),
            (5, 6),
            (8, 5),
            # (None, 4),
            # (3, None),
    ]
    for check in [strings, indexes]:
        for val in check:
            if isinstance(val, (str,)):
                p = board.string_to_index(val)
            else:
                p = val

            pos = Pattern('absolute', val)
            assert p == pos.get_position((1, 2), (0, 0)), "This is valid move"

            pos = Pattern('classic', val)
            px, py = p
            if px > 3:
                px += horiz
            if py > 3:
                py += vert

            p = px, py
            ret = pos.get_position((1, 2), (0, 0), board=board)
            assert p == ret, f"Field: {val}, Expected: {p}, got {ret}"


def test_Position_class_5_Nones():
    board = BoardBase()
    pos = Pattern("Absolute", (None, 7))

    "Assert Flips"
    pos.flip_this_by_x(board)
    assert pos.pos == (None, 7)
    pos.flip_this_by_y(board)
    assert pos.pos == (None, 0)

    "Assert Rotations"
    pos = Pattern("Absolute", (None, 7))
    pos.rotate_this(board)
    assert pos.pos == (7, None)
    pos.rotate_this(board)
    assert pos.pos == (None, 0)
    pos.rotate_this(board)
    assert pos.pos == (0, None)

    "Assert counter rotation"
    pos = Pattern("Absolute", (None, 6))
    pos.rotate_this(board, clockwise=False)
    assert pos.pos == (1, None)
    pos.rotate_this(board, clockwise=False)
    assert pos.pos == (None, 1)
    pos.rotate_this(board, clockwise=False)
    assert pos.pos == (6, None)
    pos.rotate_this(board, clockwise=False)
    assert pos.pos == (None, 6)


def test_Position_class_6_():
    pass


def test_5_():
    pass


def test_6_Position_Flip_Absolte_Gap():
    raise NotImplementedError()


def test_7_():
    pass


def test_8_():
    pass


def test_9_():
    pass


def test_10_():
    pass


def test_11_():
    pass


def test_12_():
    pass


def test_13_():
    pass


def test_14_():
    pass


def test_15_():
    pass


def test_16_():
    pass


def test_17_():
    pass


def test_18_():
    pass
