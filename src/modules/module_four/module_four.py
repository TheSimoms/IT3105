import sys

from modules.module_four.twenty_forty_eight import TwentyFortyEight
from modules.module_four.ui import Ui


class ModuleFour:
    def __init__(self, sleep_duration=0.0, height=800):
        self.sleep_duration = sleep_duration

        self.ui = Ui(height)

        self.run()

    def run(self):
        twenty_forty_eight = TwentyFortyEight(2, self.ui)

        twenty_forty_eight.run()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        sleep = float(sys.argv[1])
    else:
        sleep = 0.0

    if len(sys.argv) == 3:
        ModuleFour(sleep, sys.argv[2])
    else:
        ModuleFour(sleep)
