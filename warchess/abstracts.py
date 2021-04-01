from abc import ABC, abstractmethod, abstractproperty
from collections import namedtuple

from typing import Any, Tuple, List, AnyStr, Union, Iterable

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
                 flying_move=False, stationary_attack=False, infinite_move=False):
        color = int(color)
        if direction is None:
            direction = color
        else:
            direction = int(direction)

        assert 0 <= direction <= 3, "Figure can be only move in 4 directions"

        self.color = color
        self.direction = direction
        self.was_moved = was_moved

        self.is_move_flying = flying_move
        self.is_attack_stationary = stationary_attack
        self.is_move_infinite = infinite_move

        self._move_pattern = None
        self._attack_pattern = None
        self._special = None

    def make_move(self):
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
    def special(self):
        return self._special

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
        return f"{self.name}: Fly:{str(self.is_move_flying)[0]}, " \
               f"Inf:{str(self.is_move_infinite)[0]}, " \
               f"C:{self.color};"

    @property
    def details(self):
        return f"{self.name}: Fly:{self.is_move_flying}, Inf:{self.is_move_infinite}, " \
               f"{self.move_pattern}, {self.attack_pattern}, Special moves: {self.special}"

    def __repr__(self):
        return str(self)


class SpecialBase(ABC):
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
        self.players = 2
        self.current_player_turn = 0
        self.last_hit = 0
        self.move_count = 0

    @abstractmethod
    def _is_move_valid(self, field1, field2):
        pass

    @abstractmethod
    def _can_fig_move(self, field1, field2):
        pass

    @abstractmethod
    def _is_game_over(self):
        pass

    def make_move(self, f1, f2):
        self.resolve_action(f1, f2)

    def resolve_action(self, field1, field2):
        if self._is_move_valid(field1, field2):
            self.board.move_figure(field1, field2)
            if self._is_promotion(field2):
                fig = self.get_promotion_fig(self.current_player_turn)
                self.board.change_fig(field2, fig)
            else:
                pass

        else:
            raise ValueError("Not valid move")

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

    @abstractmethod
    def _is_team_checked(self, color):
        pass

    def new_game(self):
        self.__init__()

    def load_fen(self, fen: str):
        raise NotImplementedError

    def export_fen(self):
        raise NotImplementedError

    def export_game_history(self):
        raise NotImplementedError
