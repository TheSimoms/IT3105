from numpy import mean

from modules.module_four.game_board import GameBoard, Cell


PROBABILITIES = {
    1: 0.9,
    2: 0.1
}


class TwentyFortyEight:
    def __init__(self, game_board=None, ui=None):
        self.ui = ui
        self.game_board = GameBoard() if not game_board else game_board

    def get_depth(self):
        number_of_empty_cells = self.game_board.get_number_of_empty_cells()

        if number_of_empty_cells > 3:
            return 1
        elif number_of_empty_cells > 1:
            return 2
        else:
            return 3

    def get_next_player_move(self):
        return self.evaluate_player_move(self.get_depth())['direction']

    def make_player_move(self):
        next_move = self.get_next_player_move()

        if next_move is None:
            return False

        self.game_board.make_player_move(next_move)

        if self.ui:
            self.ui.update_ui(self.game_board.state)

        return True

    def make_computer_move(self):
        moved = self.game_board.make_computer_move()

        if moved and self.ui:
            self.ui.update_ui(self.game_board.state)

        return moved

    def evaluate_player_move(self, depth):
        best_move = None
        best_score = -1

        for direction in self.game_board.directions:
            game_board = self.game_board.clone()

            if game_board.make_player_move(direction):
                if depth == 0:
                    result = {
                        'direction': direction,
                        'score': game_board.evaluate()
                    }
                else:
                    result = TwentyFortyEight(game_board=game_board).evaluate_computer_move(depth)

                if result['score'] > best_score:
                    best_score = result['score']
                    best_move = direction

        return {
            'direction': best_move,
            'score': best_score
        }

    def evaluate_computer_move(self, depth):
        empty_cells = self.game_board.get_empty_cells()

        scores = []

        for empty_cell in empty_cells:
            for value in [1, 2]:
                cell = Cell(empty_cell, value)

                game_board = self.game_board.clone()
                game_board.add_cell_to_grid(cell)

                result = TwentyFortyEight(game_board=game_board).evaluate_player_move(depth-1)

                scores.append(result['score'] * PROBABILITIES[value])

        return {
            'direction': None,
            'score': mean(scores)
        }

    def run(self):
        is_game_over = not self.make_computer_move()

        while not is_game_over:
            self.make_player_move()

            is_game_over = not self.make_computer_move()

        return 2 ** self.game_board.get_max_value()
