from abc import ABC, abstractmethod, abstractproperty
from collections import namedtuple
from copy import deepcopy

from typing import Any, Tuple, List, AnyStr, Union, Iterable
from warnings import warn

import numpy as np

# pattern_tuple = namedtuple("P", field_names=["X", "Y"])


move_tuple = namedtuple("Move", field_names=["X", "Y"])
attack_tuple = namedtuple("Atck", field_names=["X", "Y"])
special_tuple = namedtuple("Spec", field_names=["X", "Y"])


def get_same_tuple(tuplelike):
    if isinstance(tuplelike, move_tuple):
        return move_tuple
    elif isinstance(tuplelike, attack_tuple):
        return attack_tuple
    else:
        return special_tuple


class FigureBase(ABC):
    def __init__(self, color=0, team=None, face_direction=None, was_moved=False,
                 air_move=False, air_attack=False, stationary_attack=False,
                 inf_move=False, inf_attack=False):
        color = int(color)
        if face_direction is None:
            direction = color
        else:
            direction = int(face_direction)

        assert 0 <= direction <= 3, "Figure can be only move in 4 directions"

        self.color = color
        if team is None:
            self.team = color
        else:
            self.team = int(team)
        self.direction = direction
        self.was_moved = was_moved

        self.is_air_move = air_move
        self.is_move_infinite = inf_move

        self.is_air_attack = air_attack
        self.is_attack_infinite = inf_attack
        self.is_attack_stationary = stationary_attack

        self._move_patterns = None
        self._attack_patterns = None
        self._specials = None

    def move(self):
        self.was_moved = True

    @property
    def move_patterns(self):
        return self._move_patterns

    @property
    def attack_patterns(self):
        return self._attack_patterns

    @property
    def specials(self):
        return self._specials

    @staticmethod
    def rotate_pattern(ptrn, right=True):
        named = get_same_tuple(ptrn[0])
        if right:
            rotated = (named(y, -x) for x, y in ptrn)
        else:
            rotated = (named(-y, x) for x, y in ptrn)

        return rotated

    @staticmethod
    def flip_x_pattern(ptrn):
        named = get_same_tuple(ptrn[0])
        return tuple(named(-x, y) for x, y in ptrn)

    @staticmethod
    def flip_y_pattern(ptrn):
        named = get_same_tuple(ptrn[0])
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
    def is_valid(self, game, board, f1, f2):
        pass

    @abstractmethod
    def apply(self, game, board, f1, f2):
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

    def __init__(self, width=8, height=8, extra_width=0, extra_height=0, extra_gap=0):
        self.width = width
        self.height = height
        self.figs_on_board = dict()
        self.teams = self._empty_2d_dict(2)
        self.colors = self._empty_2d_dict(2)

    def _empty_2d_dict(self, n=2):
        return {num: dict() for num in range(n)}

    @property
    def columns(self):
        return "ABCDEFGH"

    def add_figure(self, field, fig):
        if field in self.figs_on_board:
            raise ValueError(f"There is figure on this {self.figs_on_board[field]}")
        else:
            color = fig.color
            team = fig.team
            self.figs_on_board[field] = fig
            self.colors[color][field] = fig
            self.teams[team][field] = fig

    def remove_figure(self, pos: Tuple):
        fig = self.figs_on_board[pos]
        color = fig.color
        team = fig.team
        fig = self.figs_on_board.pop(pos)
        fig2 = self.teams[team].pop(pos)
        fig3 = self.colors[color].pop(pos)
        print(fig, fig2, fig3)
        assert fig == fig2 == fig3, "Figure is not the same"
        return fig

    def clear_board(self):
        self.__init__()

    def move_figure(self, field1, field2):
        fig = self.remove_figure(field1)
        self.add_figure(field2, fig)
        fig.move()

    def change_fig(self, field, fig):
        """Replacement"""

        self.figs_on_board[field] = fig

    def get(self, key):
        return self.figs_on_board.get(key, None)

    def print_board(self, *a, **kw):
        self.print_table(*a, **kw)

    def print_table(self, justify=7, flip=False):
        if flip:
            rang = range(self.height)
        else:
            rang = range(self.height - 1, -1, -1)

        print("Board:")
        for y in rang:
            print(f"{y + 1:^3} ", end="")
            for x in range(8):
                fig = self.figs_on_board.get((x, y), None)
                if fig:
                    text = fig.name
                else:
                    text = ''

                # text = text.center(justify)
                text = f"{text:<{justify}}"

                print(f"{text}", end='')
            print()
        text = " " * 3 + ''.join([f"{let:^{justify}}" for let in self.columns])
        print(text)


class Action:
    def __init__(self, f1, f2, fig, spec=None, killed=None):
        self.f1 = f1
        self.f2 = f2
        self.spec = spec
        self.fig = fig
        self.killed = killed

    @property
    def fen_move_notation(self):
        if self.spec:
            return self.spec
        else:
            return str(self.fig)


class GameModeBase(ABC):
    def __init__(self):
        self.board = BoardBase()
        self.players_num = 2
        self.current_player_turn = 0
        self.last_hit = 0  # Moves from last hit
        self.move_count = 0  # Move counter
        self._move_checker = FigMoveAnalyzer()

    def make_move(self, *args):
        """

        Args:
            *args: 2 moves in 1 tuple
                or 2 moves in separate positional arguments

        Returns:

        """
        if len(args) == 2:
            f1, f2 = args
        else:
            f1, f2 = args[0]

        self._make_move(f1, f2)

    def _make_move(self, f1, f2):
        self._resolve_action(f1, f2)

    def _post_move_actions(self, field2):
        """
        Apply changes to board after player move in same turn,
        promotion or other.
        """
        pass

    def _post_special_actions(self, field2):
        pass

    def _is_move_valid(self, f1, f2):
        check = self._move_checker.check(self, self.board, f1, f2)
        return check or self._move_checker.can_special

    def _resolve_action(self, f1, f2):
        is_ok = self._move_checker.check(self, self.board, f1, f2)
        tmp_brd = deepcopy(self.board)
        if is_ok:
            self.board.move_figure(f1, f2)
            self._post_move_actions(f2)
        elif self._move_checker.can_special:
            spc = self._move_checker.spc
            spc.apply(self, self.board, f1, f2)
            self._post_special_actions(f2)
        else:
            raise ValueError("Incorrect move")

        if self.are_rules_ok(self.current_player_turn):
            "Its ok"
        else:
            self.board = tmp_brd
            raise ValueError(f"Invalid move!{f1} to {f2}. reverting board")

        self.current_player_turn = (self.current_player_turn + 1) % self.players_num

    def under_threat(self, field=None, fields=None, defending: int = None, mode='any'):
        """
        Check if
        Args:
            field:
            fields:
            defending: int: color or team that is defending position
            mode:
                `any` return True if any field is under threat
                `all` return True if all fields are under threat
                'cover' return True if friendly is covering

        Returns:

        """
        "Input checking"
        if field is None and fields is None:
            raise ValueError("Specify field or fields!")
        elif mode not in ['any', 'all', 'cover']:
            raise ValueError(f"Specify correct mode, not: {mode}")
        elif field is not None and fields is not None:
            raise ValueError("Specify only field or fields, not both.")

        if defending is None:
            if field:
                fig = self.board.get(field)
                if fig is None:
                    raise ValueError("Field is empty, specify 'defending' team")
                else:
                    defending = fig.color
            else:
                raise ValueError("Specify 'defending' team when using 'fields'")

        elif type(defending) is not int:
            raise ValueError(f"defending should be int, but got: {type(defending)}")

        fig = self.board.get(field)
        if fig is None and defending is None:
            raise ValueError("Field is empty, specify `defending` color.")

        elif defending is not None:
            defending_team = defending

        elif fig is not None:
            defending_team = fig.team
        else:
            raise ValueError("Else?")

        if field:
            positions_to_check = [field]
        else:
            positions_to_check = fields

        if mode == "any":
            for target in positions_to_check:
                for pos, fig in self.board.figs_on_board.items():
                    if fig.team != defending_team:
                        attack_reach = self._move_checker.can_fig_reach_attack(self.board, fig, pos, target)
                        if attack_reach:
                            return True

        elif mode == "cover":
            for target in positions_to_check:
                for pos, fig in self.board.figs_on_board.items():
                    if fig.team == defending_team:
                        attack_reach = self._move_checker.can_fig_reach_attack(self.board, fig, pos, target)
                        if attack_reach:
                            return True

        else:
            attacks_num = 0
            for target in positions_to_check:
                for pos, fig in self.board.figs_on_board.items():
                    if fig.team != defending_team:
                        attack_reach = self._move_checker.can_fig_reach_attack(self.board, fig, pos, target)
                        if attack_reach:
                            attacks_num += 1
            warn("Temporary checking: num>len")
            if attacks_num == len(positions_to_check):
                return True
            elif attacks_num > len(positions_to_check):
                raise ValueError("How there is more checks?")
            else:
                return False

    @abstractmethod
    def are_rules_ok(self, color):
        pass

    @abstractmethod
    def get_proper_figure(self, name, color):
        """
        Method for generating pices
        Args:
            name:
            color:

        Returns:

        """
        pass

    @abstractmethod
    def _is_promotion(self, field):
        pass

    @abstractmethod
    def get_promotion_fig(self, color):
        return None

    def strings_to_ints(self, *moves):
        """
        Field postions notations example: "E1" -> (0, 4)
        "Returns 2d tuple of given strings"
        Args:
            *moves:

        Returns:

        """
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
    def __init__(self):
        self.game = None
        self.board = None

    def check(self, game: GameModeBase, board: BoardBase, f1: move_tuple, f2: move_tuple):
        self.game = game
        self.board = board
        # self.move_reach = False
        # self.attack_reach = False
        # self.f1 = f1
        # self.f2 = f2
        self.can_special = False
        self.spc = None

        return self._is_move_valid(f1, f2)

    def _is_move_valid(self, f1, f2):
        fig = self.board.get(f1)
        target = self.board.get(f2)

        "Check if figure is here"
        if fig is None:
            return False

        "Wrong figure, Turn for other player"
        if self.game.current_player_turn != fig.color:
            return False

        move_reach, attack_reach = self._can_fig_reach(fig, f1, f2)
        can_move = self._can_fig_move(fig, target)
        can_attack = self._can_fig_attack(fig, target)
        # print(f"mv reach:{move_reach}, attk reach:{attack_reach}")

        if target is None and can_move and move_reach:
            return True
        if target is not None and can_attack and attack_reach:
            return True

        self._can_fig_special(fig, f1, f2)
        return False

    @staticmethod
    def _can_fig_attack(fig: FigureBase, target: FigureBase):
        if target is None:
            return False
        if fig.team != target.team:
            return True
        else:
            return False

    @staticmethod
    def _can_fig_move(fig: FigureBase, target: FigureBase):
        if target is None:
            return True

    def _can_fig_reach(self, fig, f1, f2):
        args = self.args_for_reach_checking(fig, f1, f2)
        fig, move, direction, dist, _, _ = args

        move_reach = self._can_fig_reach_move(*args)

        "If params are same, then reach is the same"
        if fig.is_move_infinite == fig.is_attack_infinite and \
                fig.is_air_move == fig.is_air_attack and \
                fig.move_patterns == fig.attack_patterns:
            attack_reach = move_reach
        else:
            attack_reach = self._can_fig_reach_attack(*args)

        return move_reach, attack_reach

    @staticmethod
    def args_for_reach_checking(fig, f1, f2):
        move = f2[0] - f1[0], f2[1] - f1[1]

        direction = tuple(np.sign(np.array(move)))
        dist = max((abs(move[0]), abs(move[1])))
        return fig, move, direction, dist, f1, f2

    def _can_fig_reach_move(self, fig, move, direction, dist, f1, f2):
        if dist == 1:
            if move in fig.move_patterns:
                return True

        if fig.is_move_infinite:
            if fig.is_air_move and direction in fig.move_patterns:
                return True
            elif direction in fig.move_patterns:
                fields = self._infinite_reach_checker(f1, direction, f2)
                if f2 in fields:
                    return True
                else:
                    return False
        else:
            "Air pattern moves"
            if fig.is_air_move and move in fig.move_patterns:
                return True
            else:
                return False

    def can_fig_reach_attack(self, board, fig, f1, f2):
        self.board = board
        args = self.args_for_reach_checking(fig, f1, f2)
        return self._can_fig_reach_attack(*args)

    def _can_fig_reach_attack(self, fig, move, direction, dist, f1, f2):
        if dist == 1:
            if move in fig.attack_patterns:
                return True

        if fig.is_attack_infinite:
            if fig.is_air_attack and direction in fig.attack_patterns:
                return True
            elif direction in fig.attack_patterns:
                fields = self._infinite_reach_checker(f1, direction, f2)
                if f2 in fields:
                    return True
                else:
                    return False
        else:
            if fig.is_air_attack and move in fig.attack_patterns:
                return True
            else:
                return False

    def infinite_reach_checker(self, game, board, f1, f2):
        self.game = game
        self.board = board
        fig = board.get(f1)
        args = self.args_for_reach_checking(fig, f1, f2)
        return self._infinite_reach_checker(*args)

    def _infinite_reach_checker(self, start, direction, end=None):
        x, y = start
        valid_moves = []
        its = 0
        while True and its < 100:
            its += 1
            x = x + direction[0]
            y = y + direction[1]
            tmp_move = x, y
            is_fig = self.board.get(tmp_move)

            if x < 0 or y < 0:
                break
            elif x >= self.board.width or y >= self.board.height:
                break

            if end and tmp_move == end:
                valid_moves.append(tmp_move)
                break

            elif is_fig is not None:
                valid_moves.append(tmp_move)
                break
            else:
                valid_moves.append(tmp_move)
        return valid_moves

    def _is_team_checked(self, color):
        pass

    def _can_fig_special(self, fig: FigureBase, f1, f2):

        if fig.specials is not None:
            for spc in fig.specials:
                valid = spc.is_valid(self.game, self.board, f1, f2)
                if valid:
                    self.can_special = True
                    self.spc = spc
                    return True

    def _is_game_over(self):
        pass
