import random
import logging

from numpy import mean

from common.twenty_forty_eight.game_board import GameBoard, Cell



# Probabilities for spawning values
PROBABILITIES = {
    1: 0.9,
    2: 0.1
}


class TwentyFortyEight:
    def __init__(self, game_board=None, ui=None):
        # Callback function for updating UI
        self.ui = ui

        # Creates a new game board or sets game board to a supplied value
        self.game_board = GameBoard() if not game_board else game_board

    # Returns what depth to use in the expectimax function
    def get_depth(self):
        number_of_empty_cells = self.game_board.get_number_of_empty_cells()

        if number_of_empty_cells > 3:
            return 1
        elif number_of_empty_cells > 1:
            return 2
        else:
            return 3

    # Finds best computer move using expectimax function
    def get_next_player_move(self):
        return self.evaluate_player_move(self.get_depth())['direction']

    # Makes computer move, updates UI and returns whether move was legal or not
    def make_player_move(self):
        next_move = self.get_next_player_move()  # Finds next move using expectimax function

        # Returns False if no move found
        if next_move is None:
            return None

        # Makes the actual move
        self.game_board.make_player_move(next_move)

        # Returns that the move was legal
        return next_move

    def make_random_move(self):
        moves = [0, 1, 2, 3]
        moved = False

        while not moved:
            move = random.choice(moves)
            moved = self.game_board.make_player_move(move)

            if moved:
                return move
            else:
                moves.remove(move)

                if not len(moves):
                    return None

        return None

    # Makes computer move
    def make_computer_move(self):
        # Makes move
        moved = self.game_board.make_computer_move()

        # Updates UI if move was made
        if moved and self.ui:
            self.ui.update_ui(self.game_board.state)

        # Returns whether move was made or not
        return moved

    # Evaluates current game board, returning move expected to yield highest score
    def evaluate_player_move(self, depth):
        best_move = None
        best_score = -1

        # Iterates through all possible moves
        for direction in self.game_board.directions:
            # Clones game board
            game_board = self.game_board.clone()

            # Checks whether move is legal or not
            if game_board.make_player_move(direction):
                if depth == 0:
                    # Calculates board score if depth is 0
                    result = {
                        'direction': direction,
                        'score': game_board.evaluate()
                    }
                else:
                    # Calculates expected board score if depth is > 0
                    result = TwentyFortyEight(game_board=game_board).evaluate_computer_move(depth)

                # Compares calculated score to best score
                if result['score'] > best_score:
                    best_score = result['score']
                    best_move = direction

        # Returns best move and expected score
        return {
            'direction': best_move,
            'score': best_score
        }

    # Evaluates current game board, returning weighted mean of computer moves
    def evaluate_computer_move(self, depth):
        # All empty cells
        empty_cells = self.game_board.get_empty_cells()

        scores = []

        # Iterates through all empty cells
        for empty_cell in empty_cells:
            # Puts a 1 and 2 in each empty cell
            for value in [1, 2]:
                cell = Cell(empty_cell, value)

                # Clones game board and adds value to empty cell
                game_board = self.game_board.clone()
                game_board.add_cell_to_grid(cell)

                # Calculates expected score of current board
                result = TwentyFortyEight(game_board=game_board).evaluate_player_move(depth-1)

                # Appends weighted expected score to list of possible computer moves
                scores.append(result['score'] * PROBABILITIES[value])

        # Returns weighted mean of all possible computer moves
        return {
            'direction': None,
            'score': mean(scores)
        }

    # Runs the 2048 solver
    def run(self, move_function, save_moves=False):
        is_game_over = not self.make_computer_move()
        moves = []

        try:
            # Makes moves as long as the game isn't lost yet
            while not is_game_over:
                board_state = self.game_board.get_cell_values()

                # Makes the move
                next_move = move_function()

                # Updates UI, if any
                if next_move is not None:
                    if self.ui:
                        self.ui.update_ui(self.game_board.state)

                    if save_moves:
                        logging.info('Move made: %d' % next_move)

                        moves.append([board_state, next_move])

                # Spawns new value
                is_game_over = not self.make_computer_move()
        except KeyboardInterrupt:
            pass

        # Returns final score
        if save_moves:
            return moves
        else:
            return 2 ** self.game_board.get_max_value()
