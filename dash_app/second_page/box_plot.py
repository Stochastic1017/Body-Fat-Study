
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')

# Define the layout for the box plot with jittered data
box_plot_layout = html.Div([
    html.H3("Interactable Box Plots with Jittered Data:", 
            style={'text-align': 'left', 'color': '#293241'}),
    html.Div([
        html.P("Select Features for Box Plots:"),
        dcc.Dropdown(
            id='boxplot-features-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns[1:]],  # Options from column names
            placeholder='Choose Features',
            multi=True,
            value=df.columns[-6:-1]  # Default features
        ),
        dcc.Graph(id='boxplot-features', style={'height': '500px'}),
    ], style={'width': '100%', 'display': 'inline-block', 'padding-bottom': '30px'})
])

# Callback for updating the box plot with jittered data (existing)
@callback(
    Output('boxplot-features', 'figure'),
    Input('boxplot-features-dropdown', 'value')
)
def update_boxplot(features):
    if not features:
        return go.Figure()

    fig = go.Figure()
    
    # Add jittered box plots for selected features
    for feature in features:
        fig.add_trace(go.Box(y=df[feature], name=feature, 
                             boxpoints='all', jitter=0.3, pointpos=-1.8))

    fig.update_layout(
        title="Box Plot with Jittered Data",
        showlegend=False,
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig