from common.a_star.a_star import AStar as BaseAStar
from modules.module_one.ui import Ui


class AStar(BaseAStar):
    def __init__(self, task_space, start, end, title, sleep_duration=0.0):
        self.title = title

        ui = Ui(self.title, task_space).draw_node

        super(AStar, self).__init__(task_space, start, end, ui, sleep_duration)

        print('%s:' % self.title)
        self.run()
        print('')

    # Reports the number of open, closed, and total nodes expanded
    def report(self, open_nodes, closed_nodes):
        print('Open: %d, closed: %s, total: %d' % (
            len(open_nodes),
            len(closed_nodes),
            len(open_nodes)+len(closed_nodes)
        ))

        try:
            input('Press return to continue')
        except SyntaxError:
            pass
