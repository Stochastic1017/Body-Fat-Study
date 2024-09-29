# scatter_plot.py
from dash import dcc, html
import pandas as pd

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')

# Define the layout for the scatter plot with histograms
scatter_plot_layout = html.Div([
    html.H3("Interactable Density Histogram and Scatterplot:", 
            style={'text-align': 'left', 'color': '#293241'}),
    html.Div([
        html.Div([
            html.P("X-axis feature:"),
            dcc.Dropdown(
                id='x-axis-feature',
                options=[{'label': col, 'value': col} for col in df.columns[1:]],
                value=df.columns[3]
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.P("Y-axis feature:"),
            dcc.Dropdown(
                id='y-axis-feature',
                options=[{'label': col, 'value': col} for col in df.columns[1:]],
                value=df.columns[2]
            ),
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='scatter-hist-plot', style={'height': '600px'}),
], style={'width': '100%', 'display': 'inline-block', 'padding-bottom': '30px'})
