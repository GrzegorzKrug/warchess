from abc import ABC, abstractmethod, abstractproperty
from collections import namedtuple
from itertools import product

from abstracts import FigureBase, SpecialBase, attack_tuple, move_tuple


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
        self._move_pattern = (
                attack_tuple(0, 1),
                attack_tuple(1, 0),
                attack_tuple(0, -1),
                attack_tuple(-1, 0),
        )

    @property
    def name(self):
        return "Rook"


if __name__ == "__main__":
    p1 = Pawn(0)
    p2 = Pawn(1)

    # print(p1.color)
    # print(p2.color)
    #
    # print(p1.special)
    # print(p2.special)
    print(p1)
    print(p2)

    k1 = Knight(0)
    k2 = Knight(1)

    print(k1)
    print(k2)

    b1 = Bishop(0)
    b2 = Bishop(1)
    print(b1)
    print(b2)

    K1 = King(0)
    K2 = King(1)
    print(K1)
    print(K2)

    q1 = Queen(0)
    q2 = Queen(1)
    print(q1)
    print(q2)

    r1 = Rook(0)
    r2 = Rook(1)

    print(r1)
    print(r2)
# print(p2.was_moved)
