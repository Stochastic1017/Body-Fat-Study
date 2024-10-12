
import os
import sys
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split

# Ensure the current working directory is part of the path
sys.path.append(os.getcwd())

from model.prior_bmi_model_based_anomaly_detection import find_anomalies, clean_df

def calculate_rmse(y_true, y_pred):
    """
    Calculate the Root Mean Squared Error (RMSE) for a regression model.

    Parameters:
    - y_true (array-like): Actual target values.
    - y_pred (array-like): Predicted target values from the model.

    Returns:
    - rmse (float): The root mean squared error value.
    """
    return root_mean_squared_error(y_true, y_pred)

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')

# Find anomalies and clean the data
anomalies = find_anomalies(df, threshold=8)
cleaned_df = clean_df(df, anomalies)

# Separate features and response
X = cleaned_df[["AGE", "ADIPOSITY"]]
y = cleaned_df["BODYFAT"]

# Train-test split (fixed the variable order)
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.2, 
                                                    random_state=123)

# Fit a model (e.g., Linear Regression)
model = LinearRegression()
model.fit(np.log(X_train), y_train)

# Make predictions
y_pred = model.predict(np.log(X_test))

# Calculate RMSE
rmse = root_mean_squared_error(y_test, y_pred)
print(f"R-Squared: {model.score(np.log(X_test), y_test)}")
print(f"Root Mean Squared Error: {rmse}")
