import sys

from operator import itemgetter

from common.csp.csp import CSP
from common.csp.csp import ConstraintInstance
from common.csp_a_star.csp_a_star import CSPAStar

from modules.module_two.a_star import AStar
from modules.module_two.node import Node
from modules.module_two.ui import Ui


class ModuleTwo:
    def __init__(self, task_file, number_of_colors, sleep_duration=0.0, height=800):
        self.height = height
        self.width = None

        self.sleep_duration = sleep_duration

        self.nv, self.ne, self.vertices, self.edges = self.generate_task(task_file)

        self.colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
        self.number_of_colors = number_of_colors

        self.variables = self.generate_variables()
        self.constraints = self.generate_constraints()

        self.run()

    @staticmethod
    def read_vertex(input_value, vertex_list):
        value_list = input_value.strip().split(' ')

        vertex_list['node_%s' % value_list[0]] = {
            'x': float(value_list[1]),
            'y': float(value_list[2])
        }

    @staticmethod
    def read_edge(input_value):
        return ['node_%s' % value for value in input_value.strip().split(' ')]

    @staticmethod
    def read_integer_pair(input_value):
        return [int(value) for value in input_value.strip().split(' ')]

    def rescale_vertices(self, vertices):
        vertex_coordinates = [[vertices[vertex]['x'], vertices[vertex]['y']] for vertex in vertices]

        min_x = min(vertex_coordinates, key=itemgetter(0))[0]
        min_y = min(vertex_coordinates, key=itemgetter(1))[1]

        diff_x = max(vertex_coordinates, key=itemgetter(0))[0] - min_x
        diff_y = max(vertex_coordinates, key=itemgetter(1))[1] - min_y

        self.width = diff_x * self.height / diff_y

        scale_x = (self.width - 30.0) / diff_x
        scale_y = (self.height - 30.0) / diff_y

        for vertex in vertices:
            vertices[vertex] = {
                'x': int((vertices[vertex]['x'] - min_x) * scale_x + 15),
                'y': int((vertices[vertex]['y'] - min_y) * scale_y + 15),
            }

    def generate_task(self, input_file_name):
        with open(input_file_name) as input_file:
            nv, ne = self.read_integer_pair(input_file.readline())

            vertices = {}
            edges = []

            for i in range(nv):
                self.read_vertex(input_file.readline(), vertices)

            self.rescale_vertices(vertices)

            for i in range(ne):
                edges.append(self.read_edge(input_file.readline()))

            return nv, ne, vertices, edges

    def generate_variables(self):
        return {variable: self.colors[:self.number_of_colors] for variable in self.vertices.keys()}

    def generate_constraints(self):
        constraints = []

        for edge in self.edges:
            variables = [node for node in edge]
            expression = '%s!=%s' % (edge[0], edge[1])

            constraints.append(ConstraintInstance(variables, expression))

        return constraints

    def run(self):
        ui = Ui(self.vertices, self.edges, self.width, self.height)

        CSPAStar(self.variables, self.constraints, AStar, Node, ui.update_ui, self.sleep_duration).run()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('You need to supply a file containing the problem description and number of colors')
    else:
        if len(sys.argv) == 4:
            sleep = float(sys.argv[3])
        else:
            sleep = 0.0

        ModuleTwo(sys.argv[1], int(sys.argv[2]), sleep)
