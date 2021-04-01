import pytest

from classes import Rook, Pawn, Knight, Queen, King, Bishop, ClassicGame


def test_1_():
    figs = [Pawn, Rook, King, Knight, Queen, Bishop]
    figs = [f(n) for n in range(2) for f in figs]
    for f in figs:
        assert len(f.name) > 0, f"{f}"
        assert len(f._move_pattern) > 0, f"{f}"
        assert len(f._attack_pattern) > 0, f"{f}"


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
    with pytest.raises(ValueError):
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


def test_8_Pawn():
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


def test_9_Pawn_Black():
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


def test_9_Pawn_Black2():
    g = ClassicGame()
    g.load_fen("rnbqkbr1/p1p5/1p6/2npPppp/5PP1/P1P4P/1P1P3R/RNBQKB2 b Qq - 2 12")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_tuple("c7", "c6"))

    assert not g._is_move_valid(*g.strings_to_tuple("c7", "c5"))
    assert not g._is_move_valid(*g.strings_to_tuple("c7", "b5"))
    assert not g._is_move_valid(*g.strings_to_tuple("c7", "b6"))
    assert not g._is_move_valid(*g.strings_to_tuple("c7", "d5"))
    assert not g._is_move_valid(*g.strings_to_tuple("c7", "d6"))


def test_9_Pawn_white_2():
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

    assert not g._is_move_valid(*g.strings_to_tuple("e1", "c1"))
    assert not g._is_move_valid(*g.strings_to_tuple("e1", "g1"))
    assert not g._is_move_valid(*g.strings_to_tuple("e1", "d1"))
    assert not g._is_move_valid(*g.strings_to_tuple("e1", "f1"))


def test_10_castle_w_3_blockade():
    g = ClassicGame()
    g.load_fen("r3kbnr/pp2pppp/2ppq3/3Q4/2P5/BnN1PN2/P2P1PPP/R3K2R w KQkq - 0 13")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_tuple("e1", "d1"))
    assert g._is_move_valid(*g.strings_to_tuple("e1", "f1"))
    assert g._is_move_valid(*g.strings_to_tuple("e1", "e2"))

    assert g._is_move_valid(*g.strings_to_tuple("e1", "g1"))
    assert not g._is_move_valid(*g.strings_to_tuple("e1", "c1"))


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


def test_14_():
    pass


def test_15_():
    pass


def test_16_():
    pass


def test_17_():
    pass
