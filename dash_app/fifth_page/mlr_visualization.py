
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from dash import dcc, html
import plotly.graph_objs as go
from sklearn.model_selection import train_test_split

# Ensure the current working directory is part of the path
sys.path.append(os.getcwd())

from model.multiple_regression import run_regression_and_summary, generate_diagnostic_plots, two_dim_regression

# Load the data
cleaned_df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/cleaned_bodyfat_11.csv')
cleaned_df = cleaned_df[cleaned_df["IDNO"] != 39] # removing observation outside cooks distance

# Seperate features and response
X = cleaned_df[["AGE", "ABDOMEN"]]
y = cleaned_df["BODYFAT"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.2, 
                                                    random_state=123)

# Fitting regression model
results = run_regression_and_summary(X_train, y_train, X_test, y_test)

scatter, plane, plot_layout, table_data = two_dim_regression(df=cleaned_df, results=results, feature_1='AGE', feature_2='ABDOMEN')

# Create the Dash layout
regression_layout = html.Div([
    html.Div([
        dcc.Graph(
            id='3d-scatter-plot',
            figure={
                'data': [scatter, plane],
                'layout': plot_layout
            },
            style={'height': '400px'}
        )
    ], style={'width': '55%', 'display': 'inline-block', 'vertical-align': 'top'}),  # Adjusted width for balance
    html.Div([
        dcc.Graph(
            id='results-table',
            figure={
                'data': [go.Table(
                    header=dict(values=['Metric', 'Value'],
                                fill_color='#293241',  # Set a light background for readability
                                font=dict(color='white', size=12),  # White text
                                align='center'),  # Center align headers,
                    cells=dict(values=[list(row) for row in zip(*table_data[1:])],  # No duplicate header in table cells
                                fill_color='white',
                                align='center')
                )],
                'layout': go.Layout(
                    margin=dict(l=0, r=0, t=0, b=0)
                )
            },
            style={'height': '400px'}  # Adjusted height to match the 3D plot
        )
    ], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'})  # Adjusted width for balance
])

# Diagnostic plots figure
diagnostic_fig = generate_diagnostic_plots(results, cleaned_df)

diagnostic_layout = html.Div([
    dcc.Graph(
        id='diagnostic-plots',
        figure=diagnostic_fig,  # The diagnostic plot figure generated by the function
        style={
            'height': '800px',  # Reduced height
            'width': '80%',     # Adjust width
            'margin': '20px auto'  # Add margin to prevent overlap
        }
    )
], style={
    'display': 'flex',
    'justify-content': 'center',
    'align-items': 'center',
    'padding': '20px',  # Add padding to avoid overlap with other content
})
