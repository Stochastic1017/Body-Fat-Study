from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Import the coefficient and intercept values
from model.vif_model import coefficient, intercept

# Load the dataset
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')

# Define the layout for the scatter plot with regression plane
vif_regression_layout = html.Div([
    html.H3("3D Scatterplot with Fitted Regression Plane:", style={'text-align': 'left', 'color': '#293241'}),
    dcc.Graph(id="3d-regression-plot"),  # This will render the 3D scatter plot
])

# Create a function that returns the regression plane using the imported coefficient and intercept
def get_regression_plane():
    # Create grid for AGE and WEIGHT
    age_range = np.linspace(df['AGE'].min(), df['AGE'].max(), 10)
    weight_range = np.linspace(df['WEIGHT'].min(), df['WEIGHT'].max(), 10)
    age_grid, weight_grid = np.meshgrid(age_range, weight_range)

    # Calculate BODYFAT values on the grid using the imported coefficients
    Z = intercept + coefficient[0] * age_grid + coefficient[1] * weight_grid

    return age_grid, weight_grid, Z

# Define the callback for rendering the 3D scatter plot with regression plane
@callback(
    Output("3d-regression-plot", "figure"),
    [Input("3d-regression-plot", "id")]
)
def update_3d_scatter_plot(_):
    # Get the regression plane
    age_grid, weight_grid, Z = get_regression_plane()

    # Create 3D scatter plot
    fig = go.Figure()

    # Add scatter plot of the actual data
    fig.add_trace(go.Scatter3d(
        x=df['AGE'], y=df['WEIGHT'], z=df['BODYFAT'],
        mode='markers',
        marker=dict(size=5, color='blue', opacity=0.6),
        name='Data Points'
    ))

    # Add the regression plane
    fig.add_trace(go.Surface(
        x=age_grid, y=weight_grid, z=Z,
        colorscale='Viridis',
        opacity=0.7,
        name='Regression Plane'
    ))

    # Set layout properties
    fig.update_layout(
        title='Body Fat vs Age and Weight',
        scene=dict(
            xaxis_title='Age',
            yaxis_title='Weight',
            zaxis_title='Body Fat'
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    return fig
