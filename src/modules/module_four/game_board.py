from numpy import random, add
from copy import deepcopy


DIRECTIONS = {
    'up': [[0, -1], [[0, 1, 2, 3], [0, 1, 2, 3]]],
    'right': [[1, 0], [[3, 2, 1, 0], [0, 1, 2, 3]]],
    'down': [[0, 1], [[0, 1, 2, 3], [3, 2, 1, 0]]],
    'left': [[-1, 0], [[0, 1, 2, 3], [0, 1, 2, 3]]]
}

PATH = [
    [0, 0], [0, 1], [0, 2], [0, 3],
    [1, 3], [1, 2], [1, 1], [1, 0],
    [2, 0], [2, 1], [2, 2], [2, 3],
    [3, 3], [3, 2], [3, 1], [3, 0]
]

R = 0.25


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

    def get_value_at_index(self, index):
        return self.get_value_at_position(index[0], index[1])

    def prepare_cells_for_move(self):
        for x in [0, 1, 2, 3]:
            for y in [0, 1, 2, 3]:
                cell = self.get_cell_at_position(x, y)

                if cell:
                    cell.merged = False

    @staticmethod
    def get_next_spawning():
        return random.choice([1, 2], p=[0.9, 0.1])

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
        next_cell_index = random.choice(range(len(empty_cells))) if empty_cells else None

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

    def evaluate(self):
        return self.tidy()

    def get_max_value(self):
        return max(max([self.get_value_at_position(x, y) for y in [0, 1, 2, 3]]) for x in [0, 1, 2, 3])

    def tidy(self):
        return sum((self.get_value_at_index(PATH[n]) ** 2) * (R ** n) for n in range(16))

    def clone(self):
        return GameBoard(deepcopy(self.state))


class Cell:
    def __init__(self, position, value, merged=False):
        self.position = position
        self.value = value

        self.merged = merged

    def change_position(self, position):
        self.position = position[:]
