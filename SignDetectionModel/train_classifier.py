import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load data
data_dict = pickle.load(open('./data.pickle', 'rb'))
# Convert to numpy arrays and ensure uniform shape
data = np.array([np.array(item) for item in data_dict['data']])
labels = np.array(data_dict['labels'])

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# Initialize classifier
model = RandomForestClassifier()
# Train classifier
model.fit(x_train, y_train)

# Predict
y_predict = model.predict(x_test)
# Evaluate model
score = accuracy_score(y_predict, y_test)
print('{}% of samples were classified correctly!'.format(score * 100))






