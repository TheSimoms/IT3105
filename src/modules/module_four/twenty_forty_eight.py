import time

from math import log

from modules.module_four.game_board import GameBoard, Cell


EVAL_WEIGHTS = {
    'empty': 2.7,
    'max': 1.0,
    'smooth': 0.1,
    'mono': 1.0
}


class TwentyFortyEight:
    def __init__(self, depth, ui):
        self.depth = depth
        self.ui = ui

        self.game_board = GameBoard()

    def get_next_player_move(self):
        search = self.search(self.depth, -10000, 10000, 0, 0, True)

        print search

        return search['direction']

    def make_player_move(self):
        self.game_board.make_move(self.get_next_player_move())

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

                twenty_forty_eight = TwentyFortyEight(game_board, None)

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

        candidate_cells = []

        empty_cells = self.game_board.get_empty_cells()
        number_of_empty_cells = len(empty_cells)

        scores = {
            1: [],
            2: []
        }

        for value in scores:
            value_scores = scores[value]

            for empty_cell in empty_cells:
                new_cell = Cell(empty_cell, value)

                self.game_board.add_cell_to_grid(new_cell)

                value_scores.append(self.evaluate_state())

                self.game_board.remove_cell_from_grid(new_cell)

        min_score = min(scores[1] + scores[2])

        for value in scores:
            value_scores = scores[value]

            for i in range(number_of_empty_cells):
                if value_scores[i] == min_score:
                    candidate_cells.append([empty_cells[i], value])

        for candidate_cell in candidate_cells:
            cell = Cell(candidate_cell[0], candidate_cell[1])
            game_board = self.game_board.clone()

            positions += 1

            game_board.add_cell_to_grid(cell)
            twenty_forty_eight = TwentyFortyEight(game_board, None)

            result = twenty_forty_eight.search(depth, alpha, best_score, positions, cut_offs, True)

            positions = result['positions']
            cut_offs = result['cut_offs']

            if result['score'] < best_score:
                best_score = result['score']

            if best_score < alpha:
                cut_offs += 1

                return {
                    'direction': None,
                    'score': alpha,
                    'positions': positions,
                    'cut_offs': cut_offs
                }

        return {
            'direction': best_move,
            'score': best_score,
            'positions': positions,
            'cut_offs': cut_offs
        }

    def search(self, depth, alpha, beta, positions, cut_offs, is_player_turn):
        return \
            self.evaluate_player_move(depth, alpha, beta, positions, cut_offs) if is_player_turn else \
            self.evaluate_computer_move(depth, alpha, beta, positions, cut_offs)

    def run(self):
        while not self.game_board.is_game_over():
            self.make_player_move()
            self.ui.update_ui(self.game_board.state)

            time.sleep(1)

            self.game_board.make_computer_move()
            self.ui.update_ui(self.game_board.state)

            time.sleep(1)

        try:
            input('Done. Press return to continue')
        except:
            pass
