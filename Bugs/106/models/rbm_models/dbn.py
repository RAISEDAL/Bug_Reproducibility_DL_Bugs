import numpy as np
import tensorflow as tf
from tensorflow.python.framework import ops

from models.rbm_models import rbm
from utils import utilities
import model

import json

class DBN(model.Model):

    """ Implementation of Deep Belief Network using TensorFlow.
    The interface of the class is sklearn-like.
    """

    def __init__(self, rbm_layers, do_pretrain=True, rbm_num_epochs=list([10]), rbm_batch_size=list([10]), model_name='dbn',
                 rbm_learning_rate=list([0.01]), rbm_names=list(['']), rbm_gibbs_k=list([1]), rbm_gauss_visible=False,
                 rbm_stddev=0.1, finetune_learning_rate=0.01, momentum=0.9, finetune_num_epochs=10,
                 finetune_batch_size=10, finetune_dropout=1, finetune_opt='gradient_descent', verbose=1,
                 finetune_act_func='relu', finetune_loss_func='mean_squared', main_dir='dbn/', dataset='mnist'):

        """
        :param rbm_layers: list containing the hidden units for each layer
        :param do_pretrain: whether to do unsupervised pretraining of the network
        :param rbm_num_epochs: number of epochs to train each rbm
        :param rbm_batch_size: batch size each rbm
        :param rbm_learning_rate: learning rate each rbm
        :param rbm_names: model name for each rbm
        :param rbm_gibbs_k: number of gibbs sampling steps for each rbm
        :param rbm_gauss_visible: whether the input layer should have gaussian units
        :param rbm_stddev: standard deviation for the gaussian layer
        :param finetune_dropout: dropout parameter
        :param verbose: Level of verbosity. 0 - silent, 1 - print accuracy. int, default 0
        """
        model.Model.__init__(self, model_name, main_dir)

        self._initialize_training_parameters(loss_func=finetune_loss_func, learning_rate=finetune_learning_rate,
                                             num_epochs=finetune_num_epochs, batch_size=finetune_batch_size,
                                             dropout=finetune_dropout, dataset=dataset, opt=finetune_opt,
                                             momentum=momentum)

        self.do_pretrain = do_pretrain
        self.layers = rbm_layers
        self.finetune_act_func = finetune_act_func
        self.verbose = verbose

        self.W_pretrain = None
        self.bh_pretrain = None
        self.bv_pretrain = None

        self.W_vars = None
        self.b_vars = None

        self.rbms = []

        for l, layer in enumerate(rbm_layers):

            if l == 0 and rbm_gauss_visible:

                # Gaussian visible units

                self.rbms.append(rbm.RBM(
                    visible_unit_type='gauss', stddev=rbm_stddev,
                    model_name=rbm_names[l] + str(l), num_hidden=rbm_layers[l],
                    main_dir=self.main_dir, learning_rate=rbm_learning_rate[l], gibbs_sampling_steps=rbm_gibbs_k[l],
                    verbose=self.verbose, num_epochs=rbm_num_epochs[l], batch_size=rbm_batch_size[l]))

            else:

                # Binary RBMs

                self.rbms.append(rbm.RBM(
                    model_name=rbm_names[l] + str(l), num_hidden=rbm_layers[l],
                    main_dir=self.main_dir, learning_rate=rbm_learning_rate[l], gibbs_sampling_steps=rbm_gibbs_k[l],
                    verbose=self.verbose, num_epochs=rbm_num_epochs[l], batch_size=rbm_batch_size[l]))

    def pretrain(self, train_set, validation_set=None):

        """ Perform unsupervised pretraining of the stack of restricted boltzmann machines.
        :param train_set: training set
        :param validation_set: validation set
        :return: return data encoded by the last layer
        """

        self.W_pretrain = []
        self.bh_pretrain = []
        self.bv_pretrain = []

        next_train = train_set
        next_valid = validation_set

        for l, rboltz in enumerate(self.rbms):
            print('Training layer {}...'.format(l+1))
            next_train, next_valid = self._pretrain_rbm_and_gen_feed(rboltz, next_train, next_valid)

            # Reset tensorflow's default graph between different models
            ops.reset_default_graph()

        return next_train, next_valid

    def _pretrain_rbm_and_gen_feed(self, rboltz, train_set, validation_set):

        """ Pretrain a single rbm and encode the data for the next layer.
        :param rboltz: rbm reference
        :param train_set: training set
        :param validation_set: validation set
        :return: encoded train data, encoded validation data
        """

        rboltz.build_model(train_set.shape[1])
        rboltz.fit(train_set, validation_set)
        params = rboltz.get_model_parameters()

        self.W_pretrain.append(params['W'])
        self.bh_pretrain.append(params['bh_'])
        self.bv_pretrain.append(params['bv_'])

        return rboltz.transform(train_set), rboltz.transform(validation_set)

    def fit(self, train_set, train_labels, validation_set=None, validation_labels=None, restore_previous_model=False):

        """ Perform supervised finetuning of the model.
        :param train_set: training set
        :param train_labels: training labels
        :param validation_set: validation set
        :param validation_labels: validation labels
        :param restore_previous_model:
                    if true, a previous trained model
                    with the same name of this model is restored from disk to continue training.
        :return: self
        """

        with tf.Session() as self.tf_session:
            self._initialize_tf_utilities_and_ops(restore_previous_model)
            self._train_model(train_set, train_labels, validation_set, validation_labels)
            self.tf_saver.save(self.tf_session, self.model_path)

    def _train_model(self, train_set, train_labels, validation_set=None, validation_labels=None):

        """ Train the model.
        :param train_set: training set
        :param train_labels: training labels
        :param validation_set: validation set
        :param validation_labels: validation labels
        :return:
        """

        shuff = list(zip(train_set, train_labels))

        for i in range(self.num_epochs):

            np.random.shuffle(shuff)
            batches = [_ for _ in utilities.gen_batches(shuff, self.batch_size)]

            for batch in batches:
                x_batch, y_batch = zip(*batch)
                feed = {self.input_data: x_batch, self.input_labels: y_batch, self.keep_prob: self.dropout}
                self.tf_session.run(self.train_step, feed_dict=feed)

            if validation_set is not None:
                self._run_validation_error_and_summaries(i, validation_set, validation_labels)

    def _run_validation_error_and_summaries(self, epoch, validation_set, validation_labels):

        """ Run the summaries and error computation on the validation set.
        :param epoch: current epoch number
        :param validation_set: validation set
        :param validation_labels: validation labels
        :return: self
        """

        feed = {self.input_data: validation_set, self.input_labels: validation_labels, self.keep_prob: 1}
        result = self.tf_session.run([self.tf_merged_summaries, self.cost], feed_dict=feed)
        summary_str = result[0]
        err = result[1]

        self.tf_summary_writer.add_summary(summary_str, epoch)

        if self.verbose == 1:
            print("Cost at step %s: %s" % (epoch, err))
            # ///////// Added By @Mehdi
            file = open(file="buggy/result.json", mode="w")  # Added By @Mehdi
            model_loss = np.float64(err)
            res = {"loss": model_loss}
            json.dump(res, file)
            file.close()

    def build_model(self, n_features, n_classes):

        """ Assume self.W, self.bh and self.bv contains trained parameters.
        :param n_features: number of features
        :param n_classes: number of classes
        :return: self
        """

        self._create_placeholders(n_features, n_classes)
        self._create_variables(n_features)

        next_train = self._forward_pass()
        self._create_softmax_layer(next_train, n_classes)

        self._create_cost_function_node(self.softmax_out, self.input_labels)
        self._create_train_step_node()
        self._create_test_node()

    def _create_placeholders(self, n_features, n_classes):

        """ Create the TensorFlow placeholders for the model.
        :param n_features: number of features of the first layer
        :param n_classes: number of classes
        :return: self
        """

        self.input_data = tf.placeholder('float', [None, n_features])
        self.input_labels = tf.placeholder('float', [None, n_classes])
        self.keep_prob = tf.placeholder('float')

    def _create_variables(self, n_features):

        """ Create the TensorFlow variables for the model.
        :param n_features: number of features
        :return: self
        """

        self.W_vars = []
        self.b_vars = []

        if self.do_pretrain:
            self._create_variables_pretrain()
        else:
            self._create_variables_no_pretrain(n_features)

    def _create_variables_no_pretrain(self, n_features):

        """ Create model variables (no previous unsupervised pretraining)
        :param n_features: number of features
        :return: self
        """

        for l, layer in enumerate(self.layers):

            if l == 0:
                self.W_vars.append(tf.Variable(tf.truncated_normal(shape=[n_features, self.layers[l]], stddev=0.1)))
                self.b_vars.append(tf.Variable(tf.constant(0.1, shape=[self.layers[l]])))
            else:
                self.W_vars.append(tf.Variable(tf.truncated_normal(shape=[self.layers[l - 1], self.layers[l]], stddev=0.1)))
                self.b_vars.append(tf.Variable(tf.constant(0.1, shape=[self.layers[l]])))

    def _create_variables_pretrain(self):

        """ Create model variables (previous unsupervised pretraining)
        :return: self
        """

        for l, layer in enumerate(self.layers):
            self.W_vars.append(tf.Variable(self.W_pretrain[l], name='w-{}'.format(l)))
            self.b_vars.append(tf.Variable(self.bh_pretrain[l], name='b-{}'.format(l)))

    def _forward_pass(self):

        """ Perform a forward pass through the layers of the network.
        :return: sampled units at the last layer
        """

        next_train = self.input_data

        for l, layer in enumerate(self.layers):

            activation = tf.matmul(next_train, self.W_vars[l]) + self.b_vars[l]

            if self.finetune_act_func == 'sigmoid':
                hprobs = tf.nn.sigmoid(activation)

            elif self.finetune_act_func == 'tanh':
                hprobs = tf.nn.tanh(activation)

            elif self.finetune_act_func == 'relu':
                hprobs = tf.nn.relu(activation)

            else:
                hprobs = None

            next_train = tf.nn.dropout(hprobs, self.keep_prob)

        return next_train

    def _create_softmax_layer(self, last_layer, n_classes):

        """ Create nodes for the softmax layer build on top of the last layer.
        :param last_layer: last layer output node
        :param n_classes: number of classes
        :return: self
        """
        self.softmax_W = tf.Variable(tf.truncated_normal([self.layers[-1], n_classes], stddev=0.1), name='sm-weights')
        self.softmax_b = tf.Variable(tf.constant(0.1, shape=[n_classes]), name='sm-biases')

        with tf.name_scope("softmax_layer"):
            self.softmax_out = tf.matmul(last_layer, self.softmax_W) + self.softmax_b

    def _create_test_node(self):

        """ Create validation testing node.
        :return: self
        """

        with tf.name_scope("test"):
            correct_prediction = tf.equal(tf.argmax(self.softmax_out, 1), tf.argmax(self.input_labels, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
            _ = tf.summary.scalar('accuracy', self.accuracy)

    def get_model_parameters(self):

        """ Return the model parameters in the form of numpy arrays.
        :return: model parameters
        """

        with tf.Session() as self.tf_session:

            self.tf_saver.restore(self.tf_session, self.model_path)

            def eval_tensors(tens, prefix):
                eval_tens = {}
                for i, t in enumerate(tens):
                    eval_tens[prefix + str(i)] = t.eval()

            return {
                'W': eval_tensors(self.W_vars, 'w'),
                'b': eval_tensors(self.b_vars, 'b'),
                'smW': self.softmax_W.eval(),
                'smb': self.softmax_b.eval()
            }

    def predict(self, test_set, test_labels):

        """ Predict the labels for the test set, and return the accuracy
        over the test set.
        :param test_set: test set
        :param test_labels: test labels
        :return: accuracy over the test set
        """

        with tf.Session() as self.tf_session:

            self.tf_saver.restore(self.tf_session, self.model_path)
            feed = {self.input_data: test_set, self.input_labels: test_labels, self.keep_prob: 1}

            return self.accuracy.eval(feed)
