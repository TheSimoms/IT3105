import itertools


class CSP(object):
    def __init__(self, variables, constraints):
        self.variables = variables
        self.constraints = constraints

        self.queue = set()

    @staticmethod
    def satisfies(c, arguments):
        for variable_combination in list(itertools.product(*arguments)):
            if apply(c.constraint, variable_combination):
                return True

        return False

    def extend_queue(self, x_star=None, c_k=None):
        for c in self.constraints:
            if c != c_k:
                if x_star in c.variables or x_star is None:
                    self.queue.update([(x, c) for x in c.variables if x != x_star])

    def revise(self, x, c):
        revised = False

        for i in range(len(self.variables[x])-1, -1, -1):
            arguments = [[self.variables[x][i]] if x == variable
                         else self.variables[variable] for variable in c.variables]

            if not self.satisfies(c, arguments):
                self.variables[x].pop(i)

                revised = True

        return revised

    def initialize(self):
        self.extend_queue()

    def domain_filtering_loop(self):
        while self.queue:
            x, c = self.queue.pop()

            if self.revise(x, c):
                if not self.variables[x]:
                    return False

                self.extend_queue(x, c)

        return True

    def rerun(self, variable, value):
        self.variables[variable] = [value]

        self.extend_queue(variable)
        self.domain_filtering_loop()

    def gac(self):
        self.initialize()

        if self.domain_filtering_loop():
            return self.variables
        else:
            return None


class ConstraintInstance(object):
    def __init__(self, variables, expression):
        self.variables = variables
        self.constraint = self.generate_function(variables, expression)

    @staticmethod
    def generate_function(variables, expression, environment=globals()):
        arguments = ",".join(variables)

        return eval("(lambda %s: %s)" % (arguments, expression), environment)
