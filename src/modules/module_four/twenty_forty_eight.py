import time

from math import log

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

        self.ui.update_ui(self.game_board.state)

        #time.sleep(1)

        while True:
            self.game_board.make_move('right')

            print('right')

            self.ui.update_ui(self.game_board.state)

            #time.sleep(1)

            self.game_board.make_computer_move()
            self.ui.update_ui(self.game_board.state)

            #time.sleep(1)

            self.game_board.make_move('down')

            print('down')

            self.ui.update_ui(self.game_board.state)

            #time.sleep(1)

            self.game_board.make_computer_move()
            self.ui.update_ui(self.game_board.state)

            #time.sleep(1)

            self.game_board.make_move('left')

            print('left')

            self.ui.update_ui(self.game_board.state)

            #time.sleep(1)

            self.game_board.make_computer_move()
            self.ui.update_ui(self.game_board.state)

            #time.sleep(1)

            self.game_board.make_move('up')

            print('up')

            self.ui.update_ui(self.game_board.state)

            #time.sleep(1)

            self.game_board.make_computer_move()
            self.ui.update_ui(self.game_board.state)

            #time.sleep(1)

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

            if game_board.make_move(direction):
                positions += 1

                if game_board.has_2048():
                    return {
                        'direction': direction,
                        'score': 10000,
                        'positions': positions,
                        'cut_offs': cut_offs
                    }

                twenty_forty_eight = TwentyFortyEight(game_board)

                if depth == 0:
                    result = {
                        'direction': direction,
                        'score': twenty_forty_eight.evaluate_state()
                    }
                else:
                    result = twenty_forty_eight.search(depth-1, best_score, beta, positions, cut_offs, False)

                    if result['score'] > 9900:
                        result['score'] -= 1

                    positions = result['positions']
                    cut_offs = result['cut_offs']

                if result['score'] > best_score:
                    best_score = result['score']
                    best_move = direction

                if best_score > beta:
                    cut_offs -= 1

                    return {
                        'direction': direction,
                        'score': beta,
                        'positions': positions,
                        'cut_offs': cut_offs
                    }

        return {
            'direction': best_move,
            'score': best_score,
            'positions': positions,
            'cut_offs': cut_offs
        }

    def evaluate_computer_move(self, depth, alpha, beta, positions, cut_offs):
        best_move = -1
        best_score = beta
        result = None

        candidate_states = []
        empty_cells = self.game_board.get_empty_cells()

        scores = {
            2: [],
            4: []
        }

    def search(self, depth, alpha, beta, positions, cut_offs, is_player_turn):
        return \
            self.evaluate_player_move(depth, alpha, beta, positions, cut_offs) if is_player_turn else \
            self.evaluate_computer_move(depth, alpha, beta, positions, cut_offs)
