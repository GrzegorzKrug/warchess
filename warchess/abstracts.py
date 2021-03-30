from abc import ABC, abstractmethod, abstractproperty
from collections import namedtuple

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

    def __init__(self, color, direction=None, was_moved=False,
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
    def is_valid(self, context, move):
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
    State
    """

    def __init__(self):
        pass

    @abstractmethod
    def clear_board(self):
        pass

    @abstractmethod
    def add_figure(self):
        pass

    @abstractmethod
    def move_figure(self):
        pass


class GameBase(ABC):
    def __init__(self):
        pass

    def load_fen(self, fen):
        raise NotImplementedError

    def export_fen(self):
        raise NotImplementedError

    def export_game_history(self):
        raise NotImplementedError

    @abstractmethod
    def new_game(self, mode):
        pass


class CheckRulesBase(ABC):

    @abstractmethod
    def is_move_valid(self, some):
        pass

    @abstractmethod
    def is_game_over(self):
        pass
