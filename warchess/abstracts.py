from abc import ABC, abstractmethod, abstractproperty
from collections import namedtuple
from copy import deepcopy

from typing import Any, Tuple, List, AnyStr, Union, Iterable
from warnings import warn

# from classes import King

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


class InvalidMove(Exception):
    """Main Exceptions for all wrong moves"""
    pass
    # def __init__(self):
    #     pass


class IncorrectTurn(InvalidMove):
    pass


class InvalidBoardIndexes(InvalidMove):
    pass


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

    @abstractproperty
    def symbol(self):
        return "BF"

    def __str__(self):
        return f"{self.name}: Fly:{str(self.is_air_move)[0]}, " \
               f"Inf:{str(self.is_move_infinite)[0]}, " \
               f"C:{self.color};"

    def __repr__(self):
        return str(self)


"""
Problem that I must solve:
    - How to apply variant
    - How to check requirements for more
    - How to rotate/flip patterns
    - How to revert special
    - How to modify other pieces
    - How to revert other pieces
    - How to save move
    - Distinguish variant from all moves
"""


class Position:
    pos_keys = [
            'relative', 'relative_f1', 'relative_f2',
            'absolute', 'classic', 'any'
    ]
    relatives = ['relative', 'relative_f1', 'relative_f2']

    def __init__(self, key: str, pos):
        """
        Orientation

            0
          3   1
            2
        Args:
            key:
            pos:
        """

        key = key.lower()
        self.key = key
        if isinstance(pos, str):
            pass
        self.pos = pos
        self._ccp = None

        self.orientation = 0  # Up white

        assert key in self.pos_keys, f"This key is not valid for pos: {key}"

    @property
    def ccp(self):
        return self._ccp

    @ccp.setter
    def ccp(self, new_val):
        self._ccp = new_val

    def get_ccp(self, board=None):

        if self._ccp:
            return self._ccp

        if self.key in ['relative', 'relative_f1', 'relative_f2']:
            ccp = self.pos
        elif self.key == 'absolute':
            raise NotImplementedError("Only classic board is supported")
        else:
            "Classic"
            x, y = self.pos
            ccp = x - 4, y - 4

        self._ccp = ccp
        return ccp

    def rotate_this(self, board, clockwise=True):
        pos = self.pos
        if self.key in ['relative', 'relative_f1', 'relative_f2']:
            "Relative moves do not need board. Center always in 0,0"
            h, w = 0, 0
        else:
            h, w = board.height, board.width
            h -= 1
            w -= 1

        x, y = pos
        if clockwise:
            new_pos = (y, h - x)
        else:
            new_pos = (w - y, x)

        # assert x >= 0 and y >= 0, f"X and Y should be >=0, but got x:{x} y:{y}"

        self.pos = new_pos

    def flip_this_by_x(self, board):
        x, y = self.pos

        if self.key in ['relative', 'relative_f1', 'relative_f2']:
            "Relative moves do not need board. Center always in 0,0"
            w = 0
        else:
            w = board.width-1

        new_pos = (w - x, y)
        x, y = new_pos
        # assert x >= 0 and y >= 0, f"X and Y should be >=0, but got x:{x} y:{y}"
        self.pos = new_pos

    def flip_this_by_y(self, board):
        x, y = self.pos
        if self.key in ['relative', 'relative_f1', 'relative_f2']:
            "Relative moves do not need board. Center always in 0,0"
            h = 0
        else:
            h = board.height-1

        new_pos = (x, h - y)
        x, y = new_pos
        # assert x >= 0 and y >= 0, f"X and Y should be >=0, but got x:{x} y:{y}"
        self.pos = new_pos

    def get_position(self, f1, f2):
        pos_x, pos_y = self.pos

        if self.key == 'relative' or self.key == 'relative_f1':
            x, y = f1
            pos = x + pos_x, pos_y + y
            return pos

        elif self.key == 'relative_f2':
            xx, yy = f2
            pos = xx + pos_x, yy + pos_y
            return pos

        elif self.key == 'classic':
            return self.pos
        elif self.key == 'absolute':
            return self.pos
        else:
            raise NotImplementedError(f"Mode does not match: {self.key}")


class PositionValidator(Position):

    def is_position_valid(self, f1, f2):
        pass

        self.get_position()


class RequiredFig:
    """
    Key 0/None = Any
    Key -1 Same
    Key -2 Opposite
    """
    keys = {
            "any": 0,
            "same": -1,
            "other": -2,
            "enemy": -2,
            "opposite": -2,
            "None": -3,
            "none": -3,
    }
    inv_keys = {v: k for k, v in keys.items()}

    def __init__(self,
                 req_team=0, req_color=0, req_type=0,
                 req_status=None,
                 pos: tuple = None,
                 ):

        self.req_team = req_team
        self.req_color = req_color
        self.req_type = req_type

        if req_status:
            assert isinstance(req_status, (dict,)), f"Status must be dict, but got {type(req_status)}"
            self.req_status = req_status
        else:
            self.req_status = {}

        k, p = pos
        self.req_pos = Position(k, p)

    def check_pos(self, board, posf1, posf2):
        pass

    def get_key_val(self, key):
        return self.keys.get(key)


#
# req_rush_r = RequiredFig(
#         req_type="P", req_status={"rushed": True},
#         pos=('relative_f1', (1, 0)), req_team=RequiredFig.keys['enemy']
# )
# req_rush_r = RequiredFig(
#         req_type="P", req_status={"rushed": True},
#         pos=('relative_f1', (1, 0)), req_team=RequiredFig.keys['enemy']
# )


class SpecialVariantBase:
    def __init__(self):
        self.pattern = None
        self.offset = (0, 0)  # Change when board is bigger or smaller

        "For check checking"
        self.block = None
        self.ignore = None

    def is_var_valid(self, n):
        pass

    def apply_var(self, n):
        pass

    def timed_status(self):
        pass


class Rush(SpecialVariantBase):
    def __init__(self):
        super().__init__()

        self.pattern = PositionValidator('relative', (0, 2))


class SpecialBase(ABC):
    """
    Base for special moves, unconventional.
    """

    def __init__(self):
        self.variants = []
        self._named_tup = namedtuple(self.name, field_names=["X", "Y"])

    @abstractproperty
    def name(self):
        pass

    @property
    def named_tup(self):
        """
        General tuple for move patterns
            Tuple(X, Y)
        """
        return self._named_tup

    @abstractmethod
    def is_valid(self, game, board, f1, f2):
        pass

    @abstractmethod
    def apply(self, game, board, f1, f2):
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


class TranslatorIndexString:
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height

    def text_to_int(self, text):
        x, y = text.upper()
        y = int(y) - 1
        x = ord(x) - 65  # a=97, A=65

        if x < 0 or y < 0:
            raise InvalidBoardIndexes("Field index is under 0!")
        if x >= self.width or y >= self.height:
            raise InvalidBoardIndexes(f"Field index is too high: x:{x} y:{y}")
        return x, y

    def int_to_text(self, x, y):
        if x < 0 or y < 0:
            raise InvalidBoardIndexes("Field index is under 0!")
        if x >= self.width or y >= self.height:
            raise InvalidBoardIndexes(f"Field index is too high: x:{x} y:{y}")

        X = chr(x + 65)
        Y = str(y + 1)
        field_str = f"{X}{Y}"
        return field_str


class BoardBase(ABC):
    """
    State and pieces on the board
    """

    def __init__(
            self, width=8, height=8,
            left=0, right=0, bottom=0, top=0,
            gap_vertical=0, gap_horizontal=0
    ):
        self.width = width
        self.height = height
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.gap_vertical = gap_vertical
        self.gap_horizontal = gap_horizontal

        self.figs_on_board = dict()
        self.teams = self._empty_2d_dict(2)
        self.colors = self._empty_2d_dict(2)
        self.translator = TranslatorIndexString(width=width, height=height)

    def _empty_2d_dict(self, n=2):
        """Creates N dictionaries"""
        return {num: dict() for num in range(n)}

    @property
    def columns(self):
        letters = [chr(65 + n) for n in range(self.width)]
        return "".join(letters)

    @property
    def rows(self):
        letters = [n + 1 for n in range(self.height)]
        return "12345678"

    def add_figure(self, field, fig):
        if field in self.figs_on_board:
            raise ValueError(f"There is figure on this {self.figs_on_board[field]}")
        else:
            color = fig.color
            team = fig.team
            self.figs_on_board[field] = fig
            self.colors[color][field] = fig
            self.teams[team][field] = fig

    def clear_board(self):
        for pos, fig in self:
            self.remove_figure(pos)

    def __iter__(self):
        """
        Returns copy of board figures
        {pos: fig}
        """
        return iter(self.figs_on_board.copy().items())

    def change_fig(self, field, fig):
        """
        Put this fig on that field
        Args:
            field:
            fig:

        Returns:

        """
        color = fig.color
        team = fig.team
        self.figs_on_board[field] = fig
        self.colors[color][field] = fig
        self.teams[team][field] = fig

    def remove_figure(self, pos: Tuple):
        """
        Remove fig from pos.
        Args:
            pos:

        Returns:
            removed fig

        """
        fig = self.figs_on_board[pos]
        color = fig.color
        team = fig.team
        fig = self.figs_on_board.pop(pos)
        fig2 = self.teams[team].pop(pos)
        fig3 = self.colors[color].pop(pos)
        assert fig == fig2 == fig3, "Figures should be the same"
        return fig

    def move_figure(self, field1, field2):
        fig = self.remove_figure(field1)
        self.change_fig(field2, fig)
        fig.move()

    def get(self, *ks):
        """
        Get Figure from board
        Args:
            *ks:

        Returns:

        """
        if len(ks) == 1:
            ks = ks[0]
            return self._get(ks)
        elif len(ks) == 2:
            return self._get(tuple(ks))
        else:
            raise ValueError("Invalid key to get board")

    def _get(self, key):
        return self.figs_on_board.get(key, None)

    def print_board(self, *a, **kw):
        self.print_table(*a, **kw)

    @property
    def fields(self):
        for x in range(self.width):
            for y in range(self.height):
                color = (x + y) % 2
                yield (x, y), color

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

    def string_to_index(self, field):
        return self.translator.text_to_int(field)

    def index_to_str(self, x, y):
        return self.translator.int_to_text(x, y)


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
        self.kings = {num: dict() for num in range(self.players_num)}
        self._move_checker = FigMoveAnalyzer(self)
        self.ignore_turn = False

    def make_move_from_str(self, *args):
        """Confert keys to ints and call make_move"""
        pos = self.strings_to_ints(*args)
        ret = self.make_move(pos)
        return ret

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

        ret = self._resolve_action(f1, f2)
        return ret

    def _post_move_actions(self, field2):
        """
        Apply changes to board after player move in same turn,
        promotion or other.
        """
        pass

    def _post_special_actions(self, field2):
        pass

    def _is_move_valid(self, f1, f2):
        """
        Use checker object to check if move was valid.
        Args:
            f1:
            f2:

        Returns:

        """
        check = self._move_checker.check(f1, f2)
        return check or self._move_checker.ret['can_special']

    def _resolve_action(self, f1, f2):
        is_ok = self._move_checker.check(f1, f2)
        ret = self._move_checker.ret
        tmp_brd = deepcopy(self.board)
        if is_ok:
            if ret['valid']:
                self.board.move_figure(f1, f2)
                self._post_move_actions(f2)
            elif ret['can_special']:
                spc = self._move_checker.ret['spec']
                spc.apply(self, self.board, f1, f2)
                self._post_special_actions(f2)
            else:
                raise InvalidMove()
        else:
            # print(
            raise InvalidMove(f"Move: {f1} -> {f2} ({self.ints_to_strings(f1, f2)}): {ret}")

        if self.extra_move_rules(self.current_player_turn):
            "Its ok"
        else:
            self.board = tmp_brd
            raise ValueError(f"Invalid move!{f1} to {f2}. reverting board")

        self.current_player_turn = (self.current_player_turn + 1) % self.players_num
        return True

    def under_threat(self, field=None, fields=None,
                     defending: int = None, attacking=None,
                     mode='any_field', minimal_attacks=1
                     ):
        """
        Calls move analyzer object.
        Args:
            field:
            fields:
            defending: int: color or team that is defending position
            mode:
                @ 'any_fields' return True if any field is under threat
                @ `all` return True if all fields are under threat
                @ 'cover' return True if friendly is covering
                @ 'until' return True if there is `>= minimal_attacks`
                count_attackers
        Returns:

        """
        ret = self._move_checker.under_threat(
                field=field, fields=fields,
                defending=defending, attacking=attacking,
                mode=mode, minimal_attacks=minimal_attacks
        )
        return ret

    def extra_move_rules(self, moving_color):
        """
        Valid
        Args:
            moving_color:

        Returns:

        """
        return True

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

    def strings_to_ints(self, *arrs):
        """
        Field positions notations example: "E1" -> (0, 4)
        Translate any number of string into int tuples
        Args:
            *arrs:

        Returns:
            tuple(moves)

        """
        if len(arrs) == 1:
            if isinstance(arrs[0], (List, Tuple)):
                arrs = arrs[0]
            else:
                return self.board.string_to_index(arrs[0])

        out = []
        for move in arrs:
            x, y = self.board.string_to_index(move)
            out.append((x, y))
        return out

    def ints_to_strings(self, *arrs):
        """Use positional arguments for multiple positions"""
        if isinstance(arrs[0], (list, tuple, move_tuple, np.ndarray)):
            out = [self.board.index_to_str(x, y) for x, y in arrs]
            if len(out) == 1:
                return out[0]
            return out

        elif len(arrs) == 1:
            x, y = arrs
            return self.board.index_to_str(x, y)

        else:
            raise ValueError(f"Unrecognized type: {type(arrs[0])}")

    def new_game(self):
        self.__init__()

    def load_fen(self, fen: str):
        raise NotImplementedError

    def export_fen(self):
        raise NotImplementedError

    def export_game_history(self):
        raise NotImplementedError


class FigMoveAnalyzer:
    def __init__(self, game):
        # print(f"Fig Move analyzer initi \n" * 2)
        # print(type(game))
        # print(type(board))
        self.game = game
        self.ret = {
                'valid': None, 'spec': None, 'is_self_check_after': None,
                'can_special': False,
        }

    @property
    def board(self):
        return self.game.board

    def check(
            self, f1: move_tuple, f2: move_tuple,
            ignore_check=False,
    ):

        self.ret = {
                'valid': None, 'spec': None, 'is_self_check_after': None,
                'can_special': False,
        }
        assert isinstance(f1, (move_tuple, tuple)), "F1 has to be move_tuple"
        assert isinstance(f2, (move_tuple, tuple)), "F2 has to be move_tuple"

        return self._is_move_valid(f1, f2, ignore_check=ignore_check)

    def _is_move_valid(self, f1, f2, ignore_check=False):
        fig = self.board.get(f1)
        target = self.board.get(f2)

        "Check if figure is here"
        if fig is None:
            self.ret['valid'] = False
            return False

        "Wrong figure, Turn for other player"
        if self.game.current_player_turn != fig.color and not self.game.ignore_turn:
            self.ret['valid'] = False
            raise IncorrectTurn(f"Turn is now for: {self.game.current_player_turn}")

        move_reach, attack_reach = self._can_fig_reach(fig, f1, f2)
        can_move = self._can_fig_move(fig, target)
        can_attack = self._can_fig_attack(fig, target)

        if not ignore_check:
            is_check_after_move = self._check_consequences(fig.team, f1, f2)

            if is_check_after_move:
                self.ret['check_after_move'] = True
                return False

        if target is None and can_move and move_reach:
            self.ret['valid'] = True
            return True
        if target is not None and can_attack and attack_reach:
            self.ret['valid'] = True
            return True

        "If no move or no attack, check specials"
        ret = self._can_fig_special(fig, f1, f2)
        return ret

    @staticmethod
    def _can_fig_attack(fig: FigureBase, target: FigureBase, ignore=None):
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
    def args_for_reach_checking(fig, f1, f2, *a):
        move = f2[0] - f1[0], f2[1] - f1[1]

        direction = tuple(np.sign(np.array(move)))
        dist = max((abs(move[0]), abs(move[1])))
        return fig, move, direction, dist, f1, f2, *a

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

    def can_fig_reach_attack(self, board, fig, f1, f2, ignore=None, block=None):
        """Main function, to check reach, cals sub _name"""
        # self.board = board
        args = self.args_for_reach_checking(fig, f1, f2, ignore, block)
        return self._can_fig_reach_attack(*args)

    def _can_fig_reach_attack(
            self, fig, move, direction, dist, f1, f2, ignore=None, block=None
    ):
        if dist <= 0:
            return False
        if dist == 1:
            if move in fig.attack_patterns:
                return True

        if fig.is_attack_infinite:
            if fig.is_air_attack and direction in fig.attack_patterns:
                return True
            elif direction in fig.attack_patterns:
                fields = self._infinite_reach_checker(
                        f1, direction, f2,
                        ignore=ignore, block=block
                )
                if f2 in fields:
                    return True
                else:
                    return False
        else:
            if fig.is_air_attack and move in fig.attack_patterns:
                return True
            else:
                return False

    def infinite_reach_checker(self, f1, f2):
        """Main function for checking reach, calls sub fuction _<name>"""
        # self.game = game
        # self.board = board
        fig = self.board.get(f1)
        args = self.args_for_reach_checking(fig, f1, f2)
        return self._infinite_reach_checker(*args)

    def _infinite_reach_checker(
            self, start, direction, end=None,
            ignore=None, block=None):
        """Iteration function, checking board in one direction"""
        x, y = start
        valid_moves = []
        if ignore:
            ig_x, ig_y = ignore
        else:
            ig_x, ig_y = None, None
        if block:
            bl_x, bl_y = block
        else:
            bl_x, bl_y = None, None

        its = 0
        while True and its < 100:
            its += 1
            x = x + direction[0]
            y = y + direction[1]

            if x == ig_x and y == ig_y:
                "Ignore current position"
                continue

            if x == bl_x and y == bl_y:
                "Position after move will block"
                break

            tmp_move = x, y
            is_fig = self.board.get(tmp_move)

            if x < 0 or y < 0:
                break
            elif x >= self.board.width or y >= self.board.height:
                break

            "If End, and it reach end pos then break"
            if end and tmp_move == end:
                valid_moves.append(tmp_move)
                break

            elif is_fig is not None:
                valid_moves.append(tmp_move)
                break
            else:
                valid_moves.append(tmp_move)
        return valid_moves

    def under_threat(
            self, field=None, fields=None,
            defending: int = None, attacking=None,
            mode='any_field', minimal_attacks=1,
            ignore=None, block=None,
    ):
        """
        Args:
            field:
            fields:
            defending: int: color or team that is defending position
            mode:
                @ 'any_field' return True if any field is under threat
                @ `all` return True if all fields are under threat
                @ 'cover' return True if friendly is covering
                @ 'until' return True if there is `>= minimal_attacks`
                count_attackers
            ignore: used only for any_field
            block: used only for any_field
        Returns:

        """

        defending_team = None
        attacking_color = None

        "Input checking"
        if field is None and fields is None:
            raise ValueError("Specify field or fields!")
        elif mode not in ['any_field', 'all_fields', 'cover', 'count_attackers']:
            raise ValueError(f"Specify correct mode, not: {mode}")
        elif field is not None and fields is not None:
            raise ValueError("Specify only field or fields, not both.")

        fig = self.board.get(field)
        if defending is None and attacking is None:
            if field:
                if fig is None:
                    raise ValueError(f"Field {field} has no fig, specify 'defending' team")
                else:
                    defending_team = fig.color
            else:
                raise ValueError("Specify 'defending' team when using 'fields'")
        elif type(attacking) is int:
            defending_team = None
            attacking_color = attacking

        elif type(defending) is not int:
            raise ValueError(f"defending should be int, but got: {type(defending)}")

        elif defending is not None:
            defending_team = defending
            attacking_color = None

        if mode == "cover":
            "Change cover to attacking 'any_field'"
            mode = "any_field"
            minimal_attacks = 1
            attacking_color = defending_team
            defending_team = None

        if field:
            positions_to_check = [field]
        else:
            positions_to_check = fields

        if mode == "any_field":
            attacks_num = 0
            pool = self.board.colors if attacking_color is not None else self.board.teams
            for pool_id, team in pool.items():
                if defending_team is not None and pool_id == defending_team:
                    continue
                if attacking_color is not None and pool_id != attacking_color:
                    continue

                for target in positions_to_check:
                    reach = self._check_figures_reach(
                            team, target, 1,
                            ignore=ignore, block=block,
                    )
                    if reach:
                        attacks_num += 1
                        if attacks_num >= minimal_attacks:
                            return True

        elif mode == "all_fields":
            attacks_num = 0
            minimal_attacks = len(positions_to_check)
            for target in positions_to_check:
                for team_id, team in self.board.teams.items():
                    if team_id == defending_team:
                        continue

                    reach = self._check_figures_reach(
                            team, target, 1,
                            ignore=ignore, block=block,
                    )
                    if reach:
                        attacks_num += 1
                        if attacks_num >= minimal_attacks:
                            return True
                        break

            warn("Temporary checking: num>len")
            if attacks_num == len(positions_to_check):
                return True
            elif attacks_num > len(positions_to_check):
                raise ValueError(f"How there is more attacks? {attacks_num}")
            else:
                return False

    def _check_figures_reach(self, fig_dict, target, min_n=1, ignore=None, block=None):
        attacks = 0
        for pos, fig in fig_dict.items():
            if pos == block:
                continue
            attack_reach = self.can_fig_reach_attack(
                    self.board, fig, pos, target,
                    ignore=ignore, block=block,
            )
            if attack_reach:
                attacks += 1
                if attacks >= min_n:
                    return True

    @abstractmethod
    def _check_consequences(self, team, f1, f2):
        """
        Function analyze if team will be checked after fig move f1 -> f2
        Args:
            team:
            f1:
            f2:

        Returns:

        """

        kings = [
                (pos, fig) for pos, fig in self.board.figs_on_board.items() if fig.name == "King" and fig.color == team
        ]

        th = False
        for p, k in kings:
            if p == f1:
                th = self.under_threat(field=f2, defending=k.team, ignore=f1)
            else:
                th = self.under_threat(field=p, ignore=f1, block=f2)
            # th = self.under_threat(field=p, ignore=f1, block=f2)

            if th:
                break

        return th

    def _can_fig_special(self, fig: FigureBase, f1, f2):
        if fig.specials is not None:
            for spc in fig.specials:
                valid = spc.is_valid(self.game, self.board, f1, f2)
                if valid:
                    self.ret['spec'] = spc
                    self.ret['can_special'] = True
                    return True
        return False

    @abstractmethod
    def _is_game_over(self):
        pass
