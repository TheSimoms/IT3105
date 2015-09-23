from numpy.random import choice
from numpy import add

from math import log

from copy import deepcopy

from modules.module_four.ui import Ui
from modules.module_four.game_board import GameBoard


EVAL_WEIGHTS = {
    'empty': 2.7,
    'max': 1.0,
    'smooth': 0.1,
    'mono': 1.0
}


class TwentyFortyEight:
    def __init__(self, height=800):
        self.game_board = GameBoard()
        self.ui = Ui(height)

    def get_next_player_move(self):
        pass

    def evaluate_state(self):
        number_of_empty_cells = self.game_board.get_number_of_empty_cells()

        return \
            log(number_of_empty_cells * EVAL_WEIGHTS['empty']) +\
            self.game_board.get_max_value() * EVAL_WEIGHTS['max'] +\
            self.game_board.smoothness() * EVAL_WEIGHTS['smooth'] +\
            self.game_board.monotonicity() * EVAL_WEIGHTS['mono']

    def evaluate_player_move(self, depth, alpha, beta, positions, cut_offs):
        best_move = -1
        best_score = alpha
        result = None

        for direction in self.game_board.directions:
            game_board = self.game_board.clone()

    def evaluate_computer_move(self, depth, alpha, beta, positions, cut_offs):
        best_move = -1
        best_score = beta
        result = None

    def search(self, depth, alpha, beta, positions, cut_offs, is_player_turn):
        return \
            self.evaluate_player_move(depth, alpha, beta, positions, cut_offs) if is_player_turn else \
            self.evaluate_computer_move(depth, alpha, beta, positions, cut_offs)
