from copy import deepcopy

from common.a_star.node import Node as BaseNode
from common.csp.csp import CSP


class Node(BaseNode):
    def __init__(self, parent, state, end_state=None):
        super(Node, self).__init__(parent, state, end_state)

    # Function for getting neighbour states
    def generate_neighbours(self, task_space=None):
        neighbours = []

        variables = self.state.variables
        constraints = self.state.constraints

        # Picks the variable with fewest possible values left
        next_variable = min((variable for variable in variables if len(variables[variable]) != 1),
                            key=lambda variable: len(variables[variable]))

        # Adds neighbour for each legal value in the variable's domain. Reruns GAC for each value
        for value in variables[next_variable]:
            csp = CSP(deepcopy(variables), constraints)

            if csp.rerun(next_variable, value) is not None:
                neighbours.append(Node(self, csp))

        return neighbours

    # Node identifier
    def generate_id(self):
        return str([self.state.variables[variable] for variable in sorted(self.state.variables.keys())])

    # Returns whether the node is a solution or not
    def is_solution(self):
        for number_of_values in self.get_number_of_possible_values():
            if number_of_values != 1:
                return False

        return True

    # h function
    def heuristic(self, end_state=None):
        return sum(self.get_number_of_possible_values())

    # g function
    def arc_cost(self, neighbour_state):
        return 1

    # Returns list of possible values for each variable
    def get_number_of_possible_values(self):
        return [len(values) for values in self.state.variables.values()]
