# correlation_heatmap.py
from dash import dcc, html
import pandas as pd

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')

# Define the layout for the correlation heatmap
correlation_heatmap_layout = html.Div([
    html.H3("Interactable Correlation Heatmap:", 
            style={'text-align': 'left', 'color': '#293241'}),
    dcc.Graph(id='correlation-heatmap', style={'height': '500px'}),
    html.P("Features Included in Heatmap:"),
    dcc.Dropdown(
        id='heatmap-features-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns[1:]],  # Options from column names
        placeholder='Choose Features',
        multi=True,
        value=df.columns[1:10]  # Default features (choose first few columns as default)
    )
], style={'width': '100%', 'display': 'inline-block', 'padding-bottom': '30px'})
