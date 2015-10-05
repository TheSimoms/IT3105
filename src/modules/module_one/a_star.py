from common.a_star.a_star import AStar as BaseAStar
from modules.module_one.ui import Ui


class AStar(BaseAStar):
    def __init__(self, task_space, start, end, title, sleep_duration=0.0):
        self.title = title  # Adds title to UI window. Breadth-, depth- or best first

        # Creates a new UI instance
        ui = Ui(self.title, task_space).draw_node

        # Initialises the algorithm
        super(AStar, self).__init__(start, ui, end, task_space, sleep_duration)

        print('%s:' % self.title)

        # Runs the algorithm
        self.run()

        # Pause to see the result
        try:
            input('Press return to continue\n')
        except SyntaxError:
            pass
