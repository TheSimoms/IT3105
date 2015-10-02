from common.csp.csp import CSP


class CSPAStar(object):
    def __init__(self, variables, constraints, a_star, node, ui):
        self.csp = CSP(variables, constraints)

        self.a_star = a_star
        self.node = node
        self.ui = ui

    def run(self):
        result = self.csp.gac()

        if result:
            print('Solution found!')
        elif result is not None:
            print('No solution found. Solving using A*.')

        if result is not None:
            return self.a_star(self.node(None, self.csp), self.ui).run()
        else:
            print('No solution possible!')
