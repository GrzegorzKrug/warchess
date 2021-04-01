from abc import ABC, abstractmethod, abstractproperty
from collections import namedtuple
from itertools import product

from abstracts import FigureBase, SpecialBase, \
    attack_tuple, move_tuple, BoardBase, GameModeBase


class Pawn(FigureBase):
    def __init__(self, *a, did_rush=False, **kw):
        super().__init__(*a, **kw)
        self.did_rush = did_rush

        self._move_pattern = (
                move_tuple(0, 1),
                # self.pattern_tuple(0, 2),
        )
        self._attack_pattern = (
                attack_tuple(-1, 1),
                attack_tuple(1, 1),
        )
        self._special = (PawnRush(), EnPassant())

        if self.direction == 1:
            self._move_pattern = self.flip_y_pattern(self._move_pattern)
            self._attack_pattern = self.flip_y_pattern(self._attack_pattern)
            for spec in self._special:
                spec.flip_this_by_y()

        # print(self._move_pattern)
        # print(self._attack_pattern)
        # print(self._special)

    @property
    def name(self):
        if self.color == 0:
            return "WPawn"
        else:
            return "BPawn"

    @property
    def move_pattern(self):
        return self._move_pattern

    @property
    def attack_pattern(self):
        return self._attack_pattern

    @property
    def special_pattern(self):
        return self._special

    def make_special_move(self):
        assert not self.was_moved, "Pawn can't be moved"
        self.did_rush = True
        self.was_moved = True

    def clear_special_attr(self):
        self.did_rush = False

    def make_move(self):
        self.did_rush = False


class PawnRush(SpecialBase):
    def __init__(self):
        super().__init__()
        self.patterns = (self.named_tup(0, 2),)

    @property
    def name(self):
        return "PawnRush"

    def is_valid(self, context, move):
        pass


class EnPassant(SpecialBase):
    def __init__(self):
        super().__init__()
        self.patterns = (self.named_tup(0, 2),)

    @property
    def name(self):
        return "EnPassant"

    def is_valid(self, context, move):
        pass


class Knight(FigureBase):
    def __init__(self, *a, flying_move=True, **kw):
        super().__init__(*a, flying_move=flying_move, **kw)

        self._move_pattern = (
                move_tuple(1, 2),
                move_tuple(1, -2),
                move_tuple(2, 1),
                move_tuple(2, -1),
                move_tuple(-1, 2),
                move_tuple(-1, -2),
                move_tuple(-2, 1),
                move_tuple(-2, -1),
        )
        self._attack_pattern = (
                attack_tuple(1, 2),
                attack_tuple(1, -2),
                attack_tuple(2, 1),
                attack_tuple(2, -1),
                attack_tuple(-1, 2),
                attack_tuple(-1, -2),
                attack_tuple(-2, 1),
                attack_tuple(-2, -1),
        )

    @property
    def name(self):
        return "Knight"


class Bishop(FigureBase):
    def __init__(self, *a, infinite_move=True, **kw):
        super().__init__(*a, infinite_move=infinite_move, **kw)

        self._move_pattern = (
                move_tuple(1, 1),
                move_tuple(-1, -1),
                move_tuple(1, -1),
                move_tuple(-1, 1),
        )
        self._attack_pattern = (
                attack_tuple(1, 1),
                attack_tuple(-1, -1),
                attack_tuple(1, -1),
                attack_tuple(-1, 1),
        )

    @property
    def name(self):
        return "Bishop"


class Queen(FigureBase):
    def __init__(self, *a, infinite_move=True, **kw):
        super().__init__(*a, infinite_move=infinite_move, **kw)
        self._move_pattern = (
                move_tuple(1, -1),
                move_tuple(1, 0),
                move_tuple(1, 1),
                move_tuple(-1, -1),
                move_tuple(-1, 0),
                move_tuple(-1, 1),
                move_tuple(0, 1),
                move_tuple(0, -1),
        )
        self._move_pattern = (
                attack_tuple(1, -1),
                attack_tuple(1, 0),
                attack_tuple(1, 1),
                attack_tuple(-1, -1),
                attack_tuple(-1, 0),
                attack_tuple(-1, 1),
                attack_tuple(0, 1),
                attack_tuple(0, -1),
        )

    @property
    def name(self):
        return "Queen"


class King(Queen):
    def __init__(self, *a, infinite_move=False, **kw):
        super().__init__(*a, infinite_move=infinite_move, **kw)

        self._special = (Castle())
        # print(self._special)

    @property
    def name(self):
        return "King"


class Castle(SpecialBase):
    def __init__(self):
        super().__init__()
        self.patterns = (self.named_tup(-2, 0), self.named_tup(2, 0))

    def is_valid(self, context, move):
        pass

    @property
    def name(self):
        return "Castle"


# class CastleRookToKing(SpecialBase):
#     def __init__(self):
#         super().__init__()
#         self.patterns = (self.named_tup(3, 0), self.named_tup(-2, 0))
#
#     def is_valid(self, context, move):
#         pass
#
#     @property
#     def name(self):
#         return "CastleR"
#

class Rook(FigureBase):
    def __init__(self, *a, infinite_move=True, **kw):
        super(Rook, self).__init__(*a, infinite_move=infinite_move, **kw)
        self._move_pattern = (
                move_tuple(0, 1),
                move_tuple(1, 0),
                move_tuple(0, -1),
                move_tuple(-1, 0),
        )
        self._attack_pattern = (
                attack_tuple(0, 1),
                attack_tuple(1, 0),
                attack_tuple(0, -1),
                attack_tuple(-1, 0),
        )

    @property
    def name(self):
        return "Rook"


class Board(BoardBase):
    pass


#     def __init__(self, w=8, h=8):
#         self.board = dict()
#         self.figures = dict()
#
#     def move_figure(self):
#         pass


class ClassicGame(GameModeBase):
    def __init__(self):
        self.board = Board(8, 8)
        self.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def action(self, field1, field2):
        pass

    def _is_game_over(self):
        pass

    def load_fen(self, fen):
        self.board.clear_board()
        fen, *_ = fen.split(r" ")
        fen = fen.split(r"/")
        for y, line in enumerate(fen):
            y = 7 - y
            x = 0
            if y > 7 or y < 0:
                break

            for lt in line:
                order = ord(lt)

                if 65 <= order <= 90:
                    fig = self.get_proper_figure(lt, 0)
                    self.board.add_figure((x, y), fig)
                    x += 1
                elif 97 <= order <= 122:
                    fig = self.get_proper_figure(lt, 1)
                    self.board.add_figure((x, y), fig)
                    x += 1
                else:
                    skip = int(lt)
                    x += skip
                    if x > 7:
                        break

    def get_proper_figure(self, name, color):
        name = name.lower()
        if name in ['pawn', 'p']:
            fig = Pawn(color)
        elif name in ['knight', 'n']:
            fig = Knight(color)
        elif name in ['bishop', 'b']:
            fig = Bishop(color)
        elif name in ['rook', 'r']:
            fig = Rook(color)
        elif name in ['queen', 'q']:
            fig = Queen(color)
        elif name in ['king', 'k']:
            fig = King(color)
        else:
            fig = None

        return fig

    def _is_move_valid(self, some):
        pass

    def _is_team_checked(self, color):
        pass

    def new_game(self):
        self.__init__()


if __name__ == "__main__":

    c = ClassicGame()

    # for pos, fig in c.board.figs_on_board.items():
    #     print(pos, fig.name, fig.color)

    c.load_fen("rnbqkb1r/pp2pppp/5n2/3p4/2PP4/2N5/PP3PPP/R1BQKBNR b KQkq - 2 5")
    c.board.print_table()
# print(p2.was_moved)
