import sys

from modules.module_two.a_star import AStar
from modules.module_two.node import Node


class ModuleTwo:
    def __init__(self, task_file, sleep_duration=0.0):
        nv, ne, vertices, edges = self.generate_task(task_file)

    @staticmethod
    def read_vertex(input_value):
        value_list = input_value.strip().split(' ')

        return {
            'id': int(value_list[0]),
            'x': float(value_list[1]),
            'y': float(value_list[2])
        }

    @staticmethod
    def read_integer_pair(input_value):
        return [int(value) for value in input_value.strip().split(' ')]

    def generate_task(self, input_file_name):
        with open(input_file_name) as input_file:
            nv, ne = self.read_integer_pair(input_file.readline())

            vertices = {}
            edges = []

            for i in range(nv):
                vertex = self.read_vertex(input_file.readline())

                vertices[vertex['id']] = vertex

            for i in range(ne):
                edges.append(self.read_integer_pair(input_file.readline()))

            return nv, ne, vertices, edges


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You need to supply a file containing the problem description')
    else:
        if len(sys.argv) == 3:
            sleep = float(sys.argv[2])
        else:
            sleep = 0.0

        ModuleTwo(sys.argv[1], sleep)
