import sys

sys.path.append('../../')

from modules.module_four.twenty_forty_eight import TwentyFortyEight
from modules.module_four.ui import Ui


class ModuleFour:
    def __init__(self, height=800):
        self.ui = Ui(height)
        self.run()

    def run(self):
        TwentyFortyEight(ui=self.ui).run()

        try:
            input('Done. Press return to continue')
        except SyntaxError:
            pass

if __name__ == '__main__':
    ModuleFour()
