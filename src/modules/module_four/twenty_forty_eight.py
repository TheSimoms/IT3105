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

        if number_of_empty_cells > 10:
            return 1
        elif number_of_empty_cells > 3:
            return 1
        elif number_of_empty_cells > 2:
            return 2
        else:
            return 2

    def get_next_player_move(self):
        return self.search(self.get_depth(), True)['direction']

    def make_player_move(self):
        next_move = self.get_next_player_move()
        moved = False

        if next_move is None:
            print "NO MOVE FOUND"

            for direction in self.game_board.directions:
                if self.game_board.make_player_move(direction):
                    moved = True

                    break
        else:
            print "MOVE FOUND"

            moved = True

            self.game_board.make_player_move(next_move)

        if moved and self.ui:
            self.ui.update_ui(self.game_board.state)

        return moved

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
                if game_board.has_2048():
                    return {
                        'direction': direction,
                        'score': 1000000
                    }

                if depth == 0:
                    result = {
                        'direction': direction,
                        'score': game_board.evaluate()
                    }
                else:
                    result = TwentyFortyEight(game_board=game_board).search(depth-1, False)

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

                result = TwentyFortyEight(game_board=game_board).search(depth, True)

                scores.append(result['score'] * PROBABILITIES[value])

        return {
            'direction': None,
            'score': mean(scores)
        }

    def search(self, depth, is_player_turn):
        return \
            self.evaluate_player_move(depth) if is_player_turn else \
            self.evaluate_computer_move(depth)

    def run(self):
        computer_move = self.make_computer_move()
        player_move = self.make_player_move()

        while computer_move and player_move:
            computer_move = self.make_computer_move()
            player_move = self.make_player_move()

        print "Score: %d" % 2 ** self.game_board.get_max_value()
        print
