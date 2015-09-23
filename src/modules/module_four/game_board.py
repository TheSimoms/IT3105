from numpy.random import choice
from numpy import add

from copy import deepcopy


class GameBoard:
    def __init__(self, state=None):
        self.state = state if state else self.generate_grid()
        self.make_computer_move()

        self.directions = {
            'up': [0, -1],
            'right': [1, 0],
            'down': [0, 1],
            'left': [-1, 0],
        }

    @staticmethod
    def generate_grid():
        return [[None] * 4 for _ in [0, 1, 2, 3]]

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

    def get_cell_at_index(self, index):
        return self.get_cell_at_position(index[0], index[1])

    def get_cell_at_position(self, x, y):
        if 0 <= x <= 3 and 0 <= y <= 3:
            return self.state[x][y]
        else:
            return None

    def get_value_at_position(self, x, y):
        if 0 <= x <= 3 and 0 <= y <= 3:
            cell = self.get_cell_at_position(x, y)

            if cell:
                return cell.value

        return 0

    def get_value_at_absolute_position(self, i):
        return self.get_value_at_position(i // 3, i % 3)

    def get_value_at_index(self, index):
        if index is not None:
            return self.get_value_at_position(index[0], index[1])
        else:
            return 0

    def get_value_at_cell(self, cell):
        if cell:
            return self.get_value_at_position(cell.position[0], cell.position[1])
        else:
            return 0

    def is_index_occupied(self, index):
        return True if self.get_value_at_index(index) else False

    def prepare_cells_for_move(self):
        for x in [0, 1, 2, 3]:
            for y in [0, 1, 2, 3]:
                cell = self.get_cell_at_position(x, y)

                if cell:
                    cell.merge_parents = None
                    cell.previous_position = cell.position[:]

    @staticmethod
    def get_next_spawning():
        return choice([1, 2], p=[0.9, 0.1])

    def get_closest_neighbour(self, curr, step):
        print curr
        print step

        prev = curr
        curr = list(add(curr, step))

        print prev
        print curr

        while 0 <= curr[0] <= 3 and 0 <= curr[1] <= 3 and not self.get_value_at_index(curr):
            prev = curr
            curr = list(add(curr, step))

            print prev
            print curr

        print

        return [prev, curr]

    def empty_cell(self, x, y):
        self.state[x][y] = None

    def remove_cell_from_grid(self, cell):
        self.empty_cell(cell.position[0], cell.position[1])

    def add_cell_to_grid(self, cell):
        self.state[cell.position[0]][cell.position[1]] = cell

    @staticmethod
    def generate_steps(direction_vector):
        return [
            [3, 2, 1, 0] if direction_vector[0] == 1 else [0, 1, 2, 3],
            [3, 2, 1, 0] if direction_vector[1] == 1 else [0, 1, 2, 3],
        ]

    def move_cell(self, cell, position):
        self.state[cell.position[0]][cell.position[1]] = None
        self.state[position[0]][position[1]] = cell

        cell.change_position(position)

    def make_computer_move(self):
        empty_cells = self.get_empty_cells()
        next_cell_index = choice(range(len(empty_cells)))

        self.add_cell_to_grid(Cell(empty_cells[next_cell_index], self.get_next_spawning()))

        return self.state

    def make_move(self, direction):
        does_move_change_state = False
        direction_vector = self.directions[direction]

        steps = self.generate_steps(direction_vector)

        self.prepare_cells_for_move()

        for x in steps[0]:
            for y in steps[1]:
                cell = self.get_cell_at_position(x, y)

                if cell:
                    farthest_open_cell_indices = self.get_closest_neighbour(cell.position, direction_vector)
                    farthest_open_cell = self.get_cell_at_index(farthest_open_cell_indices[1])

                    if farthest_open_cell and farthest_open_cell.value == cell.value and not \
                            farthest_open_cell.merge_parents:
                        merged_cell = Cell(farthest_open_cell.position, cell.value + 1, [cell, farthest_open_cell])

                        self.add_cell_to_grid(merged_cell)
                        self.remove_cell_from_grid(cell)

                        cell.change_position(farthest_open_cell_indices[1])

                        does_move_change_state = True
                    # Move
                    elif cell.position != farthest_open_cell_indices[0]:
                        self.move_cell(cell, farthest_open_cell_indices[0])

                        does_move_change_state = True

        return does_move_change_state

    def smoothness(self):
        smoothness = 0

        for x in [0, 1, 2, 3]:
            for y in [0, 1, 2, 3]:
                value = self.get_value_at_position(x, y)

                if value:
                    for step in ['right', 'down']:
                        closest_cell_index = self.get_closest_neighbour([x, y], self.directions[step])[1]

                        if self.is_index_occupied(closest_cell_index):
                            smoothness -= abs(value-self.get_value_at_index(closest_cell_index))

        return smoothness

    def monotonicity(self):
        direction_scores = [0, 0, 0, 0]

        for x in [0, 1, 2, 3]:
            current_index = 0
            next_index = current_index+1

            while next_index <= 3:
                while next_index <= 3 and not self.is_index_occupied([x, next_index]):
                    next_index += 1

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

                current_value = self.get_value_at_position(current_index, y)
                next_value = self.get_value_at_position(next_index, y)

                if current_value > next_value:
                    direction_scores[1] += next_value - current_value
                elif next_index > current_value:
                    direction_scores[2] += current_value - next_value

                current_index = next_index
                next_index += 1

        return max(direction_scores[:2]) + max(direction_scores[2:])

    def get_max_value(self):
        return max(max([self.get_value_at_position(x, y) for y in [0, 1, 2, 3]]) for x in [0, 1, 2, 3])

    def clone(self):
        return GameBoard(deepcopy(self.state))


class Cell:
    def __init__(self, position, value, merge_parents=None):
        self.position = position
        self.value = value

        self.merge_parents = merge_parents
        self.previous_position = None

    def change_position(self, position):
        self.position = position[:]
