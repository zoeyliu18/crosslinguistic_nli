from __future__ import division, print_function, absolute_import

import numpy as np
import os, sys, string, itertools, pickle, datetime, statistics
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from collections import Counter
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
from sklearn.metrics import classification_report
import sklearn.metrics as metrics
from functools import reduce
from sklearn import svm
from sklearn.dummy import DummyClassifier
### e.g. python3 code/6.ngrams_svm.py TOEFL POS no

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

def save(cucumber, fileName):
    f = open(fileName, 'wb')   # Pickle file is newly created where foo1.py is
    pickle.dump(cucumber, f)          # dump data to f
    f.close()
    return

def log(test_true, test_pred, name):
    #results = {}
    contains = False
    #reduce
    #contains = reduce(lambda x,y: x.endswith("resultsdict.pkl") and y.endswith("resultsdict.pkl"), [File for File in os.listdir(".")])
    for File in os.listdir('results/'):
        if File.endswith(sys.argv[1] + "_svm_" + sys.argv[2] + ".pkl"):
            contains = True
            break
        else:
            contains = False
    if contains:
        f = open('results/' + sys.argv[1] + "_svm_" + sys.argv[2] + ".pkl", 'rb')   # Pickle file is newly created where foo1.py is
        results = pickle.load(f)          # dump data to f
        f.close()
    else: results = {}

    print(results)
    results['Last Update'] = str(datetime.datetime.now())
    save(results, 'results/' + sys.argv[1] + "_svm_" + sys.argv[2] + ".pkl")
    # accuracy = network.evaluate(testX, testY)[0] * 100
    #
    # y_pre = [network.predict([i]) for idx,i in enumerate(testX)]
    # y_pre = np.squeeze(y_pre, 1)
    # #print(y_pre)
    #
    # test_true = np.argmax(testY,1)
    # test_pred = np.argmax(y_pre,1)
    # #print(test_pred.tolist())
    # #print(test_true.tolist())

    accuracy = 100 * metrics.accuracy_score(test_true, test_pred)#, average="weighted")
    precision = 100 * metrics.precision_score(test_true, test_pred, average="weighted")
    recall = 100 * metrics.recall_score(test_true, test_pred, average="weighted")
    f1 = 100 * metrics.f1_score(test_true, test_pred, average="weighted")
    print ("Accuracy: {}%".format(accuracy))
    print ("Precision: {}%".format(precision))
    print ("Recall: {}%".format(recall))
    print ("F1_score: {}%".format(f1))
    print (name)
    results[name] = {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1}
    save(results, 'results/' + sys.argv[1] + "_svm_" + sys.argv[2] + ".pkl")

LOGDIR = "results/tflearn_logs/"
NAME = sys.argv[1] + '_SVM_POS+UDP'

# get n-gram vectors of POS annotated file as features

POS_list = []
deprel_list = []
lang_list = []

if '_' not in sys.argv[1]:
    with open('results/' + sys.argv[1] + '_syntax.txt') as f:
        for line in f:
            toks = line.strip().split('\t')
            POS_list.append(toks[0])
            deprel_list.append(toks[1])
            lang_list.append(toks[2])

else:
    corpus_list = sys.argv[1].split('_')
    if sys.argv[3] == 'no': ### restricting to only common native languages? 
        for corpus in corpus_list:
            with open('results/' + corpus + '_syntax.txt') as f:
                for line in f:
                    toks = line.strip().split('\t')
                    POS_list.append(toks[0])
                    deprel_list.append(toks[1])
                    lang_list.append(toks[2])
    else:
        temp_lang_list = []
        common_lang_list = []
        for corpus in corpus_list:
            with open('results/' + corpus + '_syntax.txt') as f:
                corpus_lang_list = []
                for line in f:
                    toks = line.strip().split('\t')
                    l = toks[2]
                    if l not in corpus_lang_list:
                        corpus_lang_list.append(toks[2])
                temp_lang_list += corpus_lang_list

        for l in set(temp_lang_list):
            if temp_lang_list.count(l) > 1:
                common_lang_list.append(l)
        print(common_lang_list)

        for corpus in corpus_list:
            with open('results/' + corpus + '_syntax.txt') as f:
                for line in f:
                    toks = line.strip().split('\t')
                    l = toks[2]
                    if l in common_lang_list:
                        POS_list.append(toks[0])
                        deprel_list.append(toks[1])
                        lang_list.append(l)


print ("Got data")

print("testing")
print(len(POS_list))
print(len(deprel_list))


POSDep = [POS_list[i] + deprel_list[i] for i in range(len(POS_list))]

select_data = ''
if sys.argv[2] == 'POS':
    select_data = POS_list
if sys.argv[2] == 'Dep':
    select_data = deprel_list
if sys.argv[2] == 'b':
    select_data = POSDep

vectorizer = TfidfVectorizer(ngram_range=(1, 3), min_df=1) 
X = vectorizer.fit_transform(select_data).toarray()
print ("Shape of vector array:")
print (X.shape[1])

le = LabelEncoder()
y = le.fit_transform(lang_list)


class_names = list(le.classes_)
print ("Class names:")
print (class_names)



X, y = shuffle(X, y, random_state=8)

### Baselines ###
most_frequent_clf = DummyClassifier(strategy="most_frequent", random_state = 8)
stratified_clf = DummyClassifier(strategy="stratified", random_state = 8)
uniform_clf = DummyClassifier(strategy="uniform", random_state = 8)

### SVM ###
#clf = svm.SVC(C=1, kernel='linear', decision_function_shape='ovr')

### Random Forest; not so good ###
#from sklearn.ensemble import RandomForestClassifier
#clf = RandomForestClassifier(max_depth=2, random_state=0) 

### Extra Trees; not AS good ###
#from sklearn.ensemble import ExtraTreesClassifier
#clf = ExtraTreesClassifier(n_estimators=100, random_state=0)

### Decision Tress; not so good ###
#from sklearn.tree import DecisionTreeClassifier
#clf = DecisionTreeClassifier(random_state=0)

### Ridge classifier; better ###

from sklearn.linear_model import RidgeClassifierCV
clf = RidgeClassifierCV(alphas=[1e-3, 1e-2, 1e-1, 1])

### Output file ###

#out_file = open('results/' + sys.argv[1] + '_svm_' + sys.argv[2] + '_results.txt', 'w')


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 8)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)


cnf_matrix = confusion_matrix(y_test, y_pred)

target_names = list(set(le.inverse_transform(y_test)))

print(classification_report(y_test, y_pred, target_names=target_names))


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

    # print(cm)

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

# print (cnf_matrix)
# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names,
                      title='Confusion Matrix, without reduction')


# Plot normalized confusion matrix
# plt.figure()
# plot_confusion_matrix(cnf_ae_matrix, classes=class_names,
#                       title='AEd confusion matrix')

#plt.show()
plt.savefig('results/' + sys.argv[1] + '_svm_confusion_' + sys.argv[2] + '.png')

'''
most_frequent_precision = cross_val_score(most_frequent_clf, X, y, cv=5, scoring = 'precision_weighted')
most_frequent_recall = cross_val_score(most_frequent_clf, X, y, cv=5, scoring = 'recall_weighted')
most_frequent_f1 = cross_val_score(most_frequent_clf, X, y, cv=5, scoring = 'f1_weighted')
out_file.write('Majority' + '\n')
out_file.write('Precision: ' + str(statistics.mean(most_frequent_precision)) + '\n')
out_file.write('Recall: ' + str(statistics.mean(most_frequent_recall)) + '\n')
out_file.write('F1: ' + str(statistics.mean(most_frequent_f1)) + '\n')
out_file.write('\n')

uniform_precision = cross_val_score(uniform_clf, X, y, cv=5, scoring = 'precision_weighted')
uniform_recall = cross_val_score(uniform_clf, X, y, cv=5, scoring = 'recall_weighted')
uniform_f1 = cross_val_score(uniform_clf, X, y, cv=5, scoring = 'f1_weighted')
out_file.write('Random' + '\n')
out_file.write('Precision: ' + str(statistics.mean(uniform_precision)) + '\n')
out_file.write('Recall: ' + str(statistics.mean(uniform_recall)) + '\n')
out_file.write('F1: ' + str(statistics.mean(uniform_f1)) + '\n')
out_file.write('\n')

stratified_precision = cross_val_score(stratified_clf, X, y, cv=5, scoring = 'precision_weighted')
stratified_recall = cross_val_score(stratified_clf, X, y, cv=5, scoring = 'recall_weighted')
stratified_f1 = cross_val_score(stratified_clf, X, y, cv=5, scoring = 'f1_weighted')
out_file.write('Stratified' + '\n')
out_file.write('Precision: ' + str(statistics.mean(stratified_precision)) + '\n')
out_file.write('Recall: ' + str(statistics.mean(stratified_recall)) + '\n')
out_file.write('F1: ' + str(statistics.mean(stratified_f1)) + '\n')
out_file.write('\n')

precision = cross_val_score(clf, X, y, cv=5, scoring = 'precision_weighted')
recall = cross_val_score(clf, X, y, cv=5, scoring = 'recall_weighted')
f1 = cross_val_score(clf, X, y, cv=5, scoring = 'f1_weighted')
out_file.write('SVM' + '\n')
out_file.write('Precision: ' + str(statistics.mean(precision)) + '\n')
out_file.write('Recall: ' + str(statistics.mean(recall)) + '\n')
out_file.write('F1: ' + str(statistics.mean(f1)) + '\n')
out_file.write('\n')

'''
