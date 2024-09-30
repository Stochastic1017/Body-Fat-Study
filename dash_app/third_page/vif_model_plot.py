from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Import the coefficient and intercept values
from model.vif_model import coefficient, intercept

# Load the dataset
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')

# Define the layout for the scatter plot with regression plane and table
vif_regression_layout = html.Div([
    html.H3("3D Scatterplot with Fitted Regression Plane:", style={'text-align': 'left', 'color': '#293241'}),
    dcc.Graph(id="3d-regression-plot"),
])

# Create a function that returns the regression plane using the imported coefficient and intercept
def get_regression_plane():
    age_range = np.linspace(df['AGE'].min(), df['AGE'].max(), 10)
    weight_range = np.linspace(df['WEIGHT'].min(), df['WEIGHT'].max(), 10)
    age_grid, weight_grid = np.meshgrid(age_range, weight_range)

    Z = intercept + coefficient[0] * age_grid + coefficient[1] * weight_grid

    return age_grid, weight_grid, Z

# Compute the OLS regression model to obtain the necessary summary statistics
X = df[['AGE', 'WEIGHT']]
X = sm.add_constant(X)
ols_model = sm.OLS(df['BODYFAT'], X).fit()

# Define the callback for rendering the 3D scatter plot with regression plane and summary table
@callback(
    Output("3d-regression-plot", "figure"),
    [Input("3d-regression-plot", "id")]
)
def update_3d_scatter_plot(_):
    # Get the regression plane
    age_grid, weight_grid, Z = get_regression_plane()

    # Create 3D scatter plot with regression plane as subplot
    fig = make_subplots(
        rows=1, cols=2,  # Two subplots: scatter plot + regression plane (left), and table (right)
        specs=[[{'type': 'scatter3d'}, {'type': 'table'}]],
        column_widths=[0.5, 0.5]  # Adjust the width of the plots to make the 3D plot smaller
    )

    # Add scatter plot of the actual data
    fig.add_trace(go.Scatter3d(
        x=df['AGE'], y=df['WEIGHT'], z=df['BODYFAT'],
        mode='markers',
        marker=dict(size=3, color='black', opacity=0.5),
        name='Data Points',
        legendgroup='scatter'
    ), row=1, col=1)

    # Add the regression plane
    fig.add_trace(go.Surface(
        x=age_grid, y=weight_grid, z=Z,
        opacity=0.7,
        name='Regression Plane',
        showscale=False,
        colorscale='Inferno',
        legendgroup='plane'
    ), row=1, col=1)

    # Create regression summary table
    regression_summary = [
        ['Coefficient (AGE)', f"{ols_model.params['AGE']:.4f}"],
        ['Coefficient (WEIGHT)', f"{ols_model.params['WEIGHT']:.4f}"],
        ['Intercept', f"{ols_model.params['const']:.4f}"],
        ['P-value (AGE)', f"{ols_model.pvalues['AGE']:.4e}"],
        ['P-value (WEIGHT)', f"{ols_model.pvalues['WEIGHT']:.4e}"],
        ['P-value (intercept)', f"{ols_model.pvalues['const']:.4e}"],
        ['R-squared', f"{ols_model.rsquared:.4f}"],
        ['Adjusted R-squared', f"{ols_model.rsquared_adj:.4f}"],
        ['F-statistic', f"{ols_model.fvalue:.2f}"],
        ['Prob (F-statistic)', f"{ols_model.f_pvalue:.4e}"],
        ['AIC', f"{ols_model.aic:.2f}"],
        ['BIC', f"{ols_model.bic:.2f}"]
    ]

    # Add the table with regression summary
    fig.add_trace(go.Table(
        header=dict(values=['<b>Metric</b>', '<b>Value</b>'],
                    fill_color='white',  # Set header background to white
                    align='left',
                    font=dict(size=12, color='black'),  # Set text color to black
                    line_color='black'),  # Set header border to black
        cells=dict(values=list(zip(*regression_summary)),
                   fill_color='white',  # Set cell background to white
                   align='left',
                   font=dict(size=12, color='black'),  # Set text color to black
                   line_color='black')),  # Set cell border to black
        row=1, col=2)

    # Set layout properties
    fig.update_layout(
        title='Body Fat vs Age and Weight with Regression Summary',
        scene=dict(
            xaxis_title='Age',
            yaxis_title='Weight',
            zaxis_title='Body Fat'
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        legend=dict(x=0, y=1)
    )

    fig.update_layout(template='plotly_white')

    return fig
