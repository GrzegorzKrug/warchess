import numpy as np
import os
import time


class Engine:
    def __init__(self, board=None, rules=None):
        self.board = board if board is not None else BaseBoard
        self.rules = rules if rules is not None else BaseGameMode


class Timer:
    def __init__(
            self, n_players=2, start_time_sec=5 * 60, add_move_s=5,
            # start_mod = dict(), add_mod = dict(),
    ):
        self.n_players = n_players
        self.times = np.zeros(n_players, dtype=np.float32) + start_time_sec
        self.current_active = 0
        self.cur_timer = time.time()

        self.add_move_s = add_move_s
        self.times[self.current_active] -= self.add_move_s

    def activate(self, ind):
        self.times[self.current_active] -= time.time() - self.cur_timer - self.add_move_s
        self.cur_timer = time.time()
        self.current_active = ind

    def status(self):
        temp = self.times.copy()
        temp[self.current_active] -= time.time() - self.cur_timer
        return temp


class RulesStandard:
    force_check = True
    pawn_promote_distance = 8


class Stan:
    pass


class Tura:
    pass


class Spawner:
    pass


if __name__ == "__main__":
    np.set_printoptions(suppress=False)

    tm = Timer(add_move_s=1)
    for x in range(10):
        tm.activate(x % 2)
        print(tm.status())
        time.sleep(1)
