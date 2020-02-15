import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
%matplotlib inline
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import  mean_absolute_error, r2_score, mean_squared_error

# Data loading
data_boston = load_boston()

# Data inspection
print(data_boston.keys())
data_boston.DESCR

boston = pd.DataFrame(data_boston.data, columns=data_boston.feature_names)
boston.head()

boston['MEDV'] = data_boston.target

#Data preprocessing and exploring
#check for null values
boston.isnull().sum()

sns.set(rc={'figure.figsize':(11.7, 8.27)})
sns.distplot(boston['MEDV'], bins=60)
plt.show()

corr_matrix =  boston.corr().round(3)
#print values in the correlation squares
sns.heatmap(data=corr_matrix, annot=True)

plt.figure(figsize=(20,5))

features = ['LSTAT','RM']
target = boston['MEDV']

for idx, col in enumerate(features):
    plt.subplot(1, len(features), idx+1)
    x = boston[col]
    y = target
    plt.scatter(x, y, marker='+')
    plt.title(col)
    plt.xlabel(col)
    plt.ylabel('MEDV')

# prepare the data for training
X = pd.DataFrame(np.c_[boston['LSTAT'], boston['RM']], columns=['LSTAT','RM'])
Y = boston['MEDV']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=5)
print(X_train.shape, X_test.shape)
print(Y_train.shape, Y_test.shape)

# Train and test the model

linear_mdl = LinearRegression()
linear_mdl.fit(X_train, Y_train)

#Evaluate model
y_train_predict = linear_mdl.predict(X_train)
mse = mean_squared_error(Y_train, y_train_predict)
mae = mean_absolute_error(Y_train, y_train_predict)
r2_mse = r2_score(Y_train, y_train_predict)

print(f"Mean Square Error : {mse}")
print(f"Mean Absolute Error : {mae}")
print(f"R2-score of MSE : {r2_mse}")

y_test_predict = linear_mdl.predict(X_test)
mse_t = mean_squared_error(Y_test, y_test_predict)
mae_t = mean_absolute_error(Y_test, y_test_predict)
r2_mse_t = r2_score(Y_test, y_test_predict)

print(f"Mean Square Error Test : {mse_t}")
print(f"Mean Absolute Error Test : {mae_t}")
print(f"R2-score of MSE Test : {r2_mse_t}")