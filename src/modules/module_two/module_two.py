import sys

from operator import itemgetter

from common.csp.csp import CSP
from common.csp.csp import ConstraintInstance

from modules.module_two.a_star import AStar
from modules.module_two.node import Node
from modules.module_two.ui import Ui


class ModuleTwo:
    def __init__(self, task_file, number_of_colors, sleep_duration=0.0, height=800):
        self.height = height
        self.width = None

        self.sleep_duration = sleep_duration

        self.nv, self.ne, self.vertices, self.edges = self.generate_task(task_file)

        self.colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'][:number_of_colors]
        self.ui = Ui(self.vertices, self.edges, self.width, self.height).update_ui

        self.variables = self.generate_variables()
        self.constraints = self.generate_constraints()

        self.run()

    def generate_vertices(self, raw_vertices):
        vertices = {}

        vertex_coordinates = [[raw_vertex['x'], raw_vertex['y']] for raw_vertex in raw_vertices]

        min_x = min(vertex_coordinates, key=itemgetter(0))[0]
        min_y = min(vertex_coordinates, key=itemgetter(1))[1]

        diff_x = max(vertex_coordinates, key=itemgetter(0))[0] - min_x
        diff_y = max(vertex_coordinates, key=itemgetter(1))[1] - min_y

        self.width = diff_x * self.height / diff_y

        scale_x = (self.width - 10.0) / diff_x
        scale_y = (self.height - 10.0) / diff_y

        for raw_vertex in raw_vertices:
            vertices[raw_vertex['id']] = {
                'id': raw_vertex['id'],
                'x': int((raw_vertex['x'] - min_x) * scale_x + 5),
                'y': int((raw_vertex['y'] - min_y) * scale_y + 5),
            }

        return vertices

    @staticmethod
    def read_vertex(input_value):
        value_list = input_value.strip().split(' ')

        return {
            'id': 'node_%s' % value_list[0],
            'x': float(value_list[1]),
            'y': float(value_list[2])
        }

    @staticmethod
    def read_edge(input_value):
        return ['node_%s' % value for value in input_value.strip().split(' ')]

    @staticmethod
    def read_integer_pair(input_value):
        return [int(value) for value in input_value.strip().split(' ')]

    def generate_task(self, input_file_name):
        with open(input_file_name) as input_file:
            nv, ne = self.read_integer_pair(input_file.readline())

            raw_vertices = []
            edges = []

            for i in range(nv):
                raw_vertices.append(self.read_vertex(input_file.readline()))

            vertices = self.generate_vertices(raw_vertices)

            for i in range(ne):
                edges.append(self.read_edge(input_file.readline()))

            return nv, ne, vertices, edges

    def generate_variables(self):
        return {variable: self.colors for variable in self.vertices.keys()}

    def generate_constraints(self):
        constraints = []

        for edge in self.edges:
            variables = [node for node in edge]
            expression = '%s!=%s' % (edge[0], edge[1])

            constraints.append(ConstraintInstance(variables, expression))

        return constraints

    def run(self):
        csp = CSP(self.variables, self.constraints)

        result = csp.gac()

        if result:
            self.finish()
        elif result is not None:
            AStar(Node(None, csp), self.ui, self.sleep_duration).run()

            self.finish()
        else:
            print('No solution possible')

    def finish(self):
        pass


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('You need to supply a file containing the problem description and number of colors')
    else:
        if len(sys.argv) == 4:
            sleep = float(sys.argv[3])
        else:
            sleep = 0.5

        ModuleTwo(sys.argv[1], int(sys.argv[2]), sleep)
