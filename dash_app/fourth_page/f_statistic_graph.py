
import os
import sys
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

# Ensure the current working directory is part of the path
sys.path.append(os.getcwd())

from model.goodness_of_fit import general_goodness_of_fit
from model.prior_bmi_model_based_anomaly_detection import find_anomalies, clean_df

# Function to create the table layout
def create_f_statistic_table(X, y):
    """
    Creates the F-statistic results table layout.

    Parameters:
    - df: The dataset to perform the goodness of fit test and present in the table.

    Returns:
    - f_statistic_table_layout: A Dash layout containing the F-statistic table.
    """

    # Performing Goodness of Fit test
    f_test = general_goodness_of_fit(X, y)

    # Extract the F-test results
    F_statistic = f_test['F-statistic']
    F_critical = f_test['F-critical']
    p_value = f_test['p-value']
    p = len(X.columns) + 1
    n = X.shape[0]
    df_model = p - 1
    df_residual = n - p

    # Prepare the F-test results for the table
    f_test_data = {
        'Statistic': ['F-statistic', 'F-critical', 'p-value', 'Degrees of Freedom (Model)', 'Degrees of Freedom (Residuals)'],
        'Value': [F_statistic, F_critical, p_value, df_model, df_residual]
    }

    # Create a DataFrame for the table
    f_test_df = pd.DataFrame(f_test_data)

    # Create the table using Plotly
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Statistic', 'Value'],
                    fill_color='lightgrey',
                    align='center',
                    font=dict(size=12)),
                    
        cells=dict(values=[f_test_df['Statistic'], f_test_df['Value']],
                   fill_color='white',
                   align='center',
                   font=dict(size=12))
    )])

    # Update layout for better visuals and reduce bottom space
    fig.update_layout(
        title_x=0.5,  # Center the title
        margin=dict(l=50, r=50, t=30, b=30),  # Adjust margins (reduce bottom space)
        height=300,  # Set a fixed height to reduce extra space
        autosize=True  # Ensure the figure resizes well
    )

    # Dash layout with the table
    f_statistic_table_layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    return f_statistic_table_layout

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')
anomalies = find_anomalies(df, threshold=8)

# Cleaned the data
cleaned_df = clean_df(df, anomalies)

# Seperate features and response
X = cleaned_df[["AGE", "ADIPOSITY", "CHEST", "ABDOMEN", "THIGH"]]
y = cleaned_df["BODYFAT"]

# Main layout for your Dash app
f_test_table = html.Div([
    create_f_statistic_table(X, y)
])
