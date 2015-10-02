from common.a_star.node import Node as BaseNode


class Node(BaseNode):
    def __init__(self, parent, state, end_state):
        super(Node, self).__init__(parent, state, end_state)

    # Function for getting neighbour states
    def generate_neighbours(self, task_space=None):
        neighbours = []
        grid_size = [len(task_space), len(task_space[0])]

        # Iterates through all neighbour positions in the horizontal direction.
        for i in range(-1, 2):
            x = self.state[0]+i

            if 0 <= x < grid_size[0]:
                # If x is in the allowed range; iterates through all neighbour positions in the vertical direction
                for j in range(-1, 2):
                    y = self.state[1]+j

                    # If the neighbour is in the allowed range, and not a diagonal neighbour, proceed
                    if 0 <= y < grid_size[1] and abs(i) != abs(j):
                        # If not own state, proceed
                        if [x, y] != self.state:
                            # If neighbour is not an obstacle, add neighbour
                            if task_space[x][y] == 'o':
                                neighbours.append(Node(self, [x, y], self.end_state))

        return neighbours

    # Node identifier. 'x.y'
    def generate_id(self):
        return '%d.%d' % (self.state[0], self.state[1])

    # Returns whether state is goal state
    def is_solution(self):
        return self.state == self.end_state

    # h function. Manhattan distance
    def heuristic(self):
        return abs(self.state[0] - self.end_state[0]) + abs(self.state[1] - self.end_state[1])
