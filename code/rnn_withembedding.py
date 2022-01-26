# -*- coding: utf-8 -*-
"""
Simple example using LSTM recurrent neural network to classify IMDB
sentiment dataset.
References:
    - Long Short Term Memory, Sepp Hochreiter & Jurgen Schmidhuber, Neural
    Computation 9(8): 1735-1780, 1997.
    - Andrew L. Maas, Raymond E. Daly, Peter T. Pham, Dan Huang, Andrew Y. Ng,
    and Christopher Potts. (2011). Learning Word Vectors for Sentiment
    Analysis. The 49th Annual Meeting of the Association for Computational
    Linguistics (ACL 2011).
Links:
    - http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf
    - http://ai.stanford.edu/~amaas/data/sentiment/
"""
from __future__ import division, print_function, absolute_import

import tflearn
from tflearn.data_utils import to_categorical, pad_sequences
from tflearn.datasets import imdb
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle

from keras.preprocessing.text import Tokenizer, text_to_word_sequence
from tflearn.layers.recurrent import bidirectional_rnn, BasicLSTMCell

import tflearn
from tflearn.data_utils import to_categorical, pad_sequences
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.embedding_ops import embedding
from tflearn.layers.recurrent import bidirectional_rnn, BasicLSTMCell
from tflearn.layers.estimator import regression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import numpy as np
import matplotlib.pyplot as plt

file = open('toefl_upos.txt', 'r')
data = []
labels = []
for line in file:
    toks = line.strip().split()
    sent = ' '.join(w for w in toks[ : -1])
    data.append(sent)
    labels.append(toks[-1])

POS = open('/Users/sven/Projects/2016_9_cp_essays/NLI/CAES/Data/POS_tags.txt', 'r')
POS_list = POS.readlines()
POS_list = [x.strip() for x in POS_list]

tknzr = Tokenizer(lower=False, split=" ")
tknzr.fit_on_texts(POS_list)
#vocabulary:
print(tknzr.word_index)
print(POS_list)
print ("Got POS tags")
trainX = tknzr.texts_to_sequences(POS_list)
print(trainX[1])

lang = open('/Users/sven/Projects/2016_9_cp_essays/NLI/CAES/Data/labels.txt','r')
lang_list = lang.readlines()
lang_list = [x.strip() for x in lang_list]
print ("Got labels")

trainY = lang_list
le = LabelEncoder()
trainY = le.fit_transform(lang_list)
print (trainY[0])
print (lang_list[0])

class_names = list(le.classes_)
print ("Class names:")
print (class_names)


# Data preprocessing

X, Y = shuffle(trainX, trainY, random_state=1)

trainX = X[:-1000]
testX = X[-1000:]

trainY = Y[:-1000]
testY = Y[-1000:]

# Sequence padding
trainX = pad_sequences(trainX, maxlen=100, value=0.)
testX = pad_sequences(testX, maxlen=100, value=0.)

# Converting labels to binary vectors
trainY = to_categorical(trainY, nb_classes=6)
testY = to_categorical(testY, nb_classes=6)

# Network building
net = tflearn.input_data([None, 100])
net = tflearn.embedding(net, input_dim=1000, output_dim=128)
net = tflearn.lstm(net, 128, dropout=0.8)
net = tflearn.fully_connected(net, 6, activation='softmax')
net = tflearn.regression(net, optimizer='adam', learning_rate=0.001,
                         loss='categorical_crossentropy')

# Training
model = tflearn.DNN(net, tensorboard_verbose=0)
model.fit(trainX, trainY, validation_set=(testX, testY), show_metric=True,
          batch_size=32)

predictY = model.predict(testX)

cnf_matrix = confusion_matrix(np.argmax(testY, axis=1), np.argmax(predictY, axis= 1))
print(cnf_matrix)

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

# Compute confusion matrix
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names,
                      title='Confusion matrix, without reduction')

plt.show()
