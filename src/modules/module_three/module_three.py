import sys
import itertools

from common.csp.csp import CSP
from common.csp.csp import ConstraintInstance
from common.csp_a_star.csp_a_star import CSPAStar

from modules.module_three.a_star import AStar
from modules.module_three.node import Node
from modules.module_three.ui import Ui


class ModuleThree:
    def __init__(self, task_file, sleep_duration=0.0, height=800):
        self.height = height
        self.sleep_duration = sleep_duration

        self.dimensions, rows, columns = self.generate_task(task_file)

        self.rows = None
        self.columns = None

        self.variables = self.generate_variables(rows, columns)
        self.constraints = self.generate_constraints()

        self.run()

    @staticmethod
    def read_integer_list(input_value):
        return [int(value) for value in input_value.strip().split(' ')]

    def generate_task(self, input_file_name):
        with open(input_file_name) as input_file:
            dimensions = self.read_integer_list(input_file.readline().strip())
            rows = []
            columns = []

            for i in xrange(dimensions[0]):
                rows.append(self.read_integer_list(input_file.readline().strip()))

            for i in xrange(dimensions[1]):
                columns.append(self.read_integer_list(input_file.readline().strip()))

            return dimensions, rows, columns

    @staticmethod
    def generate_permutations(elements, element_length, prefix):
        permutations = {}

        for i in range(len(elements)):
            # Unique ID for each element (row or column)
            element_id = '%s%d' % (prefix, i)

            # List of permutation for each element
            permutations[element_id] = []

            # Number of segments in the element
            segment_lengths = elements[i]

            # Number of empty cells. Used for knowing how many permutations to make
            number_of_empty_cells = element_length - sum(segment_lengths)

            # Permutations. Describes the number of of empty cells before each segment
            combinations = itertools.combinations(range(number_of_empty_cells+1), len(segment_lengths))

            # Generates permutations
            for combination in combinations:
                # Start positions of the empty segments. Adds an empty segment to the start
                empty_segment_start_positions = [0] + list(combination)

                # End positions of the empty segments
                empty_segment_end_positions = list(combination) + [number_of_empty_cells]

                # Length of the empty segments
                empty_segment_lengths = [end-start for start, end in zip(
                    empty_segment_start_positions, empty_segment_end_positions)]

                # Zips empty segments and filled segments, creating a list of elements containing the number
                # of empty cells before each segments, and the length of the segment
                segments_combined = zip(empty_segment_lengths, segment_lengths + [0])

                # Creates a string describing the permutation. 0 for empty cell, 1 for filled cell
                permutation_string = ''.join('0' * empty + '1' * filled for empty, filled in segments_combined)

                # Adds the permutation string to the list of permutation for the element
                permutations[element_id].append(Element(element_id, permutation_string))

        return permutations

    def generate_variables(self, rows, columns):
        self.rows = self.generate_permutations(rows, self.dimensions[1], 'r')
        self.columns = self.generate_permutations(columns, self.dimensions[0], 'c')

        return dict(self.rows.items() + self.columns.items())

    def generate_constraints(self):
        constraints = []

        for row in self.rows.keys():
            for column in self.columns.keys():
                constraints.append(ConstraintInstance(
                    [row, column],
                    '%s.string[%s.index]==%s.string[%s.index]' % (row, column, column, row)
                ))

        return constraints

    def run(self):
        ui = Ui(self.dimensions, self.height)

        csp = CSP(self.variables, self.constraints)
        a_star = AStar(Node(None, csp), ui.update_ui, self.sleep_duration)

        CSPAStar(csp, a_star).run()


class Element(object):
    def __init__(self, identifier, string):
        print identifier, string

        self.index = int(identifier[1:])
        self.string = string


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You need to supply a file containing the problem description and number of colors')
    else:
        if len(sys.argv) == 3:
            sleep = float(sys.argv[2])
        else:
            sleep = 0.0

        ModuleThree(sys.argv[1], sleep)
