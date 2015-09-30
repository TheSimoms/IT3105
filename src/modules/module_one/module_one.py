import sys

from modules.module_one.a_star import AStar
from modules.module_one.node import Node


class ModuleOne:
    def __init__(self, task_file, sleep_duration=0.0):
        self.task_space, self.grid_size, self.start_state, self.end_state = self.generate_task(task_file)

        self.start = Node(None, self.start_state, self.end_state)
        self.end = Node(None, self.end_state, self.end_state)

        BreadthFirst(self.task_space, self.start, self.end, sleep_duration)
        DepthFirst(self.task_space, self.start, self.end, sleep_duration)
        BestFirst(self.task_space, self.start, self.end, sleep_duration)

    @staticmethod
    def input_to_list(input_value):
        return [int(value) for value in input_value.strip().split(' ')]

    def generate_task(self, input_file_name):
        with open(input_file_name) as input_file:
            grid_size = self.input_to_list(input_file.readline())

            start_and_stop_positions = self.input_to_list(input_file.readline())

            start = start_and_stop_positions[:2]
            end = start_and_stop_positions[2:]

            obstacles = []

            for line in input_file:
                obstacles.append(self.input_to_list(line))

            task_space = [['o' for y in range(grid_size[1])] for x in range(grid_size[0])]

            for obstacle in obstacles:
                for x in range(obstacle[0], obstacle[0]+obstacle[2]):
                    for y in range(obstacle[1], obstacle[1]+obstacle[3]):
                        task_space[x][y] = 'x'

            return task_space, grid_size, start, end


class BreadthFirst(AStar):
    def __init__(self, task_space, start, end, sleep_duration=0.0):
        super(BreadthFirst, self).__init__(task_space, start, end, 'Breadth first', sleep_duration)

    def f(self):
        return self.open[0]


class DepthFirst(AStar):
    def __init__(self, task_space, start, end, sleep_duration=0.0):
        super(DepthFirst, self).__init__(task_space, start, end, 'Depth first', sleep_duration)

    def f(self):
        return self.open[-1]


class BestFirst(AStar):
    def __init__(self, task_space, start, end, sleep_duration=0.0):
        super(BestFirst, self).__init__(task_space, start, end, 'Best first', sleep_duration)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You need to supply a file containing the problem description')
    else:
        if len(sys.argv) == 3:
            sleep = float(sys.argv[2])
        else:
            sleep = 0.0

        ModuleOne(sys.argv[1], sleep)
