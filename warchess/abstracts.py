from abc import ABC, abstractmethod, abstractproperty
from collections import namedtuple
from copy import deepcopy

from typing import Any, Tuple, List, AnyStr, Union, Iterable

import numpy as np

# pattern_tuple = namedtuple("P", field_names=["X", "Y"])


move_tuple = namedtuple("Move", field_names=["X", "Y"])
attack_tuple = namedtuple("Atck", field_names=["X", "Y"])
special_tuple = namedtuple("Spec", field_names=["X", "Y"])


def get_right_tuple(tuplelike):
    if isinstance(tuplelike, move_tuple):
        return move_tuple
    elif isinstance(tuplelike, attack_tuple):
        return attack_tuple
    else:
        return special_tuple


class FigureBase(ABC):

    def __init__(self, color=0, direction=None, was_moved=False,
                 air_move=False, air_attack=False, stationary_attack=False, infinite_move=False):
        color = int(color)
        if direction is None:
            direction = color
        else:
            direction = int(direction)

        assert 0 <= direction <= 3, "Figure can be only move in 4 directions"

        self.color = color
        self.direction = direction
        self.was_moved = was_moved

        self.is_air_attack = air_attack
        self.is_air_move = air_move
        self.is_attack_stationary = stationary_attack
        self.is_move_infinite = infinite_move

        self._move_pattern = None
        self._attack_pattern = None
        self._specials = None

    def move(self):
        self.was_moved = True

    def clear_special_attr(self):
        pass

    @property
    def move_pattern(self):
        return self._move_pattern

    @property
    def attack_pattern(self):
        return self._attack_pattern

    @property
    def specials(self):
        return self._specials

    @staticmethod
    def rotate_pattern(ptrn, right=True):
        named = get_right_tuple(ptrn[0])
        if right:
            rotated_ptrn = (named(y, -x) for x, y in ptrn)
        else:
            rotated_ptrn = (named(-y, x) for x, y in ptrn)

        return rotated_ptrn

    @staticmethod
    def flip_x_pattern(ptrn):
        named = get_right_tuple(ptrn[0])
        return tuple(named(-x, y) for x, y in ptrn)

    @staticmethod
    def flip_y_pattern(ptrn):
        named = get_right_tuple(ptrn[0])
        return tuple(named(x, - y) for x, y in ptrn)

    @abstractproperty
    def name(self):
        return "BaseFigure"

    def __str__(self):
        return f"{self.name}: Fly:{str(self.is_air_move)[0]}, " \
               f"Inf:{str(self.is_move_infinite)[0]}, " \
               f"C:{self.color};"

    def __repr__(self):
        return str(self)


class SpecialBase(ABC):
    """
    Base for special moves, unconventional.
    """

    def __init__(self):
        self.patterns = None
        self._named_tup = namedtuple(self.name, field_names=["X", "Y"])

    @abstractproperty
    def name(self):
        pass

    @property
    def named_tup(self):
        return self._named_tup

    @abstractmethod
    def is_valid(self, board, f1, f2):
        pass

    @abstractmethod
    def apply(self, board, f1, f2):
        pass

    def counter_check(self):
        pass

    def rotate_this(self, right=True):
        if right:
            self.patterns = (self.named_tup(y, -x) for x, y in self.patterns)
        else:
            self.patterns = (self.named_tup(-y, x) for x, y in self.patterns)

    def flip_this_by_x(self):
        self.patterns = tuple(self.named_tup(-x, y) for x, y in self.patterns)

    def flip_this_by_y(self):
        self.patterns = tuple(self.named_tup(x, - y) for x, y in self.patterns)

    def __str__(self):
        return f"{self.patterns}"

    def __repr__(self):
        return str(self)


class BoardBase(ABC):
    """
    State and pieces on the board
    """

    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.figs_on_board = dict()
        # self.figures = dict()

    # @abstractmethod
    def clear_board(self):
        self.__init__()

    # @abstractmethod
    def add_figure(self, field, fig):
        if field in self.figs_on_board:
            raise ValueError(f"There is figure on this {self.figs_on_board[field]}")
        else:
            self.figs_on_board[field] = fig

    def move_figure(self, field1, field2):
        fig = self.figs_on_board.pop(field1)
        fig.move()
        self.figs_on_board[field2] = fig

    def remove_figure(self, pos: Tuple):
        del self.figs_on_board[pos]

    def get(self, key):
        return self.figs_on_board.get(key, None)

    def change_fig(self, field, fig):
        self.figs_on_board[field] = fig

    def print_table(self, justify=8, flip=False):
        if flip:
            rang = range(8)
        else:
            rang = range(7, -1, -1)

        print("Board:")
        for y in rang:
            for x in range(8):
                fig = self.figs_on_board.get((x, y), None)
                if fig:
                    text = fig.name
                else:
                    text = ''

                text = text.center(justify)
                print(f"{text}", end='')
            print()


class GameModeBase(ABC):
    def __init__(self):
        self.board = BoardBase()
        self.players_num = 2
        self.current_player_turn = 0
        self.last_hit = 0
        self.move_count = 0
        self._move_checker = FigMoveAnalyzer()

    def make_move(self, f1, f2):
        self._resolve_action(f1, f2)

    @abstractmethod
    def _post_move_actions(self, field2):
        pass

    def _is_move_valid(self, f1, f2):
        print(f"\n\nChecking: {f1}->{f2}")
        check = self._move_checker.check(self, self.board, f1, f2)
        return check or self._move_checker.can_special

    def _resolve_action(self, f1, f2):
        is_ok = self._move_checker.check(self, self.board, f1, f2)
        print()
        print(f"is ok: {is_ok}, {f1}, {f2}")
        print(f"spec: {self._move_checker.can_special}")
        tmp_brd = deepcopy(self.board)
        if is_ok:
            self.board.move_figure(f1, f2)
            self._post_move_actions(f2)
        elif self._move_checker.can_special:
            spc = self._move_checker.spc
            spc.apply(self.board, f1, f2)
        else:
            raise ValueError("Incorrect move")

        if self.check_rules_for(self.current_player_turn):
            "Its ok"
        else:
            self.board = tmp_brd
            raise ValueError(f"Invalid move!{f1} to {f2}. reverting board")

        self.current_player_turn = (self.current_player_turn + 1) % self.players_num

    @abstractmethod
    def check_rules_for(self, color):
        pass

    # if self._is_move_valid(field1, field2):
    #     self.board.move_figure(field1, field2)
    #
    #     self._post_move_actions(field2)
    #
    # else:
    #     raise ValueError("Not valid move")

    @abstractmethod
    def get_proper_figure(self, name, color):
        pass

    @abstractmethod
    def _is_promotion(self, field):
        pass

    @abstractmethod
    def get_promotion_fig(self, color):
        return None

    def strings_to_tuple(self, *moves):
        pass

    def new_game(self):
        self.__init__()

    def load_fen(self, fen: str):
        raise NotImplementedError

    def export_fen(self):
        raise NotImplementedError

    def export_game_history(self):
        raise NotImplementedError


class FigMoveAnalyzer:
    def check(self, game: GameModeBase, board: BoardBase, f1: move_tuple, f2: move_tuple):
        self.game = game
        self.board = board
        self.move_reach = False
        self.attack_reach = False
        self.f1 = f1
        self.f2 = f2
        self.can_special = False
        self.spc = None

        return self._is_move_valid(f1, f2)

    def _is_move_valid(self, f1, f2):
        move = f2[0] - f1[0], f2[1] - f1[0]
        fig1 = self.board.get(f1)
        target = self.board.get(f2)

        "Check if figure is here"
        if fig1 is None:
            return False

        "Wrong figure, Turn for other player"
        if self.game.current_player_turn != fig1.color:
            return False

        reach = self._can_fig_reach(f1, f2)
        can_move = self._can_fig_move(fig1, target)
        can_attack = self._can_fig_attack(fig1, target)
        print(f"reach:{reach}, can_mv: {can_move}, can_atk:{can_attack}")
        print(self.attack_reach, self.move_reach)

        if target is not None and can_attack and self.attack_reach:
            return True
        elif target is None and can_move and self.move_reach:
            return True

        self._can_fig_special(fig1, f1, f2)
        return False
        # if target is None:
        #     return self.move_reach
        # else:
        #     if target.color == fig.color:
        #         return False
        #     return self.attack_reach

    @staticmethod
    def _can_fig_attack(fig: FigureBase, target: FigureBase):
        if target is None:
            return False
        if fig.color != target.color:
            return True
        else:
            return False

    @staticmethod
    def _can_fig_move(fig: FigureBase, target: FigureBase):
        if target is None:
            return True

    def _can_fig_reach(self, f1, f2):
        move = f2[0] - f1[0], f2[1] - f1[1]
        fig = self.board.get(f1)

        # move_diag = abs(move[0]) == abs(move[1])
        # move_lin = move[0] == 0 or move[1] == 0
        direction = tuple(np.sign(np.array(move)))
        dist = max((abs(move[0]), abs(move[1])))
        # print(f"from: {f1} to {f2}")
        # print(f"move: {move}")
        # print(f"Dist: {dist}")

        if dist == 1:
            if move in fig.move_pattern:
                self.move_reach = True

            if move in fig.attack_pattern:
                self.attack_reach = True
            return True

        # print(fig)
        # print("infi:", fig.is_move_infinite)
        if fig.is_move_infinite:
            if fig.is_air_move and direction in fig.move_pattern:
                self.move_reach = True
            elif direction in fig.move_pattern:
                tmp_move = (0, 0)
                while True:
                    # print("loop")
                    tmp_move = tmp_move[0] + direction[0], tmp_move[1] + direction[1]
                    is_fig = self.board.get(tmp_move)
                    if tmp_move == move:
                        self.move_reach = True
                        break
                    if is_fig is not None:
                        self.move_reach = False
                        break
            else:
                raise ValueError(f"This is not valid move to long pattern: {move}")

            if fig.is_air_attack and direction in fig.attack_pattern:
                self.attack_reach = True
            elif direction in fig.attack_pattern:
                tmp_move = (0, 0)
                while True:
                    tmp_move = tmp_move[0] + direction[0], tmp_move[1] + direction[1]
                    is_fig = self.board.get(tmp_move)
                    if tmp_move == move:
                        self.attack_reach = True
                        break
                    if is_fig is not None:
                        self.attack_reach = False
                        break
            else:
                raise ValueError(f"This is not valid move to long pattern: {move}")

        else:
            return False

        if self.move_reach or self.attack_reach:
            return True

    def _is_team_checked(self, color):
        pass

    def _can_fig_special(self, fig: FigureBase, f1, f2):
        print("\nChecking specials")
        # print(fig)
        # print(fig.specials)

        if fig.specials is not None:
            for spc in fig.specials:
                print(f"Checking: {spc}")
                valid = spc.is_valid(self.board, f1, f2)
                if valid:
                    print(f"valid {valid}")
                    self.can_special = True
                    self.spc = spc
                    return True

    def _is_game_over(self):
        pass
