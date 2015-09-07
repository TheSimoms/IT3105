from common.a_star.node import Node as BaseNode


class Node(BaseNode):
    def __init__(self, parent, state, end_state):
        super(Node, self).__init__(parent, state, end_state)

    # Function for getting neighbour states
    def generate_neighbours(self, task_space):
        neighbours = []

        return neighbours

    # Node identifier
    def generate_id(self):
        pass

    # h function
    def heuristic(self, end_state):
        pass

    # g function
    def arc_cost(self, neighbour_state):
        return 1
