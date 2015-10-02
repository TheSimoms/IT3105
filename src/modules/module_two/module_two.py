import sys

from operator import itemgetter

from common.csp.csp import ConstraintInstance
from common.csp_a_star.csp_a_star import CSPAStar

from modules.module_two.a_star import AStar
from modules.module_two.node import Node
from modules.module_two.ui import Ui


class ModuleTwo:
    def __init__(self, task_file, number_of_colors, height=800):
        self.height = height  # Height. Only used in UI
        self.width = None  # Width is calculated using the height

        # Reads input file
        self.nv, self.ne, self.vertices, self.edges = self.generate_task(task_file)

        self.colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']  # List of possible colors
        self.number_of_colors = number_of_colors  # Number of colors to use in the algorithm

        self.variables = self.generate_variables()  # Generates variables
        self.constraints = self.generate_constraints()  # Generates constraints

        self.run()  # Runs the A*-GAC algorithm

    # Reads a vertex from the input file
    @staticmethod
    def read_vertex(input_value, vertex_list):
        value_list = input_value.strip().split(' ')

        vertex_list['node_%s' % value_list[0]] = {
            'x': float(value_list[1]),
            'y': float(value_list[2])
        }

    # Reads an edge from the input file
    @staticmethod
    def read_edge(input_value):
        return ['node_%s' % value for value in input_value.strip().split(' ')]

    # Reads a string with space separated integers. Returns list of the integers
    @staticmethod
    def read_integer_pair(input_value):
        return [int(value) for value in input_value.strip().split(' ')]

    # Rescales the coordinates for the vertices. Puts them all in the range of the UI
    def rescale_vertices(self, vertices):
        # Reads the coordinates of the vertices
        vertex_coordinates = [[vertices[vertex]['x'], vertices[vertex]['y']] for vertex in vertices]

        # Finds minimum value in both directions
        min_x = min(vertex_coordinates, key=itemgetter(0))[0]
        min_y = min(vertex_coordinates, key=itemgetter(1))[1]

        # Finds the max position difference in both directions
        diff_x = max(vertex_coordinates, key=itemgetter(0))[0] - min_x
        diff_y = max(vertex_coordinates, key=itemgetter(1))[1] - min_y

        # Calculates width of the UI
        self.width = diff_x * self.height / diff_y

        # Calculates how much to scale each coordinate with in each direction
        scale_x = (self.width - 30.0) / diff_x
        scale_y = (self.height - 30.0) / diff_y

        # Iterates over all the vertices and rescales the coordinates
        for vertex in vertices:
            vertices[vertex] = {
                'x': int((vertices[vertex]['x'] - min_x) * scale_x + 15),
                'y': int((vertices[vertex]['y'] - min_y) * scale_y + 15),
            }

    # Reads the input file
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

    # Generates the CSP variables
    def generate_variables(self):
        return {variable: self.colors[:self.number_of_colors] for variable in self.vertices.keys()}

    # Generates the CSP constraints
    def generate_constraints(self):
        constraints = []

        # Iterates over all the edges
        for edge in self.edges:
            variables = [node for node in edge]  # Fetches the vertices in the edge
            expression = '%s!=%s' % (edge[0], edge[1])  # Expression to feed into the constraint code chunk maker

            constraints.append(ConstraintInstance(variables, expression))  # Adds constraint to constraint list

        return constraints

    def run(self):
        ui = Ui(self.vertices, self.edges, self.width, self.height)

        CSPAStar(self.variables, self.constraints, AStar, Node, ui.update_ui).run()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('You need to supply a file containing the problem description and number of colors')
    else:
        ModuleTwo(sys.argv[1], int(sys.argv[2]))
