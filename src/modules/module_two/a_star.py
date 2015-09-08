from common.a_star.a_star import AStar as BaseAStar


class AStar(BaseAStar):
    def __init__(self, start, ui, sleep_duration=0.0):
        super(AStar, self).__init__(None, start, None, ui, sleep_duration)

    def f(self):
        return sorted(self.open, key=lambda x: -1 if x.is_solution() else (x.g+x.h))[0]

    # Reports the number of open, closed, and total nodes expanded
    def report(self, open_nodes, closed_nodes):
        print('Open: %d, closed: %s, total: %d' % (
            len(open_nodes),
            len(closed_nodes),
            len(open_nodes)+len(closed_nodes)
        ))
