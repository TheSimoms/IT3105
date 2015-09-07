from common.a_star.node import Node as BaseNode


class Node(BaseNode):
    def __init__(self, parent, state, end_state):
        super(Node, self).__init__(parent, state, end_state)

    # Function for getting neighbour states
    def generate_neighbours(self, task_space):
        neighbours = []
        grid_size = [len(task_space), len(task_space[0])]

        for i in range(-1, 2):
            x = self.state[0]+i

            if 0 <= x < grid_size[0]:
                for j in range(-1, 2):
                    y = self.state[1]+j

                    if 0 <= y < grid_size[1] and abs(i) != abs(j):
                        if [x, y] != self.state:
                            if task_space[x][y] == 'o':
                                neighbours.append(Node(self, [x, y], self.end_state))

        return neighbours

    # Node identifier
    def generate_id(self):
        return '%d.%d' % (self.state[0], self.state[1])

    def is_solution(self):
        return self.state == self.end_state

    # h function
    def heuristic(self, end_state=None):
        return abs(self.state[0] - end_state[0]) + abs(self.state[1] - end_state[1])

    # g function
    def arc_cost(self, neighbour_state):
        return 1
