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

    def is_valid(self, board, f1, f2):
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


class EnPassant(SpecialBase):
    def __init__(self):
        super().__init__()
        self.patterns = (self.named_tup(0, 2),)

    @property
    def name(self):
        return "EnPassant"

    def is_valid(self, context, f1, f2):
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
        Castling possibilites
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
            rk = self.board.get((7, 0))
            rk.was_moved = False
        if "q" in castling:
            rk = self.board.get((7, 7))
            rk.was_moved = False
        if "Q" in castling:
            rk = self.board.get((0, 7))
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

    def get_promotion_fig(self, color):
        return Queen(color)

    # def get_correct_moves(self, f1, all=True):
    #     fig = self.board.get(f1)
    #
    #     moves = fig._moves_patterns

    def _is_move_valid(self, f1, f2):
        if self._can_fig_move(f1, f2):
            # print(f"VALID: {f1} {f2}")
            return True

    def _can_fig_move(self, f1, f2):
        move = f2[0] - f1[0], f2[1] - f1[0]
        fig = self.board.get(f1)
        temp_target = self.board.get(f2)

        move_diag = abs(move[0]) == abs(move[1])
        move_lin = move[0] == 0 or move[1] == 0
        direction = tuple(np.sign(np.array(move)))

        "Check if figure is here"
        if fig is None:
            return False

        "Wrong figure, Turn for other player"
        if self.current_player_turn != fig.color:
            return False

        if fig.is_move_infinite and (
                direction in fig.move_pattern or direction in fig.attack_pattern
        ):
            return True

        elif move in fig.move_pattern or move in fig.attack_pattern:
            pass

        elif fig.is_move_flying and (
                move in fig.move_pattern or fig.attack_pattern
        ):
            return True

        else:
            for spc in fig.special:
                if spc.is_valid(self.board, f1, f2):
                    return True

        return False

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
        raise NotImplementedError()

        # def make_move(self, f1, f2):
        #     pass


if __name__ == "__main__":

    c = ClassicGame()
    c.make_move(*c.strings_to_tuple("A2", "A3"))
