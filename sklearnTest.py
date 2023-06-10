from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn import datasets
from sklearn.model_selection import train_test_split
import numpy as np
import csv
from sklearn.metrics import mean_squared_error
from sklearn.utils import Bunch
import matplotlib.pyplot as plt
import pickle
import time
from TrainingCore import TrainingCore


dat = TrainingCore.load_dataset('data_11.13.17.765.cvs')  


#
# Load California housing data set
#
X = dat.data
y = dat.target
#
# Create training/ test data split
#
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
#
# Instantiate MLPRegressor
#

nn = TrainingCore.train(X_train, y_train,save = True)
#nn = TrainingCore.load_model_latest()

pred = nn.predict(X_test)
#
# Calculate accuracy and error metrics
#
test_set_rsquared = nn.score(X_test, y_test)

test_set_rmse = np.sqrt(mean_squared_error(y_test, pred))
#
# Print R_squared and RMSE value
#
print('R_squared value: ', test_set_rsquared)
print('RMSE: ', test_set_rmse)

plt.plot(np.arange(len(nn.loss_curve_)),nn.loss_curve_)


plt.show()