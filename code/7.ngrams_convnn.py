from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.data_utils import to_categorical, pad_sequences
from tflearn.datasets import imdb
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
from keras.preprocessing.text import Tokenizer, text_to_word_sequence
from tflearn.layers.recurrent import bidirectional_rnn, BasicLSTMCell
from tflearn.layers.conv import conv_1d, global_max_pool
from tflearn.layers.merge_ops import merge
import tensorflow as tf
import pickle

import tflearn
from tflearn.data_utils import to_categorical, pad_sequences
from tflearn.datasets import imdb
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.embedding_ops import embedding
from tflearn.layers.recurrent import bidirectional_rnn, BasicLSTMCell
from tflearn.layers.estimator import regression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import numpy as np
import matplotlib.pyplot as plt
import itertools

LOGDIR = "../../../tflearn_logs/"

POS = open('../Data/UDP_tags_nli.txt', 'r')
POS_list = POS.readlines()
POS_list = [x.strip() for x in POS_list] 

tknzr = Tokenizer(lower=False, split=" ")
tknzr.fit_on_texts(POS_list)
#vocabulary:
print ("Got POS tags")
X = tknzr.texts_to_sequences(POS_list)

lang = open('../Data/UDP_labels_nli.txt','r')
lang_list = lang.readlines()
lang_list = [x.strip() for x in lang_list] 

print (lang_list)

# Y = lang_list
le = LabelEncoder()
Y = le.fit_transform(lang_list)

class_names = list(le.classes_)
print ("Class names:", class_names)
print ("# of classes:", len(class_names))

# Building convolutional network
network = input_data(shape=[None, 100], name='input')
network = tflearn.embedding(network, input_dim=1000, output_dim=128)
branch1 = conv_1d(network, 128, 3, padding='valid', activation='relu', regularizer="L2")
branch2 = conv_1d(network, 128, 4, padding='valid', activation='relu', regularizer="L2")
branch3 = conv_1d(network, 128, 5, padding='valid', activation='relu', regularizer="L2")
network = merge([branch1, branch2, branch3], mode='concat', axis=1)
network = tf.expand_dims(network, 2)
network = global_max_pool(network)
# network = dropout(network, 0.5)
fc = fully_connected(network, 11, activation='softmax')
network = regression(fc, optimizer='adam', learning_rate=0.001,
                     loss='categorical_crossentropy', name='target')

# Data preprocessing
accuracy_score = []
# Data preprocessing
for i in range(1, 10):
  X, Y = shuffle(X, Y, random_state=i)

  trainX = X[:-1000]
  testX = X[-1000:]

  trainY = Y[:-1000]
  testY = Y[-1000:]

  print(testY)
  print(testY[0])

  # Sequence padding
  trainX = pad_sequences(trainX, maxlen=100, value=0.)
  testX = pad_sequences(testX, maxlen=100, value=0.)
  # Converting labels to binary vectors
  trainY = to_categorical(trainY, nb_classes=11)
  testY = to_categorical(testY, nb_classes=11)

  # Training
  model = tflearn.DNN(network, tensorboard_verbose=3, tensorboard_dir=LOGDIR)
  model.fit(trainX, trainY, n_epoch = 25, shuffle=True, validation_set=(testX, testY), show_metric=True, batch_size=32)

  accuracy_score += model.evaluate(testX, testY)

print(accuracy_score)

pickle.dump(accuracy_score,open( "1DCNN_TOEFL_crossval.p", "wb" ))