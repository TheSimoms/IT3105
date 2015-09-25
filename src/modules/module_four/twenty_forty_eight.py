import time

from modules.module_four.game_board import GameBoard, Cell


class TwentyFortyEight:
    def __init__(self, game_board=None, ui=None):
        self.ui = ui

        self.game_board = GameBoard() if not game_board else game_board

    def get_next_player_move(self):
        number_of_empty_cells = self.game_board.get_number_of_empty_cells()
        depth = 1 if number_of_empty_cells > 7 else 2 if number_of_empty_cells > 4 else 3

        search = self.search(depth, -10000, 10000, 0, 0, True)

        return search['direction']

    def make_player_move(self):
        self.game_board.make_player_move(self.get_next_player_move())
        self.ui.update_ui(self.game_board.state)

    def make_computer_move(self):
        self.game_board.make_computer_move()
        self.ui.update_ui(self.game_board.state)

    def evaluate_player_move(self, depth, alpha, beta, positions, cut_offs):
        best_move = -1
        best_score = alpha

        for direction in self.game_board.directions:
            game_board = self.game_board.clone()

            if game_board.make_player_move(direction):
                positions += 1

                if game_board.has_2048():
                    return {
                        'direction': direction,
                        'score': 10000,
                        'positions': positions,
                        'cut_offs': cut_offs
                    }

                twenty_forty_eight = TwentyFortyEight(game_board=game_board)

                if depth == 0:
                    result = {
                        'direction': direction,
                        'score': twenty_forty_eight.game_board.evaluate()
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
                    cut_offs += 1

                    return {
                        'direction': best_move,
                        'score': beta,
                        'positions': positions,
                        'cut_offs': cut_offs
                    }

        result = {
            'direction': best_move,
            'score': best_score,
            'positions': positions,
            'cut_offs': cut_offs
        }

        return result

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
            for empty_cell in empty_cells:
                new_cell = Cell(empty_cell, value)

                self.game_board.add_cell_to_grid(new_cell)

                scores[value].append(-self.game_board.smoothness())

                self.game_board.remove_cell_from_grid(new_cell)

        max_score = max(scores[1] + scores[2])

        for value in scores:
            for i in range(number_of_empty_cells):
                if scores[value][i] == max_score:
                    candidate_cells.append([empty_cells[i], value])

        for candidate_cell in candidate_cells:
            positions += 1

            cell = Cell(candidate_cell[0], candidate_cell[1])

            game_board = self.game_board.clone()
            game_board.add_cell_to_grid(cell)

            twenty_forty_eight = TwentyFortyEight(game_board=game_board)

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

        result = {
            'direction': best_move,
            'score': best_score,
            'positions': positions,
            'cut_offs': cut_offs
        }

        return result

    def search(self, depth, alpha, beta, positions, cut_offs, is_player_turn):
        return \
            self.evaluate_player_move(depth, alpha, beta, positions, cut_offs) if is_player_turn else \
            self.evaluate_computer_move(depth, alpha, beta, positions, cut_offs)

    def player_choose_move(self):
        move = raw_input('Next move: ')

        if move == 'w':
            direction = 'up'
        elif move == 'a':
            direction = 'left'
        elif move == 's':
            direction = 'down'
        elif move == 'd':
            direction = 'right'
        else:
            direction = 'down'

        moved = self.game_board.make_player_move(direction)

        if moved:
            self.ui.update_ui(self.game_board.state)

        return moved

    def run(self):
        self.make_computer_move()

        while not self.game_board.is_game_over():
            """moved = self.player_choose_move()

            while not moved:
                print 'Illegal move'

                moved = self.player_choose_move()"""

            self.make_player_move()
            self.make_computer_move()
        try:
            input('Done. Press return to continue')
        except:
            pass
