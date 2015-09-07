from common.a_star.a_star import AStar as BaseAStar


class AStar(BaseAStar):
    def __init__(self, node_class, task_space, start, end, title, sleep_duration=0.0):
        self.title = title

        super(AStar, self).__init__(node_class, task_space, start, end, ui, sleep_duration)

    def f(self):
        pass
