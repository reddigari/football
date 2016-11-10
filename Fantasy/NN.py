import numpy as np
import pandas as pd
import tensorflow as tf
import random

def format_ffdata(row):
    outcome = row['FFPts_real']
    vector = row[[u'Week', u'RsAtt', u'RsYds', u'RsTD', u'Rec', u'RcYds', u'RcTD', u'Fum', u'FumL', u'FFPts']].values
    return dict(outcome=outcome, vector=vector)


def evaluate_classifier(classifier, eval_set):
    hypotheses = classifier(eval_set)
    actual = [i['outcome'] for i in eval_set]
    return np.corrcoef(hypotheses, actual)[0,1]**2


class FantasyNN:
    def __init__(self, dim):
        # Define the hyperparameters
        self.learning_rate = 1e-6
        self.training_epochs = 10000  # How long to train for - chosen to fit within class time
        self.display_epoch_freq = 10  # How often to test and print out statistics
        self.dim = dim  # The number of features
        self.batch_size = 512  # Somewhat arbitrary - can be tuned, but often tune for speed, not accuracy

        # TODO: Use these.
        self.hidden_layer_size = 16
        self.keep_rate = 1.0
        self.mean = 0.0
        self.stdev = 1.0
        # TODO: Overwrite this section
        ### Start of model definition ###

        # Define the inputs
        self.x = tf.placeholder(tf.float32, [None, self.dim])
        self.y = tf.placeholder(tf.float32, [None])
        self.keep_rate_ph = tf.placeholder(tf.float32, [])

        # Define (most of) the model
        self.W0 = tf.Variable(tf.random_normal([self.dim, self.hidden_layer_size], mean=self.mean, stddev=self.stdev))
        self.b0 = tf.Variable(tf.random_normal([self.hidden_layer_size], stddev=0.1))

        self.h0 = tf.nn.relu(tf.matmul(self.x, self.W0) + self.b0)
        # self.h0 = tf.nn.dropout(self.h0, self.keep_rate_ph)

        self.W1 = tf.Variable(tf.random_normal([self.hidden_layer_size, 1], mean=self.mean, stddev=self.stdev))
        self.b1 = tf.Variable(tf.random_normal([1], stddev=0.1))

        self.predicted = tf.matmul(self.h0, self.W1) + self.b1
        # self.predicted = tf.Print(self.predicted, [self.predicted])

        ### End of model definition ###

        self.cost = tf.reduce_sum(tf.square(self.predicted-tf.reshape(self.y, [-1, 1])))

        # Define the cost function (here, the exp and sum are built in)
        # self.cost = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(self.logits, self.y))

        # This library call performs the main SGD update equation
        self.optimizer = tf.train.GradientDescentOptimizer(self.learning_rate).minimize(self.cost)

        # Create an operation to fill zero values in for W and b
        self.init = tf.initialize_all_variables()

        # Create a placeholder for the session that will be shared between training and evaluation
        self.sess = None

    def train(self, training_data, dev_set):
        def get_minibatch(dataset, start_index, end_index):
            indices = range(start_index, end_index)
            vectors = np.vstack([dataset[i]['vector'] for i in indices])
            outcomes = [dataset[i]['outcome'] for i in indices]
            return vectors, outcomes

        self.sess = tf.Session()

        self.sess.run(self.init)
        print 'Training.'

        # Training cycle
        for epoch in range(self.training_epochs):
            random.shuffle(training_set)
            avg_cost = 0.
            total_batch = int(len(training_set) / self.batch_size)

            # Loop over all batches in epoch
            for i in range(total_batch):
                # Assemble a minibatch of the next B examples
                minibatch_vectors, minibatch_labels = get_minibatch(training_set,
                                                                    self.batch_size * i,
                                                                    self.batch_size * (i + 1))

                # print minibatch_vectors

                # Run the optimizer to take a gradient step, and also fetch the value of the
                # cost function for logging
                _, c = self.sess.run([self.optimizer, self.cost],
                                     feed_dict={self.x: minibatch_vectors,
                                                self.y: minibatch_labels,
                                                self.keep_rate_ph: self.keep_rate})

                # Compute average loss
                avg_cost += c / (total_batch * self.batch_size)

            # Display some statistics about the step
            if (epoch+1) % self.display_epoch_freq == 0:
                print "Epoch:", (epoch+1), "Cost:", avg_cost, \
                    "Dev R2:", evaluate_classifier(self.classify, dev_set[0:500]), \
                    "Train R2:", evaluate_classifier(self.classify, training_set[0:500])

    def classify(self, examples):
        # This classifies a list of examples
        vectors = np.vstack([example['vector'] for example in examples])
        preds = self.sess.run(self.predicted, feed_dict={self.x: vectors, self.keep_rate_ph: 1.0})
        return preds.flatten()
