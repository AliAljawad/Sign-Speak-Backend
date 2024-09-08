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

