from common.csp.csp import CSP


class CSPAStar(object):
    def __init__(self, variables, constraints, a_star, node, ui):
        self.csp = CSP(variables, constraints)  # Initializes the CSP

        self.a_star = a_star  # A* class
        self.node = node  # Node class
        self.ui = ui  # UI callback function

    def run(self):
        # Runs the CSP GAC algorithm
        result = self.csp.gac()

        # I solution is found, show it in the UI
        if result:
            print('Solution found using CSP! No search nodes have been generated.')

            self.ui(self.node(None, self.csp), None, None)

            try:
                input('Press return to continue')
            except SyntaxError:
                pass
        # If no solution is found, use A*
        elif result is not None:
            print('No solution found. Solving using A*.\n')

            return self.a_star(self.node(None, self.csp), self.ui).run()
        # If no solution is possible, say so
        else:
            print('No solution possible!')
