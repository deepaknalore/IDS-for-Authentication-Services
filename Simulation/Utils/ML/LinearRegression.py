import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

X = []
Y = []
with open("train.txt", "r") as fd:
    lines = fd.readlines()
    for line in lines:
        temp = line.split(",")
        X.append(temp[:-1])
        Y.append(temp[-1].rstrip())


X_train = np.array(X[:-5000],np.float64)
X_test = np.array(X[-5000:],np.float64)
Y_train = np.array(Y[:-5000],np.float64)
Y_test = np.array(Y[-5000:],np.float64)

regr = linear_model.LinearRegression()

regr.fit(X_train, Y_train)
Y_pred = regr.predict(X_test)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print('Mean squared error: %.2f'
      % mean_squared_error(Y_test, Y_pred))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination: %.2f'
      % r2_score(Y_test, Y_pred))
