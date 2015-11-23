import sys

import logging

import theano.tensor as T

sys.path.append('../../')

from modules.module_five.ann import Ann
from modules.module_five.mnist import mnist_basics, mnistdemo


class ModuleFive:
    def __init__(self, hidden_layer_sizes, activation_functions, learning_rate=0.1, error_limit=1e-4, max_epochs=50):
        self.ann = Ann(hidden_layer_sizes, activation_functions, learning_rate=learning_rate,
                       error_limit=error_limit, max_epochs=max_epochs)

    def run(self, r=0):
        epochs, accuracy = self.ann.train_mnist()

        return mnistdemo.major_demo(self.ann, r, mnist_basics.__mnist_path__), epochs, accuracy


def demo(r):
    results = ModuleFive([784, 392, 196], [T.tanh, T.tanh, T.tanh]).run(r)

    logging.info('Scores: %s' % str(results[0]))
    logging.info('Epochs: %s, accuracy: %s' % (str(results[1]), str(results[2])))


def test_configurations(number_of_runs=5):
    results = eval(repr([[0]*5]*5))
    configurations = [
        [[200, 100], [T.tanh, T.tanh]],
        [[100, 200, 100], [T.tanh, T.tanh, T.tanh]],
        [[100, 250, 50], [T.tanh, T.tanh, T.tanh]],
        [[392, 196, 98], [T.tanh, T.tanh, T.tanh]],
        [[784, 392, 196], [T.tanh, T.tanh, T.tanh]]
    ]

    for i in range(len(configurations)):
        logging.info('Entering configuration %d' % i)

        for j in range(number_of_runs):
            logging.info('Configuration %d, run %d' % (i, j))

            result = ModuleFive(configurations[i][0], configurations[i][1]).run()

            logging.info('Results: %s' % str(result))

            results[i][0] += float(result[0][0]) / number_of_runs
            results[i][1] += float(result[0][1]) / number_of_runs
            results[i][2] += float(result[0][2]) / number_of_runs
            results[i][3] += float(result[1]) / number_of_runs
            results[i][4] += float(result[2]) / number_of_runs

        logging.info('Configuration %d completed' % i)
        logging.info('Results %d: %s' % (i, str(results[i][:3])))
        logging.info('Data %d: %s' % (i, str(results[i][3:])))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) < 2:
        logging.error('You need to supply at least one argument. Either \'test\' for testing, or an integer')

        sys.exit(1)

    if sys.argv[1] == 'test':
        test_configurations()
    else:
        demo(sys.argv[1])
