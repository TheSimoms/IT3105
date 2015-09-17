import sys

from modules.module_four.twenty_forty_eight import TwentyFortyEight


class ModuleFour:
    def __init__(self, sleep_duration=0.0, height=800):
        self.height = height
        self.sleep_duration = sleep_duration

        self.run()

    def run(self):
        twenty_forty_eight = TwentyFortyEight()

        print twenty_forty_eight.game_board.smoothness()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        sleep = float(sys.argv[1])
    else:
        sleep = 0.0

    if len(sys.argv) == 3:
        ModuleFour(sleep, sys.argv[2])
    else:
        ModuleFour(sleep)
