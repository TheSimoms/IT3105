import sys

import logging

import theano.tensor as T

sys.path.append('../../')

from modules.module_six.Ann2048 import Ann2048
from modules.module_six.ai2048demo import welch


class ModuleSix:
    def __init__(self, hidden_layer_sizes, activation_functions, max_epochs=50, learning_rate=0.1, error_limit=1e-3):
        self.ann_2048 = Ann2048(hidden_layer_sizes, activation_functions, learning_rate=learning_rate,
                                error_limit=error_limit, max_epochs=max_epochs)

    def run(self):
        results = self.ann_2048.run(filename=None)
        welch_results = welch(results[0], results[1])

        logging.info('Results: %s' % str(results))
        logging.info('Welch results: %s' % welch_results)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    module = ModuleSix([1024, 512], [T.nnet.softplus, T.nnet.softplus])

    if len(sys.argv) > 1 and sys.argv[1] == 'train':
        module.ann_2048.generate_training_data()
    else:
        module.run()
