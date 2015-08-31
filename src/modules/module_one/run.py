import sys

sys.path.insert(0, '../../')

from a_star.a_star import AStar
from ui import Ui


class Run:
    def __init__(self, task_file, sleep_duration):
        try:
            self.task_space, self.grid_size, self.start, self.end = self.generate_task(task_file)

            BreadthFirst(self.arc_cost, self.h, self.get_neighbour_states, self.node_id,
                         Ui('Breadth first', self.task_space).draw_node, self.start, self.end, sleep_duration)
            DepthFirst(self.arc_cost, self.h, self.get_neighbour_states, self.node_id,
                       Ui('Depth first', self.task_space).draw_node, self.start, self.end, sleep_duration)
            BestFirst(self.arc_cost, self.h, self.get_neighbour_states, self.node_id,
                      Ui('Best first', self.task_space).draw_node, self.start, self.end, sleep_duration)
        except Exception as e:
            print 'Error:'
            print e

    @staticmethod
    def input_to_list(input_value):
        return [int(value) for value in input_value.strip()[1:-1].split(',')]

    def generate_task(self, input_file_name):
        with open(input_file_name) as input_file:
            grid_size = self.input_to_list(input_file.readline())
            start = self.input_to_list(input_file.readline())
            end = self.input_to_list(input_file.readline())

            obstacles = []

            for line in input_file:
                obstacles.append(self.input_to_list(line))

            task_space = [['o' for y in xrange(grid_size[1])] for x in xrange(grid_size[0])]

            for obstacle in obstacles:
                for x in xrange(obstacle[0], obstacle[0]+obstacle[2]):
                    for y in xrange(obstacle[1], obstacle[1]+obstacle[3]):
                        task_space[x][y] = 'x'

            return task_space, grid_size, start, end

    @staticmethod
    def arc_cost(parent_state, state):
        return 1

    @staticmethod
    def h(state, end_state):
        return abs(state[0] - end_state[0]) + abs(state[1] - end_state[1])

    @staticmethod
    def node_id(state):
        return '%d.%d' % (state[0], state[1])

    def get_neighbour_states(self, state):
        neighbour_states = []

        for i in xrange(-1, 2):
            x = state[0]+i

            if 0 <= x < self.grid_size[0]:
                for j in xrange(-1, 2):
                    y = state[1]+j

                    if 0 <= y < self.grid_size[1] and abs(i) != abs(j):
                        if [x, y] != state:
                            if self.task_space[x][y] == 'o':
                                neighbour_states.append([x, y])

        return neighbour_states


class BreadthFirst:
    def __init__(self, arc_cost, h, get_neighbour_states, node_id, ui, start, end, sleep_duration):
        print('Breadth first:')

        AStar(arc_cost, h, self.f, get_neighbour_states, node_id, ui, start, end, sleep_duration)

        print

    @staticmethod
    def f(open_list):
        return open_list[0]


class DepthFirst:
    def __init__(self, arc_cost, h, get_neighbour_states, node_id, ui, start, end, sleep_duration):
        print('Depth first:')

        AStar(arc_cost, h, self.f, get_neighbour_states, node_id, ui, start, end, sleep_duration)

        print

    @staticmethod
    def f(open_list):
        return open_list[-1]


class BestFirst:
    def __init__(self, arc_cost, h, get_neighbour_states, node_id, ui, start, end, sleep_duration):
        self.end = end

        print('Best first:')

        AStar(arc_cost, h, self.f, get_neighbour_states, node_id, ui, start, end, sleep_duration)

        print

    def f(self, open_list):
        return sorted(open_list, key=lambda x: -1 if x.state == self.end else (x.g+x.h))[0]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'You need to supply a file containing the problem description'
    else:
        if len(sys.argv) == 3:
            sleep = float(sys.argv[2])
        else:
            sleep = 0.5

        Run(sys.argv[1], sleep)
