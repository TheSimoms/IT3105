from numpy.random import choice

from modules.module_four.ui import Ui


EVAL_WEIGHTS = {
    'smooth': 0.1,
    'mono': 1.0,
    'empty': 2.7,
    'max': 1.0,
}


class TwentyFortyEight:
    def __init__(self, height=800):
        self.game_board = GameBoard(height)

    def get_next_player_move(self):
        pass

    def evaluate_state(self):
        empty_cells = self.game_board.get_number_of_empty_cells()


class GameBoard:
    def __init__(self, height=800):
        self.state = '0000000000000000'
        self.directions = {
            0: -1,
            1: 4,
            2: 1,
            3: -4,
        }

        self.ui = Ui(height)

    def get_number_of_empty_cells(self):
        return self.state.count('0')

    def get_value_at_matrix_position(self, x, y):
        return int(self.state[x*4+y])

    def get_value_at_absolute_position(self, i):
        return int(self.state[i])

    @staticmethod
    def get_next_spawning():
        return str(choice([1, 2], p=[0.9, 0.1]))

    def get_closest_filled_cell(self, current_index, step):
        previous_index = current_index
        current_index += step

        number_of_steps = 0

        while 0 <= current_index < 16 and not int(self.state[current_index]) and number_of_steps < 4:
            previous_index = current_index
            current_index += step

            number_of_steps += 1

        if not 0 <= current_index < 16:
            current_index -= step
            previous_index -= step

        return [previous_index, current_index]

    # FIXME: Do this a better way
    def get_next_computer_move(self):
        empty_cell_index = int(choice(range(self.get_number_of_empty_cells())))
        empty_cell_count = 0

        for x in [0, 1, 2, 3]:
            for y in [0, 1, 2, 3]:
                value = self.get_value_at_matrix_position(x, y)

                if not value and empty_cell_count == empty_cell_index:
                    next_state = self.state[:x*4+y]+self.get_next_spawning()+self.state[x*4+y+1:]

                    self.ui.update_ui(next_state)

                    return next_state
                elif not value:
                    empty_cell_count += 1

    def smoothness(self):
        smoothness = 0

        for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
            value = self.get_value_at_absolute_position(i)

            if value:
                for step in [4, 1]:
                    closest_cell_value = self.get_value_at_absolute_position(self.get_closest_filled_cell(i, step)[1])
                    if closest_cell_value:
                        smoothness -= abs(value-closest_cell_value)

        return smoothness

    def monotonicity(self):
        pass

    def max_value(self):
        return max([int(i) for i in self.state])
