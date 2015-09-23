from numpy.random import choice
from numpy import add

from copy import deepcopy


class GameBoard:
    def __init__(self, state=None):
        self.state = state if state else self.generate_grid()
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

    def get_number_of_empty_cells(self):
        number_of_empty_cells = 0

        for column in self.state:
            for cell in column:
                if not cell:
                    number_of_empty_cells += 1

        return number_of_empty_cells

    def get_cell_at_index(self, index):
        return self.get_cell_at_position(index[0], index[1])

    def get_cell_at_position(self, x, y):
        if 0 <= x <= 15 and 0 <= y <= 15:
            return self.state[x][y]
        else:
            return None

    def get_value_at_position(self, x, y):
        cell = self.get_cell_at_position(x, y)

        if cell:
            return cell.value
        else:
            return 0

    def get_value_at_absolute_position(self, i):
        return self.get_value_at_position(i // 4, i % 4)

    def get_value_at_index(self, index):
        if index:
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

    def reset_cells_after_move(self):
        for x in [0, 1, 2, 3]:
            for y in [0, 1, 2, 3]:
                cell = self.get_cell_at_position(x, y)

                if cell:
                    cell.merge_parents = None
                    cell.previous_position = cell.position[:]

    @staticmethod
    def get_next_spawning():
        return str(choice([1, 2], p=[0.9, 0.1]))

    def get_farthest_open_cell(self, curr, step):
        prev = curr
        curr = add(curr, step)

        while 0 <= curr[0] <= 3 and 0 <= curr[1] <= 3 and not self.get_value_at_index(curr):
            prev = curr
            curr += add(curr, step)

        return [prev, curr]

    def empty_cell(self, x, y):
        self.state[x][y] = None

    def remove_cell_from_grid(self, cell):
        self.empty_cell(cell.position[0], cell.position[1])

    def add_cell_to_grid(self, cell):
        self.state[cell.position[0]][cell.position[1]] = cell

    def get_next_computer_move(self):
        next_cell_position = choice([[[x, y] for y in [0, 1, 2, 3] if not self.get_value_at_position(
            x, y)] for x in [0, 1, 2, 3]])

        self.add_cell_to_grid(Cell(next_cell_position, self.get_next_spawning()))

        return self.state

    @staticmethod
    def generate_steps(direction_vector):
        return [
            [0, 1, 2, 3] if direction_vector[0] else [3, 2, 1, 0],
            [0, 1, 2, 3] if direction_vector[1] else [3, 2, 1, 0],
        ]

    def move_cell(self, cell, position):
        self.state[position[0]][position[1]] = cell

    def make_move(self, direction):
        does_move_change_state = False
        direction_vector = self.directions[direction]

        steps = self.generate_steps(direction_vector)

        for x in steps[0]:
            for y in steps[1]:
                cell = self.get_cell_at_position(x, y)

                if cell:
                    farthest_open_cell_indices = self.get_farthest_open_cell(cell.position, direction_vector)
                    farthest_open_cell = self.get_cell_at_index(farthest_open_cell_indices[1])

                    # Merge
                    if farthest_open_cell:
                        if farthest_open_cell.value == cell.value and not farthest_open_cell.merge_parents:
                            merged_cell = Cell(farthest_open_cell.position, cell.value * 2, [cell, farthest_open_cell])

                            self.add_cell_to_grid(merged_cell)
                            self.remove_cell_from_grid(cell)

                            cell.change_position(farthest_open_cell_indices[1])

                            does_move_change_state = True
                    # Move
                    else:
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
                        closest_cell_index = self.get_farthest_open_cell([x, y], self.directions[step])[1]

                        if self.is_index_occupied(closest_cell_index):
                            smoothness -= abs(value-self.get_value_at_index(closest_cell_index))

        return smoothness

    def monotonicity(self):
        direction_scores = [0, 0, 0, 0]

        for x in [0, 1, 2, 3]:
            current_index = 0
            next_index = current_index+1

            while next_index < 4:
                while next_index < 4 and not self.is_index_occupied([x, next_index]):
                    next_index += 1

                # FIXME: Is this necessary?
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

            while next_index < 4:
                while next_index < 4 and not self.is_index_occupied([next_index, y]):
                    next_index += 1

                # FIXME: Is this necessary?
                if next_index >= 4:
                    next_index -= 1

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
