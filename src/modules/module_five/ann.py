import sys

import logging

import numpy
import numpy.random as rng

import theano
import theano.tensor as T

sys.path.append('../../')

from modules.module_five.mnist import mnist_basics


class Ann:
    def __init__(self, hidden_layer_sizes, activation_functions, number_of_inputs=784, number_of_outputs=10,
                 learning_rate=0.1, error_limit=1e-5):
        self.activation_functions = activation_functions
        self.number_of_inputs = number_of_inputs
        self.number_of_outputs = number_of_outputs
        self.learning_rate = learning_rate
        self.error_limit = error_limit

        if len(hidden_layer_sizes) != len(activation_functions):
            logging.error('The number of hidden layers and number of activation functions does not match')

            sys.exit(1)

        self.input_values = T.matrix('input_values')
        self.correct_labels = T.ivector('labels')

        self.hidden_layers = self.generate_hidden_layers(
            self.input_values, number_of_inputs, hidden_layer_sizes, activation_functions
        )

        self.output_layer = OutputLayer(
            self.hidden_layers[-1].output, hidden_layer_sizes[-1], number_of_outputs
        )

        self.training_function, self.testing_function = self.generate_functions()

    @staticmethod
    def generate_hidden_layers(input_values, number_of_inputs, hidden_layer_sizes, activation_functions):
        hidden_layers = [
            HiddenLayer(0, input_values, number_of_inputs, hidden_layer_sizes[0], activation_functions[0])
        ]

        for i in range(1, len(hidden_layer_sizes)):
            hidden_layers.append(
                HiddenLayer(
                    i, hidden_layers[i-1].output, hidden_layer_sizes[i-1],
                    hidden_layer_sizes[i], activation_functions[i]
                )
            )

        return hidden_layers

    def generate_functions(self):
        step_cost = -T.mean(
            T.log(self.output_layer.output)[T.arange(self.correct_labels.shape[0]), self.correct_labels]
        )

        # FIXME: Do the parameters thing in fewer lines
        parameters = []

        for hidden_layer in self.hidden_layers:
            parameters.extend(hidden_layer.parameters)

        parameters.extend(self.output_layer.parameters)

        gradients = T.grad(step_cost, parameters)

        back_propagation = [
            (parameter, parameter - self.learning_rate*gradient) for parameter, gradient in zip(parameters, gradients)
        ]

        training_function = theano.function(
            inputs=[self.input_values, self.correct_labels],
            outputs=self.output_layer.output_label,
            updates=back_propagation,
            allow_input_downcast=True
        )

        testing_function = theano.function(
            inputs=[self.input_values],
            outputs=self.output_layer.output_label,
            allow_input_downcast=True
        )

        return training_function, testing_function

    def train(self, filename='all_flat_mnist_training_cases', batch_size=100, max_epochs=100):
        logging.info('Entering training')
        logging.info('Loading training data from file \'mnist/%s\'' % filename)

        features, correct_labels = self.load_data(filename)

        logging.info('Loading complete')

        number_of_batches = int(len(features) / batch_size)
        mean_accuracy = 0.0

        logging.info('Starting training')

        epoch = 0

        while epoch < max_epochs and 1.0-mean_accuracy > self.error_limit:
            logging.info('Epoch %d' % epoch)

            training_accuracy = []

            for i in range(number_of_batches):
                batch_input_values = features[i * batch_size:(i+1) * batch_size]
                batch_labels = correct_labels[i * batch_size:(i+1) * batch_size]

                results = self.training_function(batch_input_values, batch_labels)
                accuracy = sum(results == batch_labels) / float(len(batch_labels))

                training_accuracy.append(accuracy)

            mean_accuracy = numpy.mean(training_accuracy)

            logging.info('Accuracy: %s%%' % str(mean_accuracy*100))

            epoch += 1

        logging.info('Training complete. An average accuracy of %s%% was achieved' % str(mean_accuracy*100))

    def blind_test(self, features, correct_labels):
        """
        Classify set of features

        :param features: List of feature sets to classify

        :return List of labels for classified feature sets
        """
        logging.info('Entering testing')

        self.normalize_features(features)

        results = self.testing_function(features)
        accuracy = sum(results == correct_labels) / float(len(correct_labels))

        logging.info('Testing complete. An accuracy of %s%% was achieved' % str(accuracy*100))

        return results

    @staticmethod
    def normalize_features(features, max_value=255.0):
        """
        Normalize list of feature sets to fit in range [0, 1]. Normalization is in place

        :param features: List of feature sets to normalize
        :param max_value: Maximum value, value to be normalized to 1.0
        """

        dimensions = len(features[0])

        for feature in features:
            for i in range(dimensions):
                feature[i] /= max_value

    def load_data(self, filename):
        features, labels = mnist_basics.load_cases(filename, nested=False)

        self.normalize_features(features)

        return features, labels


class HiddenLayer(object):
    def __init__(self, i, input_values, number_of_inputs, number_of_outputs, activation=T.tanh):
        weights = numpy.asarray(
            rng.normal(loc=0.0, scale=0.05, size=(number_of_inputs, number_of_outputs)), dtype=theano.config.floatX
        )
        weights = theano.shared(weights, name='weights_%d' % i)

        bias = numpy.zeros(shape=(number_of_outputs, ), dtype=theano.config.floatX)
        bias = theano.shared(bias, name='bias_%d' % i)

        self.output = activation(
            T.dot(input_values, weights) + bias
        )

        self.parameters = [weights, bias]


class OutputLayer(object):
    def __init__(self, input_values, number_of_inputs, number_of_outputs):
        weights = numpy.asarray(
            rng.normal(loc=0.0, scale=0.05, size=(number_of_inputs, number_of_outputs)), dtype=theano.config.floatX
        )
        weights = theano.shared(weights, name='weights_output')

        bias = numpy.zeros(shape=(number_of_outputs, ), dtype='float64')
        bias = theano.shared(bias, name='bias_output')

        self.output = T.nnet.softmax(
            T.dot(input_values, weights) + bias
        )
        self.output_label = T.argmax(self.output, axis=1)

        self.parameters = [weights, bias]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    ann = Ann([50, 20], [T.tanh, T.tanh])
