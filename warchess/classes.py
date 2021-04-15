from abc import ABC, abstractmethod, abstractproperty
from collections import namedtuple
from itertools import product
from warnings import warn

from copy import copy, deepcopy

from abstracts import FigureBase, SpecialBase, \
    attack_tuple, move_tuple, BoardBase, GameModeBase

import numpy as np
import time


class Pawn(FigureBase):
    def __init__(self, *a, did_rush=False, **kw):
        super().__init__(*a, **kw)
        self.did_rush = did_rush

        self._move_patterns = (
                move_tuple(0, 1),
                # self.pattern_tuple(0, 2),
        )
        self._attack_patterns = (
                attack_tuple(-1, 1),
                attack_tuple(1, 1),
        )
        self._specials = (PawnRush(), EnPassant(),)

        if self.direction == 1:
            self._move_patterns = self.flip_y_pattern(self._move_patterns)
            self._attack_patterns = self.flip_y_pattern(self._attack_patterns)
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

    def is_valid(self, game, board, f1, f2):
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

    def apply(self, game, board, f1, f2):
        board.move_figure(f1, f2)


class EnPassant(SpecialBase):
    def __init__(self):
        super().__init__()
        self.patterns = (self.named_tup(0, 2),)

    @property
    def name(self):
        return "EnPassant"

    def is_valid(self, game, board, f1, f2):
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

    def apply(self, game, board, f1, f2):
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

        self._move_patterns = (
                move_tuple(1, 2),
                move_tuple(1, -2),
                move_tuple(2, 1),
                move_tuple(2, -1),
                move_tuple(-1, 2),
                move_tuple(-1, -2),
                move_tuple(-2, 1),
                move_tuple(-2, -1),
        )
        self._attack_patterns = (
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
    def __init__(self, *a, inf_move=True, inf_attack=True, **kw):
        super().__init__(*a, inf_move=inf_move, inf_attack=inf_attack, **kw)

        self._move_patterns = (
                move_tuple(1, 1),
                move_tuple(-1, -1),
                move_tuple(1, -1),
                move_tuple(-1, 1),
        )
        self._attack_patterns = (
                attack_tuple(1, 1),
                attack_tuple(-1, -1),
                attack_tuple(1, -1),
                attack_tuple(-1, 1),
        )

    @property
    def name(self):
        return "Bishop"


class Queen(FigureBase):
    def __init__(self, *a, inf_move=True, inf_attack=True, **kw):
        super().__init__(*a, inf_move=inf_move, inf_attack=inf_attack, **kw)
        self._move_patterns = (
                move_tuple(1, -1),
                move_tuple(1, 0),
                move_tuple(1, 1),
                move_tuple(-1, -1),
                move_tuple(-1, 0),
                move_tuple(-1, 1),
                move_tuple(0, 1),
                move_tuple(0, -1),
        )
        self._attack_patterns = (
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
    def __init__(self, *a, inf_move=False, inf_attack=False, **kw):
        super().__init__(*a, inf_move=inf_move, inf_attack=inf_attack, **kw)

        self._specials = (Castle(),)
        # print(self._special)

    @property
    def name(self):
        return "King"


class Castle(SpecialBase):
    def __init__(self):
        super().__init__()
        self.patterns = (self.named_tup(-2, 0), self.named_tup(2, 0))

    def is_valid(self, game, board, f1, f2):
        x, y = f1

        cx, cy = f2
        fig = board.get(f1)
        if x != 4 or y not in (0, 7):
            return False

        threats = []

        if isinstance(fig, King) and not fig.was_moved:
            if cx == 2 and cy == 0:
                rk = board.get((0, 0))
                empty1 = board.get((1, 0))
                empty2 = board.get((2, 0))
                empty3 = board.get((3, 0))
                threats = [(2, 0), (3, 0)]

            elif cx == 6 and cy == 0:
                rk = board.get((7, 0))
                empty1 = board.get((6, 0))
                empty2 = board.get((7, 0))
                empty3 = None
                threats = [(5, 0), (6, 0)]

            elif cx == 2 and cy == 7:
                rk = board.get((0, 7))
                empty1 = board.get((1, 7))
                empty2 = board.get((2, 7))
                empty3 = board.get((3, 7))
                threats = [(2, 7), (3, 7)]

            elif cx == 6 and cy == 7:
                rk = board.get((7, 7))
                empty1 = board.get((6, 7))
                empty2 = board.get((7, 7))
                empty3 = None
                threats = [(5, 7), (6, 7)]

            else:
                return False

            if empty1 is not None or empty2 is not None and empty3 is not None:
                "Check if there is fig between king and rook"
                return False

            "Add kings position"
            threats.append(f1)

            if isinstance(rk, Rook) and not rk.was_moved:
                if game.under_threat(fields=threats, defending=fig.team):
                    return False
                return True
        else:
            return False

    def apply(self, game, board, f1, f2):
        x, y = f2
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
    def __init__(self, *a, inf_move=True, inf_attack=True, **kw):
        super(Rook, self).__init__(*a, inf_move=inf_move, inf_attack=inf_attack, **kw)
        self._move_patterns = (
                move_tuple(0, 1),
                move_tuple(1, 0),
                move_tuple(0, -1),
                move_tuple(-1, 0),
        )
        self._attack_patterns = (
                attack_tuple(0, 1),
                attack_tuple(1, 0),
                attack_tuple(0, -1),
                attack_tuple(-1, 0),
        )

    @property
    def name(self):
        return "Rook"


class Board(BoardBase):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)


class ClassicGame(GameModeBase):
    def __init__(self):
        super().__init__()
        self.board = Board(8, 8)
        self.checks = {num: False for num in range(self.players_num)}

    def new_game(self):
        self.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self._initial_checks()

    def _initial_checks(self):
        for color in range(self.players_num):
            for pos in self.kings[color]:
                is_check = self.under_threat(field=pos)

                if is_check and self.current_player_turn != color:
                    raise ValueError(f"Invalid Game. player moved into check: {color}")
                elif is_check:
                    self.checks[color] = True
                else:
                    self.checks[color] = False

    def load_fen(self, fen):
        self._load_fen(fen)
        self._initial_checks()

    def _load_fen(self, fen: str):
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
                elif 97 <= order <= 122:
                    fig = self.get_proper_figure(char, 1)
                    self.board.add_figure((x, y), fig)
                else:
                    skip = int(char)
                    x += skip
                    if x > 7:
                        break
                    continue
                if isinstance(fig, (King,)):
                    self.kings[fig.color][x, y] = fig
                    print(f"Adding king: {fig.color}, to ({x},{y})")
                x += 1

        self.current_player_turn = 0 if cur_player == "w" else 1

        if 'k' not in castling:
            rk = self.board.get((7, 7))
            if rk:
                rk.was_moved = True
        if 'K' not in castling:
            rk = self.board.get((7, 0))
            if rk:
                rk.was_moved = True
        if "q" not in castling:
            rk = self.board.get((0, 7))
            if rk:
                rk.was_moved = True
        if "Q" not in castling:
            rk = self.board.get((0, 0))
            if rk:
                rk.was_moved = True

        if enpasant != "-":
            x, y = enpasant

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

    # def extra_move_rules(self, moving_color):
    #     return not self._is_player_checked(moving_color)

    def _is_player_checked(self, color):
        kgs = self.kings[color]
        for pos, king in kgs.items():
            self.under_threat(field=pos, defending=king.team)
        return False

    def _is_game_over(self):
        pass

    def _post_move_actions(self, field2):
        if self._is_promotion(field2):
            self._promote(field2)

    def _promote(self, field2):
        cl = self.board.get(field2).color
        fig = self.get_promotion_fig(cl)
        self.board.change_fig(field2, fig)

    def get_promotion_fig(self, color):
        warn("static queen return")
        return Queen(color)

    def strings_to_ints(self, *arrs):
        """
        Translate any number of string into int tuples
        Args:
            *arrs:

        Returns:
            tuple(moves)

        """
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

        # def make_move(self, f1, f2):
        #     pass


if __name__ == "__main__":
    g = ClassicGame()
    g.load_fen("r3r1k1/pppb1ppp/5n2/3P4/2P5/2NB1P2/PP1q3P/2KR1R2 w - - 0 15")
    g.board.print_table()

    g.make_move(g.strings_to_ints("a2", "a4"))
    g.board.print_table()
