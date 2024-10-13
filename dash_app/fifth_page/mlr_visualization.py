
import os
import sys
import pandas as pd
import numpy as np
from dash import dcc, html
import plotly.graph_objs as go
from sklearn.model_selection import train_test_split

# Ensure the current working directory is part of the path
sys.path.append(os.getcwd())

from model.multiple_regression import run_regression_and_summary, generate_diagnostic_plots

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

# Create custom hover text
hover_text = [
    f"IDNO: {int(row['IDNO'])}<br>AGE: {row['AGE']}<br>ABDOMEN: {row['ABDOMEN']}<br>BODYFAT: {row['BODYFAT']}"
    for index, row in cleaned_df.iterrows()
]

# 3D scatter plot with custom hovertext
scatter = go.Scatter3d(
    x=cleaned_df['AGE'],
    y=cleaned_df['ABDOMEN'],
    z=cleaned_df['BODYFAT'],
    mode='markers',
    marker=dict(size=3.5, color=cleaned_df['BODYFAT'], colorscale='Inferno', opacity=0.8),
    text=hover_text,  # Add custom hover text
    hoverinfo='text'  # Display only the custom hover text
)

# Adjust the number of points in the meshgrid to increase the size of the plane
x_range = np.linspace(cleaned_df['AGE'].min()-1, 
                      cleaned_df['AGE'].max()+1, 50)  # Increase the range and mesh points

y_range = np.linspace(cleaned_df['ABDOMEN'].min()-1, 
                      cleaned_df['ABDOMEN'].max()+1, 50)  # Increase the range and mesh points

x_mesh, y_mesh = np.meshgrid(x_range, y_range)

z_mesh = (results['Intercept'] + 
          results['Coefficient (AGE)'] * x_mesh + 
          results['Coefficient (ABDOMEN)'] * y_mesh)

plane = go.Surface(
    x=x_mesh,
    y=y_mesh,
    z=z_mesh,
    opacity=0.35,
    showscale=False,  # Disable color scale
    surfacecolor=np.full_like(z_mesh, 0.0),  # Set plane color to black
    colorscale="Greys",  # Black color for the plane
    name='Regression Plane'
)

# Adjust the layout to make the plot more cube-like by setting equal axis ranges
plot_layout = go.Layout(
    scene=dict(
        xaxis=dict(title='Age', range=[cleaned_df['AGE'].min()-3, 
                                       cleaned_df['AGE'].max()+3],  # Adjust x range
                   nticks=10),
        yaxis=dict(title='ABDOMEN', range=[cleaned_df['ABDOMEN'].min()-3, 
                                           cleaned_df['ABDOMEN'].max()+3],  # Adjust y range
                   nticks=10),
        zaxis=dict(title='Bodyfat (%)', range=[cleaned_df['BODYFAT'].min()-3, 
                                               cleaned_df['BODYFAT'].max()+3],  # Adjust z range
                   nticks=10),
        aspectmode='cube'  # This ensures the plot will be more cube-like
    ),
    margin=dict(l=0, r=0, b=0, t=0)
)

# Create the table
table_data = [
    ['Metric', 'Value'],
    ['Intercept', f"{results['Intercept']:.4f}"],
    ['p-value (Intercept)', f"{results['p-value (Intercept)']:.4f}"],
    ['Coefficient (AGE)', f"{results['Coefficient (AGE)']:.4f}"],
    ['p-value (AGE)', f"{results['p-value (AGE)']:.4f}"],
    ['Coefficient (ABDOMEN)', f"{results['Coefficient (ABDOMEN)']:.4f}"],
    ['p-value (ABDOMEN)', f"{results['p-value (ABDOMEN)']:.4f}"],
    ['R-squared (Test set)', f"{results['R-squared (Test set)']:.4f}"],
    ['Adjusted R-squared (Test set)', f"{results['Adjusted R-squared (Test set)']:.4f}"],
    ['RMSE (Test set)', f"{results['RMSE (Test set)']:.4f}"],
    ['F-statistic', f"{results['F-statistic']:.4f}"],
    ['p-value (F-statistic)', f"{results['p-value (F-statistic)']:.4f}"],
    ['AIC', f"{results['AIC']:.4f}"],
    ['BIC', f"{results['BIC']:.4f}"]
]

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
diagnostic_fig = generate_diagnostic_plots(results)

diagnostic_layout = html.Div([
    dcc.Graph(
        id='diagnostic-plots',
        figure=diagnostic_fig,  # The diagnostic plot figure generated by the function
        style={'height': '800px'}  # Adjusted height for diagnostic plots
    )
])
