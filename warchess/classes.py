from abc import ABC, abstractmethod, abstractproperty
from collections import namedtuple
from itertools import product

from copy import copy, deepcopy

from abstracts import FigureBase, SpecialBase, \
    attack_tuple, move_tuple, BoardBase, GameModeBase

import numpy as np
import time


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
        self._specials = (PawnRush(), EnPassant(),)

        if self.direction == 1:
            self._move_pattern = self.flip_y_pattern(self._move_pattern)
            self._attack_pattern = self.flip_y_pattern(self._attack_pattern)
            for spec in self._specials:
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

    # @property
    # def special_pattern(self):
    #     return self._special

    def make_special_move(self):
        assert not self.was_moved, "Pawn can't be moved"
        self.did_rush = True
        self.was_moved = True

    def clear_special_attr(self):
        self.did_rush = False

    def make_move(self):
        self.was_moved = True
        self.did_rush = False


class PawnRush(SpecialBase):
    def __init__(self):
        super().__init__()
        self.patterns = (self.named_tup(0, 2),)

    @property
    def name(self):
        return "PawnRush"

    def is_valid(self, board, f1, f2):
        x, y = f1
        if not (y == 1 or y == 6):
            return False

        dx, dy = f2[0] - f1[0], f2[1] - f1[1]
        fig = board.get(f1)
        target = board.get(f2)
        c = fig.color
        if c == 0:
            no_fig = board.get((f2[0], f2[1] - 1))
        else:
            no_fig = board.get((f2[0], f2[1] + 1))

        if target is None and no_fig is None:
            if dx == 0 and (c == 0 and dy == 2) or (c == 1 and dy == -2):
                return True
        else:
            return False

    def apply(self, board, f1, f2):
        board.move_figure(f1, f2)


class EnPassant(SpecialBase):
    def __init__(self):
        super().__init__()
        self.patterns = (self.named_tup(0, 2),)

    @property
    def name(self):
        return "EnPassant"

    def is_valid(self, board, f1, f2):
        x, y = f1
        bx, by = f2
        fig1 = board.get(f1)

        if abs(x - bx) != 1:
            return False

        if by == 5 and y == 4:
            fig2_pos = bx, y
        elif by == 2 and y == 3:
            fig2_pos = bx, y
        else:
            return False
            # raise ValueError(f"This move is not valid: {f1} -> {f2}")

        fig2 = board.get(fig2_pos)
        if not isinstance(fig2, Pawn):
            print("Not a pawn")
            return False

        if fig1.color == fig2.color:
            print("Same fig colors")
            return False

        if fig2.did_rush:
            print("did rush")
            return True
        else:
            print("It did not rush")
            return False

    def apply(self, board, f1, f2):
        x, y = f1
        bx, by = f2
        # fig1 = board.get(f1)

        if y == 5:
            fig2_pos = bx, by - 1
        elif y == 3:
            fig2_pos = bx, by + 1
        else:
            raise ValueError(f"This move is not valid: {f1} -> {f2}")

        board.remove_figure(fig2_pos)
        board.move_figure(f1, f2)


class Knight(FigureBase):
    def __init__(self, *a, air_move=True, air_attack=True, **kw):
        super().__init__(*a, air_move=air_move, air_attack=air_attack, **kw)

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
        self._attack_pattern = (
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

        self._specials = (Castle(),)
        # print(self._special)

    @property
    def name(self):
        return "King"


class Castle(SpecialBase):
    def __init__(self):
        super().__init__()
        self.patterns = (self.named_tup(-2, 0), self.named_tup(2, 0))

    def is_valid(self, board, f1, f2):
        x, y = f1

        bx, by = f2
        fig = board.get(f1)
        if x != 4 or y not in (0, 7):
            return False

        if isinstance(fig, King) and not fig.was_moved:
            if bx == 4 and by == 0:
                rk = board.get((7, 0))
                empty1 = board.get((6, 0))
                empty2 = board.get((7, 0))
                empty3 = None
            elif bx == 2 and by == 0:
                rk = board.get((0, 0))
                empty1 = board.get((1, 0))
                empty2 = board.get((2, 0))
                empty3 = board.get((3, 0))

            elif bx == 6 and by == 7:
                rk = board.get((7, 7))
                empty1 = board.get((6, 7))
                empty2 = board.get((7, 7))
                empty3 = None
            elif bx == 6 and by == 0:
                rk = board.get((0, 7))
                empty1 = board.get((1, 7))
                empty2 = board.get((2, 7))
                empty3 = board.get((3, 7))
            else:
                return False

            if empty1 is not None or empty2 is not None and empty3 is not None:
                return False

            if isinstance(rk, Rook) and not rk.was_moved:
                return True
        else:
            return False

    def apply(self, board, f1, f2):
        x, y = f1
        fig = board.get(f1)
        if x == 6 and y == 0:
            rk = board.get((7, 0))
            rook_field = (5, 0)
        elif x == 2 and y == 0:
            rk = board.get((0, 0))
            rook_field = (3, 0)

        elif x == 6 and y == 7:
            rk = board.get((7, 7))
            rook_field = (5, 7)
        elif x == 6 and y == 0:
            rk = board.get((0, 7))
            rook_field = (3, 7)
        else:
            raise ValueError(f"Impossible move:{f1} -> {f2}")

        board.move_figure(f1, f2)
        board.add_figure(rook_field, rk)

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
        super().__init__()
        self.board = Board(8, 8)
        self.kings = dict()
        self.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def _is_game_over(self):
        pass

    def load_fen(self, fen: str):
        """
        Setup board to fen
        8Lines of board layout
        Current turn.
        Castling possibilities
        Enpassant to this field.
        2 x Counter
        Small letters - black
        Big letter - white
        Args:
            fen:

        Returns:

        """
        self.board.clear_board()
        fen, cur_player, castling, enpasant, lasthit, move_count = fen.split(r" ")
        fen = fen.split(r"/")
        for y, line in enumerate(fen):
            y = 7 - y
            x = 0
            if y > 7 or y < 0:
                break

            for char in line:
                order = ord(char)

                if 65 <= order <= 90:
                    fig = self.get_proper_figure(char, 0)
                    self.board.add_figure((x, y), fig)
                    x += 1
                elif 97 <= order <= 122:
                    fig = self.get_proper_figure(char, 1)
                    self.board.add_figure((x, y), fig)
                    x += 1
                else:
                    skip = int(char)
                    x += skip
                    if x > 7:
                        break
                    continue
                if isinstance(fig, King):
                    self.kings[fig.color] = fig

        self.current_player_turn = 0 if cur_player == "w" else 1

        if 'k' in castling:
            rk = self.board.get((7, 7))
            rk.was_moved = False
        if 'K' in castling:
            rk = self.board.get((0, 7))
            rk.was_moved = False
        if "q" in castling:
            rk = self.board.get((0, 7))
            rk.was_moved = False
        if "Q" in castling:
            rk = self.board.get((0, 0))
            rk.was_moved = False

        if enpasant != "-":
            x, y = enpasant

            # if 97 <= ord(x) <= 104:  # a <= x <= h
            #     color_who_rushed = 0  # White rushed
            # elif 65 <= ord(x) <= 72:  # A <= x <= H
            #     color_who_rushed = 1  # Black rushed
            # else:
            #     raise ValueError(f"This is not correct position for enpassant: {x}{y}")

            y = int(y)
            if y <= 3:
                color_who_rushed = 0
                y = y  # -1 + 1
            else:
                color_who_rushed = 1
                y = y - 2  # -1 -1 index

            x = ord(x.lower()) - 97  # a=97,

            pw = self.board.get((x, y))
            assert pw.color == color_who_rushed, f"Wrong pawn color, should be: {color_who_rushed}, is {pw.color}"
            assert isinstance(pw, Pawn)
            pw.did_rush = True

        self.last_hit = lasthit
        self.move_count = move_count

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

    def _is_promotion(self, field):
        fig = self.board.get(field)
        x, y = field
        if y == 7 and fig.color == 0:
            return True
        if y == 0 and fig.color == 1:
            return True
        return False

    def check_rules_for(self, color):
        return not self._is_team_checked(color)

    def _post_move_actions(self, field2):
        if self._is_promotion(field2):
            self._promote(field2)

    def _promote(self, field2):
        cl = self.board.get(field2).color
        fig = self.get_promotion_fig(cl)
        self.board.change_fig(field2, fig)

    def get_promotion_fig(self, color):
        return Queen(color)

    def strings_to_tuple(self, *arrs):
        out = []
        if type(arrs) is str:
            arrs = [arrs]

        for move in arrs:
            move = move.lower()
            x, y = move
            y = int(y) - 1
            x = ord(x.lower()) - 97  # a=97,
            out.append((x, y))
        return out

    def _is_team_checked(self, color):
        return False
        raise NotImplementedError()

        # def make_move(self, f1, f2):
        #     pass


if __name__ == "__main__":

    # c = ClassicGame()
    # c.make_move(*c.strings_to_tuple("A2", "A3"))
    # c.make_move(*c.strings_to_tuple("A7", "A6"))
    # c.make_move(*c.strings_to_tuple("B2", "B4"))
    # c.board.print_table()

    g = ClassicGame()
    g.load_fen("r3kbnr/pp2pppp/2ppq3/3Q4/2P5/BPNnPN2/P2P1PPP/R3K2R w KQkq - 3 13")
    g.board.print_table()

    assert g._is_move_valid(*g.strings_to_tuple("e1", "d1"))

# print(out)
