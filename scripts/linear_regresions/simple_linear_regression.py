import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/ElStevenn/PropertyPricePredictor/main/datasets/encoded_labels.csv"
cls = lambda: os.system('cls'); cls()
df = pd.read_csv(url, index_col=False)
np.set_printoptions(suppress=True, precision=10, formatter={'float': '{: 0.2f}'.format}, threshold=np.inf)


Regression = LinearRegression()

# Select witch data we want so select as X and as Y
Y = np.array(df['price_per_month']).reshape(-1,1)
X = np.array(df[['m2','bedrooms','bathrooms','encoded_neighborhood']])

# Split data in train and test (80%/20%)
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, train_size=0.2, random_state=43)


# X_test_price_month = np.array(df[''])

Regression.fit(X_train, Y_train)

predicts = Regression.predict(X_test)
# print(predicts)
result = np.hstack((Y_test, predicts)).reshape(Y_test.shape[0], 2, order="F")


with open("predictions_comparation.txt", "w") as f:
    for row in result:
        f.write(" -----> ".join(map(str, row)) + "\n - ")

# Evaluate the model
mse = mean_squared_error(Y_test, predicts)
print('Mean Squared Error:', mse)

# Feature Importance
print('Feature Coefficients:', Regression.coef_)