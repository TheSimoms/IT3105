import itertools


class CSP(object):
    def __init__(self, variables, constraints):
        self.variables = variables  # Dictionary with key variable name and value domain
        self.constraints = constraints  # List of ConstraintInstances

        self.queue = set()  # Revise queue

    # Extends queue, either filtering on variable, constraint, or both
    def extend_queue(self, x_star=None, c_k=None):
        for c in self.constraints:
            if c != c_k:
                if x_star in c.variables or x_star is None:
                    self.queue.update([(x, c) for x in c.variables if x != x_star])

    # Revise* function. Removes any illegal values from the domain of x
    def revise(self, x, c):
        revised = False

        for i in range(len(self.variables[x])-1, -1, -1):
            arguments = [[self.variables[x][i]] if x == variable else
                         self.variables[variable] for variable in c.variables]

            if not c.satisfies(arguments):
                self.variables[x].pop(i)

                revised = True

        return revised

    # Domain filtering loop. Returns None if no solution is possible, whether a solution is found if not
    def domain_filtering_loop(self):
        while self.queue:
            x, c = self.queue.pop()

            if self.revise(x, c):
                if not self.variables[x]:
                    return None

                self.extend_queue(x, c)

        return self.is_solution()

    # Returns whether the current state is a solution or not
    def is_solution(self):
        for variable in self.variables:
            if len(self.variables[variable]) > 1:
                return False

        return True

    # Reruns the algorithm with the assumption that a given variable has taken on a certain value
    def rerun(self, variable, value):
        self.variables[variable] = [value]
        self.extend_queue(variable)

        return self.domain_filtering_loop()

    # The GAC function. Initializes with all combinations of variables and constraints and runs domain filtering loop
    def gac(self):
        self.extend_queue()

        return self.domain_filtering_loop()


# A ConstraintInstance hold the constraint itself as a function, and the variables in the constraint
class ConstraintInstance(object):
    def __init__(self, variables, expression):
        self.variables = variables
        self.constraint = self.generate_function(variables, expression)

    # Checks whether a combination of variable values is valid or not
    def satisfies(self, arguments):
        for variable_combination in list(itertools.product(*arguments)):
            if apply(self.constraint, variable_combination):
                return True

        return False

    # Generates the constraint function from the constraint expression
    @staticmethod
    def generate_function(variables, expression, environment=globals()):
        return eval("(lambda %s: %s)" % (",".join(variables), expression), environment)
