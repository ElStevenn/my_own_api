import os
import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

url = "https://raw.githubusercontent.com/ElStevenn/PropertyPricePredictor/main/datasets/encoded_labels.csv"
cls = lambda: os.system('cls'); cls()
df = pd.read_csv(url, index_col=False)
np.set_printoptions(suppress=True, precision=1, formatter={'float': '{: 0.2f}'.format}, threshold=np.inf)


# Select witch data we want so select as X and as Y
Y = np.array(df['price_per_month']).reshape(-1,1)
X = np.array(df[['m2','bedrooms','bathrooms','encoded_neighborhood']])

# Split data into Train and Test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.2, random_state=43)

# Apply Lasso reggrestion
lasso_reg = Lasso(alpha=0.1)
lasso_reg.fit(X_train, Y_train)

# Predict house prices from X_test
y_pred = lasso_reg.predict(X_test).reshape(-1,1)

result = np.hstack((Y_test, y_pred)).reshape(Y_test.shape[0], 2, order="F")

# with open("Lasso_trained.txt", "w") as f:
#     for row in result:
#         f.write(" ---> ".join(map(str, row)) + "\n - ")

# Evaluating the model
mse = mean_squared_error(Y_test, y_pred)
print('Mean Squared Error:', mse)

# Feature Importance
print('Feature Coefficients:', lasso_reg.coef_)