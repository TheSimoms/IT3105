import sys

import logging
import numpy

sys.path.append('../../')

from modules.module_five.ann import Ann

from modules.module_four.twenty_forty_eight import TwentyFortyEight
from modules.module_four.ui import Ui


TRAINING_DATA_FILENAME = 'generated-training-data.txt'


class Ann2048:
    def __init__(self, hidden_layer_sizes, activation_functions, number_of_inputs=16, number_of_outputs=4,
                 learning_rate=0.1, error_limit=1e-4, batch_size=100, max_epochs=100, height=800):
        self.ann = Ann(hidden_layer_sizes, activation_functions, number_of_inputs, number_of_outputs,
                       learning_rate, error_limit, batch_size, max_epochs)

        self.height = height

    @staticmethod
    def flatten_list(nested_list):
        """
        Flatten list. Return a flat version of the supplied nested list

        :param nested_list: Nested list to flatten
        :return: Flattened list
        """

        def kd_reduce(func, seq):
            res = seq[0]

            for item in seq[1:]:
                res = func(res, item)
            return res

        def flatten(a, b):
            return a + b

        return kd_reduce(flatten, nested_list)

    def train(self, filename=TRAINING_DATA_FILENAME):
        """
        Train the network using supplied file

        :param filename: Filename containing training data
        """

        feature_sets, correct_labels = self.ann.load_data(filename)

        self.ann.start_training(feature_sets, correct_labels)

    def play_intelligently(self):
        """
        Play 2048 using the trained neural network

        :return: Highest tile achieved
        """

        logging.info('Playing using the neural network')

        ui = Ui(self.height)
        twenty_forty_eight = TwentyFortyEight(ui=ui)

        is_game_over = not twenty_forty_eight.make_computer_move()

        # Makes moves as long as the game isn't lost yet
        while not is_game_over:
            # Makes the move
            board_state = self.flatten_list(twenty_forty_eight.game_board.get_cell_values())
            next_moves = self.ann.testing_function_list([board_state])[0]

            moved = False
            illegal_moves = 0

            while not moved:
                next_move_index = next_moves.argmax()
                moved = twenty_forty_eight.game_board.make_player_move(next_move_index)

                if not moved:
                    next_moves[next_move_index] = -1
                    illegal_moves += 1

                    if illegal_moves == 4:
                        break

            # Updates UI, if any
            if not moved and ui:
                ui.update_ui(twenty_forty_eight.game_board.state)

            # Spawns new value
            is_game_over = not twenty_forty_eight.make_computer_move()

        result = 2 ** twenty_forty_eight.game_board.get_max_value()

        logging.info('Result: %d' % result)

        # Returns final score
        return result

    @staticmethod
    def play_randomly():
        """
        Play 2048 using only random moves

        :return: Highest tile achieved
        """

        twenty_forty_eight = TwentyFortyEight()

        logging.info('Playing using random moves')

        result = twenty_forty_eight.run(twenty_forty_eight.make_random_move)

        logging.info('Result: %d' % result)

        return result

    def run(self):
        """
        Run the module. Play 2048 50 times using random player, then 50 times using the neural network. Report results.

        :return: Results from all 100 playings, in two lists. One list for random, and one for intelligent
        """

        results = [
            [],  # Random
            []  # Intelligently
        ]

        # Playing using random player
        for i in range(50):
            results[0].append(self.play_randomly())

        logging.info('Completed playing the random games. Mean highest value: %f' % numpy.mean(results[0]))

        # Training the neural network
        self.train()

        # Playing using the neural network
        for i in range(50):
            results[1].append(self.play_intelligently())

        logging.info('Completed playing the intelligent games. Mean highest value: %f' % numpy.mean(results[1]))

        return results

    def generate_training_data(self, filename=TRAINING_DATA_FILENAME):
        """
        Generate training data sets. Play the 2048 game using A*-GAC, and write every move made to supplied file

        :param filename: Filename to save the results to
        """

        logging.info('Starting AI run')

        twenty_forty_eight = TwentyFortyEight()
        moves = twenty_forty_eight.run(twenty_forty_eight.make_player_move, True)

        logging.info('AI run completed. Saving to file')

        with open(filename, 'w') as f:
            for move in moves:
                game_board = self.flatten_list(move[0])
                move_made = move[1]

                f.write('[%s] %d\n' % (','.join([str(element) for element in game_board]), move_made))

        logging.info('Moves successfully saved to file %s' % filename)
