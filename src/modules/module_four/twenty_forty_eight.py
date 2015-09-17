from numpy.random import choice

from modules.module_four.ui import Ui


class TwentyFortyEight:
    def __init__(self, height=800):
        self.game_board = GameBoard(height)

    def get_next_player_move(self, state):
        pass


class GameBoard:
    def __init__(self, height=800):
        self.ui = Ui(height)

    @staticmethod
    def get_next_spawning():
        return str(choice([2, 4], p=[0.9, 0.1]))

    # FIXME: Do this a better way
    def get_next_computer_move(self, state):
        index_of_next_new_cell = int(choice(range(state.count('0'))))
        index_found = 0

        for i in range(len(state)):
            value = int(state[i])

            if not value and index_found == index_of_next_new_cell:
                next_state = state[:i]+self.get_next_spawning()+state[i+1:]

                self.ui.update_ui(next_state)

                return next_state
            elif not value:
                index_found += 1
