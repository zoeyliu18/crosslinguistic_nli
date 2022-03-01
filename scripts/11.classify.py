import pandas as pd 
import numpy as np 
import statistics
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
from sklearn.metrics import f1_score

from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.inspection import permutation_importance

from sklearn.feature_extraction.text import CountVectorizer

def plot_coefficients(classifier, feature_names, top_features=20):
	coef = classifier.coef_.ravel()
	top_positive_coefficients = np.argsort(coef)[-top_features:]
	top_negative_coefficients = np.argsort(coef)[:top_features]
	top_coefficients = np.hstack([top_negative_coefficients, top_positive_coefficients])
	# create plot
	plt.figure(figsize=(15, 5))
	colors = ['red' if c < 0 else 'blue' for c in coef[top_coefficients]]
	plt.bar(np.arange(2 * top_features), coef[top_coefficients], color=colors)
	feature_names = np.array(feature_names)
	plt.xticks(np.arange(1, 1 + 2 * top_features), feature_names[top_coefficients], rotation=60, ha='right')
	plt.show()

### Combining data together ###

TOEFL_data = pd.read_csv('TOEFL_features.txt', sep = '\t')
TOEFL_data = pd.DataFrame(TOEFL_data)
TOEFL_data = TOEFL_data.loc[:, (TOEFL_data != 0).any(axis=0)]
TOEFL_data = TOEFL_data.dropna(axis = 'columns')
TOEFL_data = shuffle(TOEFL_data)
TOEFL_lang = list(set(TOEFL_data['Lang'].tolist()))

PELIC_data = pd.read_csv('PELIC_features.txt', sep = '\t')
PELIC_data = pd.DataFrame(PELIC_data)
PELIC_data = PELIC_data.loc[:, (PELIC_data != 0).any(axis=0)]
PELIC_data = PELIC_data.dropna(axis = 'columns')
PELIC_data = shuffle(PELIC_data)
PELIC_lang = list(set(PELIC_data['Lang'].tolist()))

WriCLE_formal_data = pd.read_csv('WriCLE-formal_features.txt', sep = '\t')
WriCLE_formal_data = pd.DataFrame(WriCLE_formal_data)
WriCLE_formal_data = WriCLE_formal_data.loc[:, (WriCLE_formal_data != 0).any(axis=0)]
WriCLE_formal_data = WriCLE_formal_data.dropna(axis = 'columns')
WriCLE_formal_data = shuffle(WriCLE_formal_data)
WriCLE_formal_lang = list(set(WriCLE_formal_data['Lang'].tolist()))

WriCLE_informal_data = pd.read_csv('WriCLE-informal_features.txt', sep = '\t')
WriCLE_informal_data = pd.DataFrame(WriCLE_formal_data)
WriCLE_informal_data = WriCLE_informal_data.loc[:, (WriCLE_informal_data != 0).any(axis=0)]
WriCLE_informal_data = WriCLE_informal_data.dropna(axis = 'columns')
WriCLE_informal_data = shuffle(WriCLE_informal_data)
WriCLE_informal_lang = list(set(WriCLE_informal_data['Lang'].tolist()))

CAES_data = pd.read_csv('CAES_features.txt', sep = '\t')
CAES_data = pd.DataFrame(CAES_data)
CAES_data = CAES_data.loc[:, (CAES_data != 0).any(axis=0)]
CAES_data = CAES_data.dropna(axis = 'columns')
CAES_data = shuffle(CAES_data)
CAES_lang = list(set(CAES_data['Lang'].tolist()))

CEDEL_data = pd.read_csv('CEDEL_features.txt', sep = '\t')
CEDEL_data = pd.DataFrame(CEDEL_data)
CEDEL_data = CEDEL_data.loc[:, (CEDEL_data != 0).any(axis=0)]
CEDEL_data = CEDEL_data.dropna(axis = 'columns')
CEDEL_data = shuffle(CEDEL_data)
CEDEL_lang = list(set(CEDEL_data['Lang'].tolist()))

COWS_data = pd.read_csv('COWS_features.txt', sep = '\t')
COWS_data = pd.DataFrame(COWS_data)
COWS_data = COWS_data.loc[:, (COWS_data != 0).any(axis=0)]
COWS_data = COWS_data.dropna(axis = 'columns')
COWS_data = shuffle(COWS_data)
COWS_lang = list(set(COWS_data['Lang'].tolist()))

temp_lang_list = TOEFL_lang + PELIC_lang + WriCLE_formal_lang + WriCLE_informal_lang + CAES_lang + CEDEL_lang + COWS_lang
lang_list = []
for l in set(temp_lang_list):
	if temp_lang_list.count(l) > 1:
		lang_list.append(l)

print(len(lang_list))
print(lang_list)

all_data = pd.concat([TOEFL_data, PELIC_data, WriCLE_formal_data, WriCLE_informal_data, CAES_data, CEDEL_data, COWS_data], axis = 0)

all_data = all_data.loc[all_data['Lang'].isin(lang_list)]
#all_data = all_data.loc[:, (all_data != 0).any(axis=0)]
all_data = all_data.dropna(axis = 'columns')
all_features = list(all_data.columns)

exclude = []
for f in all_features:
	if 'lemma' in f:
		exclude.append(f)

exclude = exclude + ['num_word_type', 'ttr_word', 'ave_word_len', 'lexical_density', 'function_word_type']

all_data = all_data.drop(exclude, axis = 1)
all_features = list(all_data.columns)

X = all_data.drop(['Lang'], axis = 1)
features = X.columns
X = np.array(X)

languages = all_data['Lang'].tolist()
i = 0
language_ids = {}
for tok in set(languages):
	language_ids[tok] = i 
	i += 1

y = []
for tok in languages:
	y.append(language_ids[tok])

print(set(languages))
print(language_ids)

scaler = preprocessing.MinMaxScaler().fit(X)
X_transformed = scaler.transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2,random_state = 8)

from sklearn.linear_model import RidgeClassifierCV
clf = RidgeClassifierCV(alphas=[1e-3, 1e-2, 1e-1, 1])

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

accuracy = 0
for i in range(len(y_pred)):
  gold = y_test[i]
  pred = y_pred[i]
  if gold == pred:
    accuracy += 1

print(accuracy / len(y_test))

#f1_score(y_test, y_pred, average='weighted')

precision = cross_val_score(clf, X, y, cv=5, scoring = 'precision_weighted')
recall = cross_val_score(clf, X, y, cv=5, scoring = 'recall_weighted')
f1 = cross_val_score(clf, X, y, cv=5, scoring = 'f1_weighted')

print(statistics.mean(precision))
print(statistics.mean(recall))
print(statistics.mean(f1))

### Calculating feature importance ###
r = permutation_importance(clf, X_test, y_test, n_repeats = 30, random_state = 8, scoring = ['f1_weighted'])

importances_mean = r['f1_weighted']['importances_mean']
importances_std = r['f1_weighted']['importances_std']

for i in importances_mean.argsort()[::-1]:
	if importances_mean[i] - 2 * importances_std[i] > 0:
		print(all_features[i], importances_mean[i], importances_std[i])

cv = CountVectorizer()
cv.fit(all_data)
print(len(cv.vocabulary_))
print(cv.get_feature_names())

top_features = 10
coef =  clf.coef_.ravel()
top_positive_coefficients = np.argsort(coef)[-top_features:]
top_negative_coefficients = np.argsort(coef)[:top_features]

top_coefficients = np.hstack([top_negative_coefficients, top_positive_coefficients])
feature_names = np.array(cv.get_feature_names())

print(feature_names)
