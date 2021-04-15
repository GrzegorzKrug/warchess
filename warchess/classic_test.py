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
    g.new_game()
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
        g.make_move(g.strings_to_ints("d5", "e6"))

    assert g._is_move_valid(*g.strings_to_ints("d5", "d6"))
    assert g._is_move_valid(*g.strings_to_ints("d5", "c6"))


def test_5_load_fen_2():
    g = ClassicGame()
    g.load_fen("rnbqkbnr/4pp1p/1pp5/pB4p1/2Pp3P/P3P3/1P1P1PP1/RNBQ1KNR b kq c3 0 7")


def test_5_enpassant_move():
    g = ClassicGame()
    g.load_fen("rnbqkbnr/4pp1p/1pp5/pB4p1/2Pp3P/P3P3/1P1P1PP1/RNBQ1KNR b kq c3 0 7")
    g.board.print_table()
    with pytest.raises(ValueError):
        g.make_move(g.strings_to_ints("d5", "e6"))

    assert g._is_move_valid(*g.strings_to_ints("d4", "d3"))
    assert g._is_move_valid(*g.strings_to_ints("d4", "c3"))


def test_6_black_moves():
    g = ClassicGame()
    g.load_fen("rnbqkbnr/4pp1p/1pp5/pB4p1/2Pp3P/P3P3/1P1P1PP1/RNBQ1KNR b kq c3 0 7")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_ints("c6", "b5"))
    assert g._is_move_valid(*g.strings_to_ints("c6", "c5"))
    assert g._is_move_valid(*g.strings_to_ints("a5", "a4"))
    assert g._is_move_valid(*g.strings_to_ints("a8", "a7"))
    assert g._is_move_valid(*g.strings_to_ints("a8", "a6"))
    assert not g._is_move_valid(*g.strings_to_ints("a8", "a5"))

    assert g._is_move_valid(*g.strings_to_ints("b8", "a6"))
    assert not g._is_move_valid(*g.strings_to_ints("b8", "c6"))

    assert g._is_move_valid(*g.strings_to_ints("d8", "d7"))
    assert g._is_move_valid(*g.strings_to_ints("d8", "c7"))
    assert g._is_move_valid(*g.strings_to_ints("d8", "d5"))
    assert not g._is_move_valid(*g.strings_to_ints("d8", "d4"))
    assert not g._is_move_valid(*g.strings_to_ints("d8", "d3"))

    "King"
    assert not g._is_move_valid(*g.strings_to_ints("e8", "f8"))
    assert not g._is_move_valid(*g.strings_to_ints("e8", "e7"))
    assert not g._is_move_valid(*g.strings_to_ints("e8", "f7"))


def test_7_white_moves():
    g = ClassicGame()
    g.load_fen("rnbqk2r/5nbp/1pp5/pB3pp1/2Ppp2P/PPN1P2R/1BQPNPP1/R3K3 w kq - 1 14")
    g.board.print_table()

    "W King"
    assert g._is_move_valid(*g.strings_to_ints("e1", "d1"))
    assert g._is_move_valid(*g.strings_to_ints("e1", "f1"))

    assert not g._is_move_valid(*g.strings_to_ints("e1", "d2"))
    assert not g._is_move_valid(*g.strings_to_ints("e1", "e2"))
    assert not g._is_move_valid(*g.strings_to_ints("e1", "f2"))
    assert not g._is_move_valid(*g.strings_to_ints("e1", "c1"))
    assert not g._is_move_valid(*g.strings_to_ints("e1", "g1"))

    "Knight"
    assert g._is_move_valid(*g.strings_to_ints("e2", "d4"))
    assert g._is_move_valid(*g.strings_to_ints("e2", "f4"))
    assert not g._is_move_valid(*g.strings_to_ints("e2", "e4"))
    assert not g._is_move_valid(*g.strings_to_ints("e2", "e3"))


def test_8_pawn():
    g = ClassicGame()
    g.load_fen("rnbqkbr1/p1p5/1p6/2npPppp/5PP1/P1P4P/1P1P4/RNBQKB1R w KQq - 1 12")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_ints("a3", "a4"))
    assert not g._is_move_valid(*g.strings_to_ints("a3", "a5"))
    assert not g._is_move_valid(*g.strings_to_ints("a3", "b4"))
    assert not g._is_move_valid(*g.strings_to_ints("c3", "b4"))
    assert not g._is_move_valid(*g.strings_to_ints("c3", "d4"))

    assert g._is_move_valid(*g.strings_to_ints("f4", "g5"))
    assert not g._is_move_valid(*g.strings_to_ints("f4", "f5"))


def test_9_pawn_black():
    g = ClassicGame()
    g.load_fen("rnbqkbr1/p1p5/1p6/2npPppp/5PP1/P1P4P/1P1P3R/RNBQKB2 b Qq - 2 12")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_ints("f5", "g4"))
    assert g._is_move_valid(*g.strings_to_ints("h5", "g4"))
    assert g._is_move_valid(*g.strings_to_ints("h5", "h4"))
    assert g._is_move_valid(*g.strings_to_ints("a7", "a6"))
    assert g._is_move_valid(*g.strings_to_ints("a7", "a5"))
    assert g._is_move_valid(*g.strings_to_ints("b6", "b5"))

    assert not g._is_move_valid(*g.strings_to_ints("f5", "f4"))
    assert not g._is_move_valid(*g.strings_to_ints("f5", "e4"))
    assert not g._is_move_valid(*g.strings_to_ints("g5", "g4"))
    assert not g._is_move_valid(*g.strings_to_ints("c7", "b6"))


def test_9_pawn_black2():
    g = ClassicGame()
    g.load_fen("rnbqkbr1/p1p5/1p6/2npPppp/5PP1/P1P4P/1P1P3R/RNBQKB2 b Qq - 2 12")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_ints("c7", "c6"))

    assert not g._is_move_valid(*g.strings_to_ints("c7", "c5"))
    assert not g._is_move_valid(*g.strings_to_ints("c7", "b5"))
    assert not g._is_move_valid(*g.strings_to_ints("c7", "b6"))
    assert not g._is_move_valid(*g.strings_to_ints("c7", "d5"))
    assert not g._is_move_valid(*g.strings_to_ints("c7", "d6"))


def test_9_pawn_white_2():
    g = ClassicGame()
    g.load_fen("rnbqkbr1/p1p5/1p6/2PpPppp/4nPP1/P6P/1P1P3R/RNBQKB2 w Qq - 1 15")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_ints("c5", "c6"))
    assert g._is_move_valid(*g.strings_to_ints("c5", "b6"))
    assert not g._is_move_valid(*g.strings_to_ints("c5", "d6"))


def test_10_castle_w_1():
    g = ClassicGame()
    g.load_fen("r3kbnr/pp2pppp/2pp4/2nq4/2P5/BPN1PN2/P2P1PPP/R3K2R w KQkq - 0 13")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_ints("e1", "g1"))
    assert g._is_move_valid(*g.strings_to_ints("e1", "c1"))
    assert g._is_move_valid(*g.strings_to_ints("e1", "d1"))
    assert g._is_move_valid(*g.strings_to_ints("e1", "f1"))


def test_10_castle_w_2_check():
    g = ClassicGame()
    g.load_fen("r3kbnr/pp2pppp/2ppq3/3Q4/2P5/BPNnPN2/P2P1PPP/R3K2R w KQkq - 3 13")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_ints("e1", "d1"))
    assert g._is_move_valid(*g.strings_to_ints("e1", "f1"))
    assert g._is_move_valid(*g.strings_to_ints("e1", "e2"))

    assert not g._is_move_valid(*g.strings_to_ints("e1", "c1")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_ints("e1", "g1")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_ints("e1", "d2")), "Not valid move"
    assert not g._is_move_valid(*g.strings_to_ints("e1", "f2")), "Not valid move"


def test_10_castle_w_3_blockade():
    g = ClassicGame()
    g.load_fen("r3kbnr/pp2pppp/2ppq3/3Q4/2P5/BnN1PN2/P2P1PPP/R3K2R w KQkq - 0 13")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_ints("e1", "d1"))
    assert g._is_move_valid(*g.strings_to_ints("e1", "f1"))
    assert g._is_move_valid(*g.strings_to_ints("e1", "e2"))

    assert g._is_move_valid(*g.strings_to_ints("e1", "g1"))
    assert not g._is_move_valid(*g.strings_to_ints("e1", "c1")), "Not valid move"


def test_10_castle_w_move():
    g = ClassicGame()
    g.load_fen("r3kbnr/pp2pppp/2ppq3/2n5/2P5/BPNQPN2/P2P1PPP/R3K2R w KQkq - 1 12")
    g.board.print_table()

    g.make_move(g.strings_to_ints("e1", "g1"))

    f1 = g.strings_to_ints("g1")[0]
    f2 = g.strings_to_ints("f1")[0]

    assert isinstance(g.board.get(f1), King)
    assert isinstance(g.board.get(f2), Rook)


def test_10_castle_w_move2():
    g = ClassicGame()
    g.load_fen("r3kbnr/pp2pppp/2ppq3/2n5/2P5/BPNQPN2/P2P1PPP/R3K2R w KQkq - 1 12")
    g.board.print_table()

    g.make_move(g.strings_to_ints("e1", "c1"))

    f1 = g.strings_to_ints("c1")[0]
    f2 = g.strings_to_ints("d1")[0]

    assert isinstance(g.board.get(f1), King)
    assert isinstance(g.board.get(f2), Rook)


def test_11_white_bishop():
    g = ClassicGame()
    g.load_fen("2kr1bn1/pp3ppN/2pB4/2n1p3/6q1/1P2P3/P2P1PPP/2KR3R w - - 0 19")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_ints("d6", "c5"))
    assert g._is_move_valid(*g.strings_to_ints("d6", "c7"))
    assert g._is_move_valid(*g.strings_to_ints("d6", "b8"))
    assert g._is_move_valid(*g.strings_to_ints("d6", "e7"))
    assert g._is_move_valid(*g.strings_to_ints("d6", "f8"))
    assert g._is_move_valid(*g.strings_to_ints("d6", "e5"))

    assert not g._is_move_valid(*g.strings_to_ints("d6", "b4"))
    assert not g._is_move_valid(*g.strings_to_ints("d6", "a3"))
    assert not g._is_move_valid(*g.strings_to_ints("d6", "c6"))
    assert not g._is_move_valid(*g.strings_to_ints("d6", "e6"))
    assert not g._is_move_valid(*g.strings_to_ints("d6", "f4"))
    assert not g._is_move_valid(*g.strings_to_ints("d6", "g3"))
    assert not g._is_move_valid(*g.strings_to_ints("d6", "h2"))
    assert not g._is_move_valid(*g.strings_to_ints("d6", "d7"))
    assert not g._is_move_valid(*g.strings_to_ints("d6", "d8"))
    assert not g._is_move_valid(*g.strings_to_ints("d6", "d5"))


def test_11_white_bishop_2():
    g = ClassicGame()
    g.load_fen("2kr1bn1/pp3ppn/2p5/2n1b1q1/8/1p2p3/p2p1ppp/2kr3r w - - 1 20")
    g.board.print_table()

    assert not g._is_move_valid(*g.strings_to_ints("e5", "h2"))


def test_12_knights():
    g = ClassicGame()
    g.load_fen("rn1qkb1r/pppbpNpp/8/3p4/2n1P3/2N5/PPPP1P1P/R1BQKB1R w KQkq - 1 7")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_ints("c3", "b5"))
    assert g._is_move_valid(*g.strings_to_ints("c3", "d5"))
    assert g._is_move_valid(*g.strings_to_ints("c3", "b1"))
    assert g._is_move_valid(*g.strings_to_ints("f7", "d8"))
    assert g._is_move_valid(*g.strings_to_ints("f7", "d6"))
    assert g._is_move_valid(*g.strings_to_ints("f7", "e5"))
    assert g._is_move_valid(*g.strings_to_ints("f7", "h8"))
    assert g._is_move_valid(*g.strings_to_ints("f7", "h6"))
    assert g._is_move_valid(*g.strings_to_ints("f7", "g5"))

    assert not g._is_move_valid(*g.strings_to_ints("c3", "e4"))
    assert not g._is_move_valid(*g.strings_to_ints("c3", "d1"))
    assert not g._is_move_valid(*g.strings_to_ints("c3", "a2"))


def test_13_white_queen():
    g = ClassicGame()
    g.load_fen("rnbqkbnr/pppp2pp/5p2/4p3/3QPP2/3B1N2/PPPPB1PP/RN2K2R w KQkq - 0 1")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_ints("d4", "d5"))
    assert g._is_move_valid(*g.strings_to_ints("d4", "d6"))
    assert g._is_move_valid(*g.strings_to_ints("d4", "d7"))
    assert not g._is_move_valid(*g.strings_to_ints("d4", "d8"))

    assert g._is_move_valid(*g.strings_to_ints("d4", "c5"))
    assert g._is_move_valid(*g.strings_to_ints("d4", "b6"))
    assert g._is_move_valid(*g.strings_to_ints("d4", "a7"))

    assert g._is_move_valid(*g.strings_to_ints("d4", "c4"))
    assert g._is_move_valid(*g.strings_to_ints("d4", "b4"))
    assert g._is_move_valid(*g.strings_to_ints("d4", "a4"))
    assert not g._is_move_valid(*g.strings_to_ints("d4", "e4"))
    assert not g._is_move_valid(*g.strings_to_ints("d4", "f4"))
    assert not g._is_move_valid(*g.strings_to_ints("d4", "d3"))

    assert g._is_move_valid(*g.strings_to_ints("d4", "c3"))
    assert g._is_move_valid(*g.strings_to_ints("d4", "e3"))
    assert g._is_move_valid(*g.strings_to_ints("d4", "f2"))
    assert g._is_move_valid(*g.strings_to_ints("d4", "g1"))
    assert g._is_move_valid(*g.strings_to_ints("d4", "c3"))
    assert not g._is_move_valid(*g.strings_to_ints("d4", "b2"))


def test_14_move_and_check():
    g = ClassicGame()
    g.load_fen("kp2q3/pq5q/6P1/q2QNP2/q1QBKR1q/5N2/2N1R1N1/1q2q2q w - - 0 1")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_ints("c4", "b4")), "Valid move"
    assert g._is_move_valid(*g.strings_to_ints("c4", "a4")), "Valid move"
    assert g._is_move_valid(*g.strings_to_ints("c4", "c5")), "Valid move"
    assert g._is_move_valid(*g.strings_to_ints("c4", "c3")), "Valid move"
    assert g._is_move_valid(*g.strings_to_ints("c4", "a2")), "Valid move"

    assert g._is_move_valid(*g.strings_to_ints("d5", "c6")), "Valid move"
    assert g._is_move_valid(*g.strings_to_ints("d5", "b7")), "Valid move"
    assert not g._is_move_valid(*g.strings_to_ints("d5", "a8")), "Move is illegal"
    assert not g._is_move_valid(*g.strings_to_ints("d5", "d6")), "Move is illegal"
    assert not g._is_move_valid(*g.strings_to_ints("d5", "c5")), "Move is illegal"
    assert not g._is_move_valid(*g.strings_to_ints("d5", "e4")), "Move is illegal"

    assert not g._is_move_valid(*g.strings_to_ints("c2", "e1")), "Move is illegal"

    assert g._is_move_valid(*g.strings_to_ints("f4", "h4")), "Valid move"
    assert g._is_move_valid(*g.strings_to_ints("f4", "g4")), "Valid move"
    assert not g._is_move_valid(*g.strings_to_ints("f4", "f3")), "Move is illegal"
    assert not g._is_move_valid(*g.strings_to_ints("f4", "f5")), "Move is illegal"
    assert not g._is_move_valid(*g.strings_to_ints("f4", "f2")), "Move is illegal"
    assert not g._is_move_valid(*g.strings_to_ints("f4", "f1")), "Move is illegal"
    assert not g._is_move_valid(*g.strings_to_ints("f4", "e4")), "Move is illegal"

    assert g._is_move_valid(*g.strings_to_ints("f3", "h4")), "Valid move"
    assert g._is_move_valid(*g.strings_to_ints("f3", "e1")), "Valid move"
    assert g._is_move_valid(*g.strings_to_ints("f3", "h2")), "Valid move"

    assert g._is_move_valid(*g.strings_to_ints("g2", "h4")), "Valid move"
    assert g._is_move_valid(*g.strings_to_ints("g2", "e1")), "Valid move"

    assert g._is_move_valid(*g.strings_to_ints("e2", "e1")), "Valid move"
    assert g._is_move_valid(*g.strings_to_ints("e2", "e3")), "Valid move"
    assert not g._is_move_valid(*g.strings_to_ints("e2", "f1")), "Move is illegal"
    assert not g._is_move_valid(*g.strings_to_ints("e2", "d1")), "Move is illegal"
    assert not g._is_move_valid(*g.strings_to_ints("e2", "e4")), "Move is illegal"

    assert not g._is_move_valid(*g.strings_to_ints("c2", "e4")), "Move is illegal"
    assert not g._is_move_valid(*g.strings_to_ints("c2", "e1")), "Move is illegal"
    assert not g._is_move_valid(*g.strings_to_ints("c2", "e3")), "Move is illegal"
    assert not g._is_move_valid(*g.strings_to_ints("c2", "b4")), "Move is illegal"


def test_15_under_threat():
    g = ClassicGame()
    g.load_fen("r3kbnr/pp2pppp/2ppq3/2n5/2P5/BPNQPN2/P2P1PPP/R3K2R w KQkq - 1 12")
    g.board.print_table()

    assert g.under_threat(*g.strings_to_ints("c4"))
    assert g.under_threat(*g.strings_to_ints("e3"))
    assert g.under_threat(*g.strings_to_ints("d6"))
    assert g.under_threat(*g.strings_to_ints("c5"))

    assert not g.under_threat(*g.strings_to_ints("e1"))
    assert not g.under_threat(*g.strings_to_ints("h1"))
    assert not g.under_threat(*g.strings_to_ints("a1"))
    assert not g.under_threat(*g.strings_to_ints("g8"))
    assert not g.under_threat(*g.strings_to_ints("g8"))


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
        assert g.under_threat(*g.strings_to_ints(mv), defending=1), f"White is not attacking {mv}"


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
        assert g._is_move_valid(*g.strings_to_ints(*pair)), "This is not white valid move"

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
        assert not g._is_move_valid(*g.strings_to_ints(*pair)), f"This move is invalid for white: {pair}"


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
        assert g.board.get(*g.strings_to_ints(pos)).team == 1, f"Fig on {pos} is black!"
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
        assert g.board.get(*g.strings_to_ints(pos)).team == 0, f"Fig on {pos} is white!"


def test_18_nopassant():
    g = ClassicGame()
    g.load_fen("rnbqkbnr/pp1p1pp1/7p/2pPp3/8/7P/PPP1PPP1/RNBQKBNR w KQkq - 0 4")

    inv_moves = [
            ("d5", "c6"),
            ("d5", "e6"),
            ("d5", "d7"),
            ("d5", "d8"),

    ]
    for pair in inv_moves:
        assert not g._is_move_valid(*g.strings_to_ints(*pair)), f"This move is invalid for white: {pair}"


def test_19_valid_checks():
    g = ClassicGame()
    g.load_fen("rnbq4/pppppbk1/8/1Q4n1/2Q5/PPP5/PPPP3P/K1RQ1BN1 w - - 0 1")

    val_moves = [
            ("c4", "f7"),
            ("c4", "d4"),
            ("b5", "g5"),
            ("b5", "e5"),
    ]
    for pair in val_moves:
        assert g._is_move_valid(*g.strings_to_ints(*pair)), f"This is invalid for white: {pair}"


def test_20_valid_mates():
    def new():
        g = ClassicGame()
        g.load_fen("rnbQ4/pppp1pkp/8/1Q4n1/5Q2/PPP5/PPPP3P/K1R2BN1 w - - 0 1")
        return g

    val_moves = [
            ("b5", "g5"),
            ("f4", "g5"),
    ]
    for pair in val_moves:
        g = new()
        g.make_move(g.strings_to_ints(*pair))
        assert g._is_game_over(), "Mate! Game over."


def test_21_invalid_game():
    g = ClassicGame()
    with pytest.raises(ValueError):
        g.load_fen("r3k2r/ppp3pp/8/8/8/8/PPPQQQPP/RNBQKBNR w KQkq - 0 1")


def test_22_new_board():
    g = ClassicGame()
    g.new_game()
    for row in [1, 6]:
        for x in range(8):
            c = 0 if row == 1 else 1
            fig = g.board.get((x, row))
            assert isinstance(fig, (Pawn,)), f"Here should be a pawn: {x}"
            assert fig.color == c, f"Pawn valid color is: {c}"

    for row in [0, 7]:
        for col, _val_fig in zip(range(8), [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
            c = 0 if row == 0 else 1
            fig = g.board.get((col, row))
            assert fig.color == c, f"Figure color should be: {c}"
            assert isinstance(fig, (_val_fig,)), f"This fig should be: {_val_fig}"


def test_23_kings_dict():
    g = ClassicGame()
    g.new_game()
    kings = g.kings
    for c in range(2):
        assert 0 in kings, f"This color should be in kings: {c}"
        pos = (4, 0) if c == 0 else (4, 7)
        assert pos in kings[c], f"King should be here:{pos}"
        assert len(kings[c]) == 1, f"Only one king for classic game but got: {len(kings[c])}"


def test_24_loading_check():
    raise NotImplementedError


def test_25_():
    pass


def test_26_():
    pass


def test_27_():
    pass