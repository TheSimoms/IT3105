from common.a_star.a_star import AStar as BaseAStar
from modules.module_one.ui import Ui


class AStar(BaseAStar):
    def __init__(self, node_class, task_space, start, end, title, sleep_duration=0.0):
        self.title = title

        ui = Ui(self.title, task_space).draw_node

        super(AStar, self).__init__(node_class, task_space, start, end, ui, sleep_duration)

        print('%s:' % self.title)
        self.run()
        print('')

    def f(self):
        raise NotImplementedError
