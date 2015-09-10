class CSPAStar(object):
    def __init__(self, csp, a_star):
        self.csp = csp
        self.a_star = a_star

    def run(self):
        result = self.csp.gac()

        if result:
            print('Solution found!')
        elif result is not None:
            print('No solution found. Solving using A*')

            return self.a_star.run()
        else:
            print('No solution possible!')
