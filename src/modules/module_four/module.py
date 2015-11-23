import sys

sys.path.append('../../')

from modules.module_four.twenty_forty_eight import TwentyFortyEight
from modules.module_four.ui import Ui


class ModuleFour:
    def __init__(self, height=800):
        self.ui = Ui(height)
        self.run()

    def run(self):
        twenty_forty_eight = TwentyFortyEight(ui=self.ui)

        twenty_forty_eight.run(twenty_forty_eight.make_player_move)

        try:
            input('Done. Press return to continue')
        except SyntaxError:
            pass

if __name__ == '__main__':
    ModuleFour()
