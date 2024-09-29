# box_plot.py
from dash import dcc, html
import pandas as pd

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')

# Define the layout for the box plot with jittered data
box_plot_layout = html.Div([
    html.H3("Interactable Box Plots with Jittered Data:", 
            style={'text-align': 'left', 'color': '#293241'}),
    html.Div([
        dcc.Graph(id='boxplot-features', style={'height': '500px'}),
        html.P("Select Features for Box Plots:"),
        dcc.Dropdown(
            id='boxplot-features-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns[1:]],  # Options from column names
            placeholder='Choose Features',
            multi=True,
            value=df.columns[1:5]  # Default features
        ),
    ], style={'width': '100%', 'display': 'inline-block', 'padding-bottom': '30px'})
])
