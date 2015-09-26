from numpy.random import choice
from numpy import add, dot

from math import log, exp

from copy import deepcopy


EVAL_WEIGHTS = {
    'empty': 2.7,
    'max': 1.5,
    'smooth': 1.0,
    'mono': 2.0,
    'tidy': 0.0
}

TIDY_WEIGHTS = [
    map(exp, _) for _ in [
        [10.0, 8.0, 7.0, 6.5],
        [0.5, 0.7, 1.0, 3.0],
        [-0.5, -1.5, -1.8, -2.0],
        [-3.8, -3.7, -3.5, -3.0]
    ]
]

DIRECTIONS = {
    'up': [[0, -1], [[0, 1, 2, 3], [0, 1, 2, 3]]],
    'right': [[1, 0], [[3, 2, 1, 0], [0, 1, 2, 3]]],
    'down': [[0, 1], [[0, 1, 2, 3], [3, 2, 1, 0]]],
    'left': [[-1, 0], [[0, 1, 2, 3], [0, 1, 2, 3]]]
}


class GameBoard:
    def __init__(self, state=None):
        self.state = state if state else self.generate_grid()
        self.directions = DIRECTIONS

    @staticmethod
    def generate_grid():
        return [[None] * 4 for _ in [0, 1, 2, 3]]

    def get_cell_values(self):
        values = []

        for x in [0, 1, 2, 3]:
            column = []

            for y in [0, 1, 2, 3]:
                column.append(self.get_value_at_position(x, y))

            values.append(column)

        return values

    def has_2048(self):
        for x in [0, 1, 2, 3]:
            for y in [0, 1, 2, 3]:
                if self.get_value_at_position(x, y) >= 11:
                    return True

        return False

    def get_empty_cells(self):
        return [[x, y] for y in [0, 1, 2, 3] for x in [0, 1, 2, 3] if not self.get_value_at_position(x, y)]

    def get_number_of_empty_cells(self):
        return len(self.get_empty_cells())

    def get_cell_at_position(self, x, y):
        if 0 <= x <= 3 and 0 <= y <= 3:
            return self.state[x][y]
        else:
            return None

    def get_cell_at_index(self, index):
        return self.get_cell_at_position(index[0], index[1])

    def get_value_at_position(self, x, y):
        cell = self.get_cell_at_position(x, y)

        if cell:
            return cell.value

        return 0

    def get_value_at_absolute_position(self, i):
        return self.get_value_at_position(i // 3, i % 3)

    def get_value_at_index(self, index):
        return self.get_value_at_position(index[0], index[1])

    def get_value_at_cell(self, cell):
        if cell:
            return self.get_value_at_position(cell.position[0], cell.position[1])
        else:
            return 0

    def is_index_occupied(self, index):
        return self.get_value_at_index(index) > 0

    def prepare_cells_for_move(self):
        for x in [0, 1, 2, 3]:
            for y in [0, 1, 2, 3]:
                cell = self.get_cell_at_position(x, y)

                if cell:
                    cell.merged = False
                    cell.previous_position = cell.position[:]

    @staticmethod
    def get_next_spawning():
        return choice([1, 2], p=[0.9, 0.1])

    def get_closest_neighbour(self, curr, step):
        prev = curr
        curr = list(add(curr, step))

        while 0 <= curr[0] <= 3 and 0 <= curr[1] <= 3 and not self.get_value_at_index(curr):
            prev = curr
            curr = list(add(curr, step))

        return [prev, curr]

    def remove_cell_from_grid(self, cell):
        self.state[cell.position[0]][cell.position[1]] = None

    def add_cell_to_grid(self, cell):
        self.state[cell.position[0]][cell.position[1]] = cell

    def move_cell(self, cell, position):
        self.state[cell.position[0]][cell.position[1]] = None
        self.state[position[0]][position[1]] = cell

        cell.change_position(position)

    def make_computer_move(self):
        empty_cells = self.get_empty_cells()
        next_cell_index = choice(range(len(empty_cells))) if empty_cells else None

        if next_cell_index is not None:
            self.add_cell_to_grid(Cell(empty_cells[next_cell_index], self.get_next_spawning()))

            return True

        return False

    def make_player_move(self, direction):
        does_move_change_state = False
        direction = self.directions[direction]

        steps = direction[1]

        self.prepare_cells_for_move()

        for x in steps[0]:
            for y in steps[1]:
                cell = self.get_cell_at_position(x, y)
                cell_index = [x, y]

                if cell:
                    closest_neighbour_indices = self.get_closest_neighbour(cell.position, direction[0])
                    closest_neighbour = self.get_cell_at_index(closest_neighbour_indices[1])

                    if closest_neighbour and closest_neighbour.value == cell.value and not \
                            closest_neighbour.merged:
                        merged_cell = Cell(closest_neighbour_indices[1], cell.value + 1, True)

                        self.add_cell_to_grid(merged_cell)
                        self.remove_cell_from_grid(cell)

                        cell.change_position(closest_neighbour_indices[1])

                        does_move_change_state = True
                    # Move
                    else:
                        self.move_cell(cell, closest_neighbour_indices[0])

                    if cell.position != cell_index:
                        does_move_change_state = True

        return does_move_change_state

    def smoothness(self):
        smoothness = 0

        for x in [0, 1, 2, 3]:
            for y in [0, 1, 2, 3]:
                value = self.get_value_at_position(x, y)

                if value:
                    for step in ['right', 'down']:
                        closest_cell_index = self.get_closest_neighbour([x, y], self.directions[step][0])[1]
                        closest_cell_value = self.get_value_at_index(closest_cell_index)

                        if closest_cell_value:
                            smoothness -= abs(value-closest_cell_value)

        return smoothness

    def monotonicity(self):
        direction_scores = [0, 0, 0, 0]

        for x in [0, 1, 2, 3]:
            current_index = 0
            next_index = current_index+1

            while next_index <= 3:
                while next_index <= 3 and not self.is_index_occupied([x, next_index]):
                    next_index += 1

                if next_index >= 4:
                    next_index -= 1

                current_value = self.get_value_at_position(x, current_index)
                next_value = self.get_value_at_position(x, next_index)

                if current_value > next_value:
                    direction_scores[0] += next_value - current_value
                elif next_index > current_value:
                    direction_scores[1] += current_value - next_value

                current_index = next_index
                next_index += 1

        for y in [0, 1, 2, 3]:
            current_index = 0
            next_index = current_index+1

            while next_index <= 3:
                while next_index <= 3 and not self.is_index_occupied([next_index, y]):
                    next_index += 1

                if next_index >= 4:
                    next_index -= 1

                current_value = self.get_value_at_position(current_index, y)
                next_value = self.get_value_at_position(next_index, y)

                if current_value > next_value:
                    direction_scores[2] += next_value - current_value
                elif next_index > current_value:
                    direction_scores[3] += current_value - next_value

                current_index = next_index
                next_index += 1

        return max(direction_scores[:2]) + max(direction_scores[2:])

    def get_max_value(self):
        return max(max([self.get_value_at_position(x, y) for y in [0, 1, 2, 3]]) for x in [0, 1, 2, 3])

    def evaluate(self):
        number_of_empty_cells = self.get_number_of_empty_cells()
        number_of_empty_cells_log = log(number_of_empty_cells) if number_of_empty_cells else 0.0

        weights = [
            number_of_empty_cells_log * EVAL_WEIGHTS['empty'],
            (2 ** self.get_max_value()) * EVAL_WEIGHTS['max'],
            self.smoothness() * EVAL_WEIGHTS['smooth'],
            self.monotonicity() * EVAL_WEIGHTS['mono'],
            self.tidy() * EVAL_WEIGHTS['tidy']
        ]

        return sum(weights)

    def tidy(self):
        dot_product = sum(sum(dot(self.get_cell_values(), TIDY_WEIGHTS)))

        return dot_product

    def clone(self):
        return GameBoard(deepcopy(self.state))


class Cell:
    def __init__(self, position, value, merged=False):
        self.position = position
        self.value = value

        self.merged = merged
        self.previous_position = None

    def change_position(self, position):
        self.position = position[:]
