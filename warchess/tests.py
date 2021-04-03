import pytest

from classes import Rook, Pawn, Knight, Queen, King, Bishop, ClassicGame


def test_1_():
    figs = [Pawn, Rook, King, Knight, Queen, Bishop]
    figs = [f(n) for n in range(2) for f in figs]
    for f in figs:
        assert len(f.name) > 0, f"{f}"
        assert len(f._move_patterns) > 0, f"{f}"
        assert len(f._attack_patterns) > 0, f"{f}"


def test_1_fig_attrs():
    figs = [Pawn, Rook, King, Knight, Queen, Bishop]
    figs = [f(n) for n in range(2) for f in figs]
    for f in figs:
        assert len(f.name) > 0, f"{f}"
        assert len(f._move_patterns) > 0, f"{f}"
        assert len(f._attack_patterns) > 0, f"{f}"
        assert len(f.move_patterns) > 0, f"{f}"
        assert len(f.attack_patterns) > 0, f"{f}"
        assert hasattr(f, '_specials')
        assert not hasattr(f, '_special')

        if f.specials:
            assert type(f.specials) is tuple


def test_2_():
    g = ClassicGame()
    g.board.print_table()
    g.make_move((0, 1), (0, 2))
    g.make_move((0, 6), (0, 5))

    g.make_move((1, 1), (1, 3))
    g.make_move((1, 6), (1, 4))

    with pytest.raises(ValueError) as err:
        g.make_move((0, 6), (0, 5))

    with pytest.raises(ValueError) as err:
        g.make_move((0, 1), (0, 2))


def test_3_load_fen():
    g = ClassicGame()
    g.load_fen("rnbqkbnr/pp1p1ppp/8/2pPp3/8/8/PPP1PPPP/RNBQKBNR w KQkq c6 0 3")


def test_4_enpassant():
    g = ClassicGame()
    g.load_fen("rnbqkbnr/pp1p1ppp/8/2pPp3/8/8/PPP1PPPP/RNBQKBNR w KQkq c6 0 3")
    with pytest.raises(ValueError) as err:
        g.make_move(*g.strings_to_tuple("d5", "e6"))

    assert g._is_move_valid(*g.strings_to_tuple("d5", "d6"))
    assert g._is_move_valid(*g.strings_to_tuple("d5", "c6"))


def test_5_load_fen_2():
    g = ClassicGame()
    g.load_fen("rnbqkbnr/4pp1p/1pp5/pB4p1/2Pp3P/P3P3/1P1P1PP1/RNBQ1KNR b kq c3 0 7")


def test_5_enpassant_move():
    g = ClassicGame()
    g.load_fen("rnbqkbnr/4pp1p/1pp5/pB4p1/2Pp3P/P3P3/1P1P1PP1/RNBQ1KNR b kq c3 0 7")
    g.board.print_table()
    with pytest.raises(ValueError):
        g.make_move(*g.strings_to_tuple("d5", "e6"))

    assert g._is_move_valid(*g.strings_to_tuple("d4", "d3"))
    assert g._is_move_valid(*g.strings_to_tuple("d4", "c3"))


def test_6_black_moves():
    g = ClassicGame()
    g.load_fen("rnbqkbnr/4pp1p/1pp5/pB4p1/2Pp3P/P3P3/1P1P1PP1/RNBQ1KNR b kq c3 0 7")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_tuple("c6", "b5"))
    assert g._is_move_valid(*g.strings_to_tuple("c6", "c5"))
    assert g._is_move_valid(*g.strings_to_tuple("a5", "a4"))
    assert g._is_move_valid(*g.strings_to_tuple("a8", "a7"))
    assert g._is_move_valid(*g.strings_to_tuple("a8", "a6"))
    assert not g._is_move_valid(*g.strings_to_tuple("a8", "a5"))

    assert g._is_move_valid(*g.strings_to_tuple("b8", "a6"))
    assert not g._is_move_valid(*g.strings_to_tuple("b8", "c6"))

    assert g._is_move_valid(*g.strings_to_tuple("d8", "d7"))
    assert g._is_move_valid(*g.strings_to_tuple("d8", "c7"))
    assert g._is_move_valid(*g.strings_to_tuple("d8", "d5"))
    assert not g._is_move_valid(*g.strings_to_tuple("d8", "d4"))
    assert not g._is_move_valid(*g.strings_to_tuple("d8", "d3"))

    "King"
    assert not g._is_move_valid(*g.strings_to_tuple("e8", "f8"))
    assert not g._is_move_valid(*g.strings_to_tuple("e8", "e7"))
    assert not g._is_move_valid(*g.strings_to_tuple("e8", "f7"))


def test_7_white_moves():
    g = ClassicGame()
    g.load_fen("rnbqk2r/5nbp/1pp5/pB3pp1/2Ppp2P/PPN1P2R/1BQPNPP1/R3K3 w kq - 1 14")
    g.board.print_table()

    "W King"
    assert g._is_move_valid(*g.strings_to_tuple("e1", "d1"))
    assert g._is_move_valid(*g.strings_to_tuple("e1", "f1"))

    assert not g._is_move_valid(*g.strings_to_tuple("e1", "d2"))
    assert not g._is_move_valid(*g.strings_to_tuple("e1", "e2"))
    assert not g._is_move_valid(*g.strings_to_tuple("e1", "f2"))
    assert not g._is_move_valid(*g.strings_to_tuple("e1", "c1"))
    assert not g._is_move_valid(*g.strings_to_tuple("e1", "g1"))

    "Knight"
    assert g._is_move_valid(*g.strings_to_tuple("e2", "d4"))
    assert g._is_move_valid(*g.strings_to_tuple("e2", "f4"))
    assert not g._is_move_valid(*g.strings_to_tuple("e2", "e4"))
    assert not g._is_move_valid(*g.strings_to_tuple("e2", "e3"))


def test_8_pawn():
    g = ClassicGame()
    g.load_fen("rnbqkbr1/p1p5/1p6/2npPppp/5PP1/P1P4P/1P1P4/RNBQKB1R w KQq - 1 12")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_tuple("a3", "a4"))
    assert not g._is_move_valid(*g.strings_to_tuple("a3", "a5"))
    assert not g._is_move_valid(*g.strings_to_tuple("a3", "b4"))
    assert not g._is_move_valid(*g.strings_to_tuple("c3", "b4"))
    assert not g._is_move_valid(*g.strings_to_tuple("c3", "d4"))

    assert g._is_move_valid(*g.strings_to_tuple("f4", "g5"))
    assert not g._is_move_valid(*g.strings_to_tuple("f4", "f5"))


def test_9_pawn_black():
    g = ClassicGame()
    g.load_fen("rnbqkbr1/p1p5/1p6/2npPppp/5PP1/P1P4P/1P1P3R/RNBQKB2 b Qq - 2 12")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_tuple("f5", "g4"))
    assert g._is_move_valid(*g.strings_to_tuple("h5", "g4"))
    assert g._is_move_valid(*g.strings_to_tuple("h5", "h4"))
    assert g._is_move_valid(*g.strings_to_tuple("a7", "a6"))
    assert g._is_move_valid(*g.strings_to_tuple("a7", "a5"))
    assert g._is_move_valid(*g.strings_to_tuple("b6", "b5"))

    assert not g._is_move_valid(*g.strings_to_tuple("f5", "f4"))
    assert not g._is_move_valid(*g.strings_to_tuple("f5", "e4"))
    assert not g._is_move_valid(*g.strings_to_tuple("g5", "g4"))
    assert not g._is_move_valid(*g.strings_to_tuple("c7", "b6"))


def test_9_pawn_black2():
    g = ClassicGame()
    g.load_fen("rnbqkbr1/p1p5/1p6/2npPppp/5PP1/P1P4P/1P1P3R/RNBQKB2 b Qq - 2 12")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_tuple("c7", "c6"))

    assert not g._is_move_valid(*g.strings_to_tuple("c7", "c5"))
    assert not g._is_move_valid(*g.strings_to_tuple("c7", "b5"))
    assert not g._is_move_valid(*g.strings_to_tuple("c7", "b6"))
    assert not g._is_move_valid(*g.strings_to_tuple("c7", "d5"))
    assert not g._is_move_valid(*g.strings_to_tuple("c7", "d6"))


def test_9_pawn_white_2():
    g = ClassicGame()
    g.load_fen("rnbqkbr1/p1p5/1p6/2PpPppp/4nPP1/P6P/1P1P3R/RNBQKB2 w Qq - 1 15")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_tuple("c5", "c6"))
    assert g._is_move_valid(*g.strings_to_tuple("c5", "b6"))
    assert not g._is_move_valid(*g.strings_to_tuple("c5", "d6"))


def test_10_castle_w_1():
    g = ClassicGame()
    g.load_fen("r3kbnr/pp2pppp/2pp4/2nq4/2P5/BPN1PN2/P2P1PPP/R3K2R w KQkq - 0 13")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_tuple("e1", "g1"))
    assert g._is_move_valid(*g.strings_to_tuple("e1", "c1"))
    assert g._is_move_valid(*g.strings_to_tuple("e1", "d1"))
    assert g._is_move_valid(*g.strings_to_tuple("e1", "f1"))


def test_10_castle_w_2_check():
    g = ClassicGame()
    g.load_fen("r3kbnr/pp2pppp/2ppq3/3Q4/2P5/BPNnPN2/P2P1PPP/R3K2R w KQkq - 3 13")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_tuple("e1", "d1"))
    assert g._is_move_valid(*g.strings_to_tuple("e1", "f1"))
    assert g._is_move_valid(*g.strings_to_tuple("e1", "e2"))

    assert not g._is_move_valid(*g.strings_to_tuple("e1", "c1")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("e1", "g1")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("e1", "d2")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("e1", "f2")), "Not valid move"


def test_10_castle_w_3_blockade():
    g = ClassicGame()
    g.load_fen("r3kbnr/pp2pppp/2ppq3/3Q4/2P5/BnN1PN2/P2P1PPP/R3K2R w KQkq - 0 13")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_tuple("e1", "d1"))
    assert g._is_move_valid(*g.strings_to_tuple("e1", "f1"))
    assert g._is_move_valid(*g.strings_to_tuple("e1", "e2"))

    assert g._is_move_valid(*g.strings_to_tuple("e1", "g1"))
    assert not g._is_move_valid(*g.strings_to_tuple("e1", "c1")), "Not valid move"


def test_10_castle_w_move():
    g = ClassicGame()
    g.load_fen("r3kbnr/pp2pppp/2ppq3/2n5/2P5/BPNQPN2/P2P1PPP/R3K2R w KQkq - 1 12")
    g.board.print_table()

    g.make_move(*g.strings_to_tuple("e1", "g1"))

    f1 = g.strings_to_tuple("g1")[0]
    f2 = g.strings_to_tuple("f1")[0]

    assert isinstance(g.board.get(f1), King)
    assert isinstance(g.board.get(f2), Rook)


def test_10_castle_w_move2():
    g = ClassicGame()
    g.load_fen("r3kbnr/pp2pppp/2ppq3/2n5/2P5/BPNQPN2/P2P1PPP/R3K2R w KQkq - 1 12")
    g.board.print_table()

    g.make_move(*g.strings_to_tuple("e1", "c1"))

    f1 = g.strings_to_tuple("c1")[0]
    f2 = g.strings_to_tuple("d1")[0]

    assert isinstance(g.board.get(f1), King)
    assert isinstance(g.board.get(f2), Rook)


def test_11_white_bishop():
    g = ClassicGame()
    g.load_fen("2kr1bn1/pp3ppN/2pB4/2n1p3/6q1/1P2P3/P2P1PPP/2KR3R w - - 0 19")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_tuple("d6", "c5"))
    assert g._is_move_valid(*g.strings_to_tuple("d6", "c7"))
    assert g._is_move_valid(*g.strings_to_tuple("d6", "b8"))
    assert g._is_move_valid(*g.strings_to_tuple("d6", "e7"))
    assert g._is_move_valid(*g.strings_to_tuple("d6", "f8"))
    assert g._is_move_valid(*g.strings_to_tuple("d6", "e5"))

    assert not g._is_move_valid(*g.strings_to_tuple("d6", "b4"))
    assert not g._is_move_valid(*g.strings_to_tuple("d6", "a3"))
    assert not g._is_move_valid(*g.strings_to_tuple("d6", "c6"))
    assert not g._is_move_valid(*g.strings_to_tuple("d6", "e6"))
    assert not g._is_move_valid(*g.strings_to_tuple("d6", "f4"))
    assert not g._is_move_valid(*g.strings_to_tuple("d6", "g3"))
    assert not g._is_move_valid(*g.strings_to_tuple("d6", "h2"))
    assert not g._is_move_valid(*g.strings_to_tuple("d6", "d7"))
    assert not g._is_move_valid(*g.strings_to_tuple("d6", "d8"))
    assert not g._is_move_valid(*g.strings_to_tuple("d6", "d5"))


def test_11_white_bishop_2():
    g = ClassicGame()
    g.load_fen("2kr1bn1/pp3ppn/2p5/2n1b1q1/8/1p2p3/p2p1ppp/2kr3r w - - 1 20")
    g.board.print_table()

    assert not g._is_move_valid(*g.strings_to_tuple("e5", "h2"))


def test_12_knights():
    g = ClassicGame()
    g.load_fen("rn1qkb1r/pppbpNpp/8/3p4/2n1P3/2N5/PPPP1P1P/R1BQKB1R w KQkq - 1 7")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_tuple("c3", "b5"))
    assert g._is_move_valid(*g.strings_to_tuple("c3", "d5"))
    assert g._is_move_valid(*g.strings_to_tuple("c3", "b1"))
    assert g._is_move_valid(*g.strings_to_tuple("f7", "d8"))
    assert g._is_move_valid(*g.strings_to_tuple("f7", "d6"))
    assert g._is_move_valid(*g.strings_to_tuple("f7", "e5"))
    assert g._is_move_valid(*g.strings_to_tuple("f7", "h8"))
    assert g._is_move_valid(*g.strings_to_tuple("f7", "h6"))
    assert g._is_move_valid(*g.strings_to_tuple("f7", "g5"))

    assert not g._is_move_valid(*g.strings_to_tuple("c3", "e4"))
    assert not g._is_move_valid(*g.strings_to_tuple("c3", "d1"))
    assert not g._is_move_valid(*g.strings_to_tuple("c3", "a2"))


def test_13_white_queen():
    g = ClassicGame()
    g.load_fen("rnbqkbnr/pppp2pp/5p2/4p3/3QPP2/3B1N2/PPPPB1PP/RN2K2R w KQkq - 0 1")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_tuple("d4", "d5"))
    assert g._is_move_valid(*g.strings_to_tuple("d4", "d6"))
    assert g._is_move_valid(*g.strings_to_tuple("d4", "d7"))
    assert not g._is_move_valid(*g.strings_to_tuple("d4", "d8"))

    assert g._is_move_valid(*g.strings_to_tuple("d4", "c5"))
    assert g._is_move_valid(*g.strings_to_tuple("d4", "b6"))
    assert g._is_move_valid(*g.strings_to_tuple("d4", "a7"))

    assert g._is_move_valid(*g.strings_to_tuple("d4", "c4"))
    assert g._is_move_valid(*g.strings_to_tuple("d4", "b4"))
    assert g._is_move_valid(*g.strings_to_tuple("d4", "a4"))
    assert not g._is_move_valid(*g.strings_to_tuple("d4", "e4"))
    assert not g._is_move_valid(*g.strings_to_tuple("d4", "f4"))
    assert not g._is_move_valid(*g.strings_to_tuple("d4", "d3"))

    assert g._is_move_valid(*g.strings_to_tuple("d4", "c3"))
    assert g._is_move_valid(*g.strings_to_tuple("d4", "e3"))
    assert g._is_move_valid(*g.strings_to_tuple("d4", "f2"))
    assert g._is_move_valid(*g.strings_to_tuple("d4", "g1"))
    assert g._is_move_valid(*g.strings_to_tuple("d4", "c3"))
    assert not g._is_move_valid(*g.strings_to_tuple("d4", "b2"))


def test_14_move_and_check():
    g = ClassicGame()
    g.load_fen("kp2q3/pq5q/6P1/q2QNP2/q1QBKR1q/5N2/2N1R1N1/1q2q2q w - - 0 1")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_tuple("c4", "b4")), "Valid move"
    assert g._is_move_valid(*g.strings_to_tuple("c4", "a4")), "Valid move"
    assert g._is_move_valid(*g.strings_to_tuple("c4", "c5")), "Valid move"
    assert g._is_move_valid(*g.strings_to_tuple("c4", "c3")), "Valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("c4", "a2")), "Not valid move"

    assert g._is_move_valid(*g.strings_to_tuple("d5", "c6")), "Valid move"
    assert g._is_move_valid(*g.strings_to_tuple("d5", "b7")), "Valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("d5", "a8")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("d5", "d6")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("d5", "c5")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("d5", "e4")), "Not valid move"

    assert not g._is_move_valid(*g.strings_to_tuple("c2", "e1")), "Not valid move"

    assert g._is_move_valid(*g.strings_to_tuple("f4", "h4")), "Valid move"
    assert g._is_move_valid(*g.strings_to_tuple("f4", "g4")), "Valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("f4", "f3")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("f4", "f5")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("f4", "f2")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("f4", "f1")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("f4", "e4")), "Not valid move"

    assert g._is_move_valid(*g.strings_to_tuple("f3", "h4")), "Valid move"
    assert g._is_move_valid(*g.strings_to_tuple("f3", "e1")), "Valid move"
    assert g._is_move_valid(*g.strings_to_tuple("f3", "h2")), "Valid move"

    assert g._is_move_valid(*g.strings_to_tuple("g2", "h4")), "Valid move"
    assert g._is_move_valid(*g.strings_to_tuple("g2", "e1")), "Valid move"

    assert g._is_move_valid(*g.strings_to_tuple("e2", "e1")), "Valid move"
    assert g._is_move_valid(*g.strings_to_tuple("e2", "e3")), "Valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("e2", "f1")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("e2", "d1")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("e2", "e4")), "Not valid move"

    assert not g._is_move_valid(*g.strings_to_tuple("c2", "e4")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("c2", "e1")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("c2", "e3")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_tuple("c2", "b4")), "Not valid move"


def test_15_under_threat():
    g = ClassicGame()
    g.load_fen("r3kbnr/pp2pppp/2ppq3/2n5/2P5/BPNQPN2/P2P1PPP/R3K2R w KQkq - 1 12")
    g.board.print_table()

    assert g.under_threat(*g.strings_to_tuple("c4"))
    assert g.under_threat(*g.strings_to_tuple("e3"))
    assert g.under_threat(*g.strings_to_tuple("d6"))
    assert g.under_threat(*g.strings_to_tuple("c5"))

    assert not g.under_threat(*g.strings_to_tuple("e1"))
    assert not g.under_threat(*g.strings_to_tuple("h1"))
    assert not g.under_threat(*g.strings_to_tuple("a1"))
    assert not g.under_threat(*g.strings_to_tuple("g8"))
    assert not g.under_threat(*g.strings_to_tuple("g8"))


def test_15_under_threat_2():
    g = ClassicGame()
    g.load_fen("r3r1k1/pppb1ppp/5n2/3P4/2P5/2NB1P2/PP1q3P/2KR1R2 w - - 0 15")
    g.board.print_table()

    moves = [
            'h1', 'g1', 'e1', 'e2', 'e4', 'c1', 'b1', 'c2', 'd2', 'd1', 'd5', 'e4',
            'e6', 'f3', 'g4', 'g3', 'a3', 'b3', 'c6', 'e6', 'f2', 'a4', 'b5', 'f5',
            'g6', 'h7', 'f3'

    ]
    for mv in moves:
        assert g.under_threat(*g.strings_to_tuple(mv), defending=1), f"White is not attacking {mv}"


def test_16_counter_checks():
    g = ClassicGame()
    g.load_fen("r3r1k1/pppb1ppp/5n2/3P4/2P5/2NB1P2/PP1q3P/2KR1R2 w - - 0 15")
    g.board.print_table()

    moves = [
            ('c1', 'b1'),
            ('d1', 'd2'),
            ('c1', 'd2'),
    ]
    for pair in moves:
        assert g._is_move_valid(*g.strings_to_tuple(*pair)), "This is not white valid move"

    moves = [
            ('f1', 'f2'),
            ('f1', 'e1'),
            ('d3', 'c2'),
            ('c3', 'b2'),
            ('d3', 'h7'),
            ('f3', 'f4'),
            ('f3', 'f5'),
            ('d5', 'd6'),
            ('c4', 'c5'),
            ('c4', 'c6'),
            ('d1', 'c2'),
            ('d1', 'e1'),
            ('d1', 'e2'),
            ('c1', 'b2'),
    ]
    for pair in moves:
        assert not g._is_move_valid(*g.strings_to_tuple(*pair)), f"This move is invalid for white: {pair}"


def test_17_loading_fen_color_check():
    g = ClassicGame()
    g.load_fen("r3kbnr/pp2pppp/2ppq3/3Q4/2P5/BPNnPN2/P2P1PPP/R3K2R w KQkq - 3 13")
    g.board.print_table()

    black_poses = [
            "d3",
            "a8",
            "a7",
            "e6",
            "d6",
            "c6",
            "e8",
            "f8",
            "g8",
            "h7",
            "f7",
            "g7",
            "h7",
            "c6",
    ]
    for pos in black_poses:
        assert g.board.get(*g.strings_to_tuple(pos)).team == 1, f"Fig on {pos} is black!"
    white_poses = [
            "e1",
            "a1",
            "h1",
            "a3",
            "a2",
            "b3",
            "c3",
            "c4",
            "d2",
            "d5",
            "e3",
            "f2",
            "f3",
            "g2",
            "h2",
    ]
    for pos in white_poses:
        assert g.board.get(*g.strings_to_tuple(pos)).team == 0, f"Fig on {pos} is white!"


def test_18_():
    pass
