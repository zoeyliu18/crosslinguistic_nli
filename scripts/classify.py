import pandas as pd 
import numpy as np 
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv('features.txt', sep = '\t')
data = pd.DataFrame(data)
data = shuffle(data)
X = data.dropna(axis = 'columns')
X = X.drop(['Lang'],axis = 1)
X = np.array(X)

languages = data['Lang'].tolist()
i = 0
language_ids = {}
for tok in set(languages):
	language_ids[tok] = i 
	i += 1

Y = []
for tok in languages:
	Y.append(language_ids[tok])

#Create a svm Classifier
clf = svm.SVC(kernel='linear') # Linear Kernel

#Decision tree

clf = DecisionTreeClassifier(random_state=0)

#scaler = preprocessing.StandardScaler().fit(X)
scaler = preprocessing.MinMaxScaler().fit(X)
X_transformed = scaler.transform(X)

### Cross-validation ###

scores = cross_val_score(clf, X, Y, cv=5)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2,random_state = 8)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)


### random splits ###

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2,random_state = 8)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

for i in range(1, 11):
	# Split dataset into training set and test set
	X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2,random_state = i)
	
	#Train the model using the training sets
	clf.fit(X_train, y_train)

	#Predict the response for test dataset
	y_pred = clf.predict(X_test)

