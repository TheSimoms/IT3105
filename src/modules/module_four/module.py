import sys
import logging

sys.path.append('../../')

from common.twenty_forty_eight.twenty_forty_eight import TwentyFortyEight
from common.twenty_forty_eight.ui_simple import Ui


class ModuleFour:
    def __init__(self):
        self.ui = Ui()
        self.run()

    def run(self):
        twenty_forty_eight = TwentyFortyEight(ui=self.ui)

        twenty_forty_eight.run(twenty_forty_eight.make_player_move)

        try:
            input('Done. Press return to continue')
        except SyntaxError:
            pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    ModuleFour()
