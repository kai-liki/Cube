import random
from model import Cube
from cube.model import F, B, R, L, U, D, F_, B_, R_, L_, U_, D_, DIRECTIONS, DIRECTION_OFFSET
import tensorflow as tf
import struct
import os, os.path


CUBE_DATA_LEN = 66
FEATURE_DATA_LEN = 54
TAG_DATA_LEN = 12


class CubeDataReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_pointer = None

    def begin_read(self):
        if self.file_pointer is None:
            self.file_pointer = open(self.file_path, 'r')

    def read(self, count=-1):
        result = {'feature': [], 'direction': []}
        is_eof = False
        i = 0
        while count < 0 or i < count:
            step_sample = []
            for j in range(0, CUBE_DATA_LEN):
                data = self.file_pointer.read(4)
                if '' == data:
                    is_eof = True
                else:
                    step_sample.append(self.data_to_float(data))
            if is_eof:
                break

            result['feature'].append(step_sample[:-TAG_DATA_LEN])
            result['direction'].append(step_sample[-TAG_DATA_LEN:])

            i = i + 1
        return result

    def finish_read(self):
        if self.file_pointer is not None:
            self.file_pointer.close()

    def data_to_float(self, buff):
        buf = struct.unpack_from('f', buffer=buff)
        return buf[0]


def train_and_test(sample_data_file, test_data_file):
    train_data_reader = CubeDataReader(sample_data_file)

    x = tf.placeholder("float", [None, FEATURE_DATA_LEN])
    W = tf.Variable(tf.zeros([FEATURE_DATA_LEN, TAG_DATA_LEN]))
    b = tf.Variable(tf.zeros([TAG_DATA_LEN]))
    y = tf.nn.softmax(tf.matmul(x, W) + b)

    y_ = tf.placeholder("float", [None, TAG_DATA_LEN])
    cross_entropy = -tf.reduce_sum(y_ * tf.log(y))
    train_step = tf.train.GradientDescentOptimizer(0.001).minimize(cross_entropy)

    print 'tf global_variables_initializer.'
    init = tf.global_variables_initializer()

    sess = tf.Session()
    sess.run(init)

    saver = tf.train.Saver()
    train_dir = './train_dir/'

    if os.path.exists(train_dir):
        saver.restore(sess=sess, save_path=train_dir)
    else:
        os.mkdir(train_dir)
        # Start training
        train_data_reader.begin_read()
        try:
            for i in range(4000):
                train_data = train_data_reader.read(10000)
                batch_xs = train_data['feature']
                batch_ys = train_data['direction']
                sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
                # saver.save(sess=sess, save_path=train_dir)
                print 'Training round %s finished.' % i
        except Exception as ex:
            train_data_reader.finish_read()
            print 'Training data read error! %s' % ex.message
            exit(1)
        train_data_reader.finish_read()
        saver.save(sess=sess, save_path=train_dir)

    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

    print 'Run test'
    test_data_reader = CubeDataReader(test_data_file)
    test_data_reader.begin_read()
    try:
        test_data = test_data_reader.read()
    except Exception as ex:
        test_data_reader.finish_read()
        print 'Test data read error! %s' % ex.message
        exit(1)
    test_data_reader.finish_read()
    print sess.run(accuracy, feed_dict={x: test_data['feature'], y_: test_data['direction']})





