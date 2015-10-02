from common.a_star.a_star import AStar as BaseAStar


class AStar(BaseAStar):
    def __init__(self, start, ui):
        super(AStar, self).__init__(start, ui)

    # Reports the number of open, closed, and total nodes expanded
    def report(self, final_node, open_nodes, closed_nodes):
        print('Total number of nodes: %s' % (len(open_nodes)+len(closed_nodes)))
        print('Number of expanded nodes: %d' % len(closed_nodes))
        print('Path length: %d' % len(self.build_path(final_node)))

        try:
            input('Press return to continue')
        except SyntaxError:
            pass
