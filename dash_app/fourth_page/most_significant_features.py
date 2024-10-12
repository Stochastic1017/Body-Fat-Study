
import os
import sys
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

# Ensure the current working directory is part of the path
sys.path.append(os.getcwd())

from model.goodness_of_fit import finding_most_significant_features
from model.prior_bmi_model_based_anomaly_detection import find_anomalies, clean_df

# Function to create the table layout
import os
import sys
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

# Ensure the current working directory is part of the path
sys.path.append(os.getcwd())

from model.goodness_of_fit import finding_most_significant_features

# Function to create the table layout
def create_best_predictors_table(X, y, alpha=0.05):
    """
    Creates a table layout showing the most significant features and their p-values,
    adjusted by the Holm-Bonferroni method.

    Parameters:
    - X: DataFrame of predictor variables.
    - y: Series or array of the target variable.
    - alpha: Significance level for the Holm-Bonferroni correction (default = 0.05).

    Returns:
    - best_predictors_table_layout: A Dash layout containing the best predictors table.
    """

    # Finding the most significant features and p-values using Holm-Bonferroni correction
    significant_features, p_values_df = finding_most_significant_features(X, y, alpha)

    # Sample data for predictors and p-values
    table_data = {
        'Predictor': p_values_df['Feature'],
        'p-value': p_values_df['p-value']
    }

    # Set the alpha level
    alpha = 0.05

    # Create a DataFrame for the table
    table_df = pd.DataFrame(table_data)

    # Adjust alpha for Holm-Bonferroni method
    m = len(table_df)  # Number of hypotheses (predictors)
    adjusted_alphas = [alpha / (m - i) for i in range(m)]

    # Add the adjusted alpha column to the DataFrame
    table_df['Adjusted Alpha'] = adjusted_alphas

    # Check if p-value is less than adjusted alpha
    table_df['Significant'] = table_df['p-value'] < table_df['Adjusted Alpha']

    # Create colors for the cells: green for significant, red for non-significant
    cell_colors = [['lightgreen' if sig else 'lightcoral' for sig in table_df['Significant']]]

    # Create the table using Plotly
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Predictor', 'p-value', 'Adjusted Alpha'],
                    fill_color='lightgrey',
                    align='center',
                    font=dict(size=12)),
                    
        cells=dict(values=[table_df['Predictor'], table_df['p-value'], table_df['Adjusted Alpha']],
                fill_color=[['white'] * m, ['white'] * m, cell_colors[0]],
                align='center',
                font=dict(size=12))
    )])

    # Update layout for better visuals
    fig.update_layout(
        title="Holm-Bonferroni Adjusted Alpha and p-values",
        title_x=0.5,  # Center the title
        margin=dict(l=50, r=50, t=50, b=30),  # Adjust margins
        height=400,  # Set a fixed height for the table
        autosize=True
    )
    # Dash layout with the table
    best_predictors_table_layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    return best_predictors_table_layout

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')
anomalies = find_anomalies(df, threshold=8)

# Cleaned the data
cleaned_df = clean_df(df, anomalies)

# Seperate features and response
X = cleaned_df[["AGE", "ADIPOSITY", "CHEST", "ABDOMEN", "THIGH"]]
y = cleaned_df["BODYFAT"]

# Main layout for your Dash app
best_predictors_table = html.Div([
    create_best_predictors_table(X, y)
])