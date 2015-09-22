from numpy.random import choice
from numpy import add

from math import log

from modules.module_four.ui import Ui


EVAL_WEIGHTS = {
    'empty': 2.7,
    'max': 1.0,
    'smooth': 0.1,
    'mono': 1.0
}


class TwentyFortyEight:
    def __init__(self, height=800):
        self.game_board = GameBoard(height)

    def get_next_player_move(self):
        pass

    def evaluate_state(self):
        number_of_empty_cells = self.game_board.get_number_of_empty_cells()

        return \
            log(number_of_empty_cells * EVAL_WEIGHTS['empty']) +\
            self.game_board.get_max_value() * EVAL_WEIGHTS['max'] +\
            self.game_board.smoothness() * EVAL_WEIGHTS['smooth'] +\
            self.game_board.monotonicity() * EVAL_WEIGHTS['mono']


class GameBoard:
    def __init__(self, height=800):
        self.state = '1000000040000001'
        self.directions = {
            'up': [0, -1],
            'right': [1, 0],
            'down': [0, 1],
            'left': [-1, 0],
        }

        self.ui = Ui(height)

    def has_2048(self):
        return self.state.count('11') > 0

    def get_number_of_empty_cells(self):
        return self.state.count('0')

    def get_value_at_matrix_position(self, x, y):
        return int(self.state[x*4+y])

    def get_value_at_absolute_position(self, i):
        return int(self.state[i])

    def is_cell_occupied(self, cell):
        if 0 <= cell[0] <= 3 and 0 <= cell[1] <= 3:
            return self.get_value_at_matrix_position(cell[0], cell[1]) > 0
        else:
            return None

    @staticmethod
    def get_next_spawning():
        return str(choice([1, 2], p=[0.9, 0.1]))

    def get_closest_filled_cell(self, curr, step):
        prev = curr
        curr = add(curr, step)

        while 0 <= curr[0] <= 3 and 0 <= curr[1] <= 3 and not self.get_value_at_matrix_position(curr[0], curr[1]):
            prev = curr
            curr += add(curr, step)

        return [prev, curr]

    def get_next_computer_move(self):
        next_cell_index = choice([i for i in xrange(16) if not self.get_value_at_absolute_position(i)])
        next_state = self.state[:next_cell_index]+self.get_next_spawning()+self.state[next_cell_index+1:]

        self.ui.update_ui(next_state)

        return next_state

    def smoothness(self):
        smoothness = 0

        for x in [0, 1, 2, 3]:
            for y in [0, 1, 2, 3]:
                value = self.get_value_at_matrix_position(x, y)

                if value:
                    for step in ['right', 'down']:
                        closest_cell = self.get_closest_filled_cell([x, y], self.directions[step])[1]

                        if self.is_cell_occupied(closest_cell):
                            closest_cell_value = self.get_value_at_matrix_position(closest_cell[0], closest_cell[1])

                            smoothness -= abs(value-closest_cell_value)

        return smoothness

    def monotonicity(self):
        direction_scores = [0, 0, 0, 0]

        for x in [0, 1, 2, 3]:
            current_index = 0
            next_index = current_index+1

            while next_index < 4:
                while next_index < 4 and not self.is_cell_occupied([x, next_index]):
                    next_index += 1

                # FIXME: Is this necessary?
                if next_index >= 4:
                    next_index -= 1

                current_value = self.get_value_at_matrix_position(x, current_index)
                next_value = self.get_value_at_matrix_position(x, next_index)

                if current_value > next_value:
                    direction_scores[0] += next_value - current_value
                elif next_index > current_value:
                    direction_scores[1] += current_value - next_value

                current_index = next_index
                next_index += 1

        for y in [0, 1, 2, 3]:
            current_index = 0
            next_index = current_index+1

            while next_index < 4:
                while next_index < 4 and not self.is_cell_occupied([next_index, y]):
                    next_index += 1

                # FIXME: Is this necessary?
                if next_index >= 4:
                    next_index -= 1

                current_value = self.get_value_at_matrix_position(current_index, y)
                next_value = self.get_value_at_matrix_position(next_index, y)

                if current_value > next_value:
                    direction_scores[1] += next_value - current_value
                elif next_index > current_value:
                    direction_scores[2] += current_value - next_value

                current_index = next_index
                next_index += 1

        return max(direction_scores[:2]) + max(direction_scores[2:])

    def get_max_value(self):
        return max([int(i) for i in self.state])
