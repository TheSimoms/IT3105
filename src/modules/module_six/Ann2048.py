import sys
import logging

import numpy

sys.path.append('../../')

from common.ann.ann import Ann

from common.twenty_forty_eight.twenty_forty_eight import TwentyFortyEight
from common.twenty_forty_eight.ui_simple import Ui


TRAINING_DATA_FILENAME = 'generated-training-data.txt'


class Ann2048:
    def __init__(self, hidden_layer_sizes, activation_functions, max_epochs, learning_rate, error_limit,
                 batch_size=100):
        self.hidden_layer_sizes = hidden_layer_sizes
        self.activation_functions = activation_functions
        self.max_epochs = max_epochs
        self.learning_rate = learning_rate
        self.error_limit = error_limit
        self.batch_size = batch_size

        self.ann = Ann(hidden_layer_sizes, activation_functions, 16, 4, learning_rate, error_limit,
                       batch_size, max_epochs)

    @staticmethod
    def nest_list(flat_list):
        """
        Nest list. Return a nested 4x4 version of the flat lits supplied

        :param flat_list: List to nest
        :return: Nested list
        """

        nested_list = numpy.array(flat_list)
        nested_list = numpy.reshape(nested_list, (4, 4))

        return list(nested_list.tolist())

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

    def pre_process(self, feature_sets):
        for feature_set in feature_sets:
            for i in range(len(feature_set)):
                feature_set[i] *= feature_set[i]

        return feature_sets

    def train(self, filename):
        """
        Train the network using supplied file

        :param filename: Filename containing training data
        """

        feature_sets, correct_labels = self.ann.load_data(filename)

        feature_sets = self.pre_process(feature_sets)

        self.ann.start_training(feature_sets, correct_labels)

    @staticmethod
    def list_from_integer(integer):
        return list(map(lambda x: (integer >> x*4) & 0xf, range(16)))

    def load_integer_formatted_data(self, filename):
        """
        Load data from a file, where the states are formatted as integers

        :param filename: Name of file containing data to load
        :return: Feature sets and labels from the supplied data
        """

        feature_sets = []
        correct_labels = []

        with open(filename, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                content = line.split(',')

                feature_sets.append(self.list_from_integer(int(content[0])))
                correct_labels.append(int(content[1]))

        return feature_sets, correct_labels

    def play_intelligently(self):
        """
        Play 2048 using the trained neural network

        :return: Highest tile achieved
        """

        logging.info('Playing using the neural network')

        ui = Ui()
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

    def run(self, filename=TRAINING_DATA_FILENAME):
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
        self.train(filename)

        # Playing using the neural network
        for i in range(50):
            results[1].append(self.play_intelligently())

        logging.info('Completed playing the intelligent games. Mean highest value: %f' % numpy.mean(results[1]))

        return results

    def generate_statistics(self, filename=TRAINING_DATA_FILENAME):
        """
        Run the module. Play 2048 50 times using random player, then 50 times using the neural network. Report results.

        :return: Results from all 100 playings, in two lists. One list for random, and one for intelligent
        """

        results = []

        try:
            for _ in range(50):
                # Training the neural network
                self.ann = Ann(self.hidden_layer_sizes, self.activation_functions, 16, 4, self.learning_rate,
                               self.error_limit, self.batch_size, self.max_epochs)
                self.train(filename)

                # Playing using the neural network
                results.append(self.play_intelligently())
        except KeyboardInterrupt:
            pass

        logging.info('Completed playing the intelligent games. Mean highest value: %f' % numpy.mean(results))

        return results

    def generate_training_data(self, filename=TRAINING_DATA_FILENAME):
        """
        Generate training data sets. Play the 2048 game using A*-GAC, and write every move made to supplied file

        :param filename: Filename to save the results to
        """

        while True:
            logging.info('Starting AI run')

            twenty_forty_eight = TwentyFortyEight()
            moves = twenty_forty_eight.run(twenty_forty_eight.make_player_move, True)

            logging.info('AI run completed. Saving to file')

            with open(filename, 'a') as f:
                for move in moves:
                    game_board = self.flatten_list(move[0])
                    move_made = move[1]

                    f.write('[%s] %d\n' % (','.join([str(element) for element in game_board]), move_made))

            logging.info('Moves successfully saved to file %s' % filename)
