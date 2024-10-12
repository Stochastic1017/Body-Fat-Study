
import os
import sys
import pandas as pd
import numpy as np
from dash import dcc, html
import plotly.graph_objs as go
from sklearn.model_selection import train_test_split

# Ensure the current working directory is part of the path
sys.path.append(os.getcwd())

from model.multiple_regression import run_regression_and_summary, generate_diagnostic_plots, fit_all_combinations

# Load the data
cleaned_df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/cleaned_bodyfat.csv')

X = cleaned_df[["AGE", "ADIPOSITY", "ABDOMEN"]]
y = cleaned_df["BODYFAT"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.2, 
                                                    random_state=123)

results_df = fit_all_combinations(X_train, X_test, y_train, y_test)

# Replace NaN values in the VIF column to avoid issues with color generation
vif_column = results_df['Mean VIF'].fillna(0)

# Creating the table figure
table_fig = go.Figure(data=[go.Table(
    header=dict(
        values=[f"<b>{col}</b>" for col in results_df.columns],  # Bold headers
        fill_color='#293241',  # Header background color
        font=dict(color='white', size=12),  # White text
        align='center',  # Center align headers
    ),
    cells=dict(
        values=[results_df[col] for col in results_df.columns],  # Table data
        fill_color=[
            ['white'] * len(vif_column),  # All cells white except VIF
            ['white'] * len(vif_column),
            ['white'] * len(vif_column),
        ],
        align='center',  # Center align cells
        font=dict(size=11)  # Set font size for a tighter layout
    )
)])

# Update layout for better visuals and reduce bottom space
table_fig.update_layout(
    title_x=0.5,  # Center the title
    margin=dict(l=50, r=50, t=20, b=20),  # Adjust margins (reduce bottom space)
    height=300,  # Set the height to a more appropriate value
    autosize=False  # Disable autosize to maintain the fixed height
)

# Return the layout for the table
combination_table_layout = html.Div([
    dcc.Graph(
        id='results-table',
        figure=table_fig,
        style={'height': '300px'}  # Adjusted height for the table
    )
],
style={'display': 'flex', 'justify-content': 'center', 
       'align-items': 'center', 'width': '100%'}  # Center the table
)

# Separate features and response
X_train = X_train[["AGE", "ADIPOSITY"]]
X_test = X_test[["AGE", "ADIPOSITY"]]

# Fitting regression model
results = run_regression_and_summary(X_train, y_train, X_test, y_test)

# Create custom hover text
hover_text = [
    f"IDNO: {int(row['IDNO'])}<br>AGE: {row['AGE']}<br>ADIPOSITY: {row['ADIPOSITY']}<br>BODYFAT: {row['BODYFAT']}"
    for index, row in cleaned_df.iterrows()
]

# 3D scatter plot with custom hovertext
scatter = go.Scatter3d(
    x=cleaned_df['AGE'],
    y=cleaned_df['ADIPOSITY'],
    z=cleaned_df['BODYFAT'],
    mode='markers',
    marker=dict(size=3.5, color=cleaned_df['BODYFAT'], colorscale='Inferno', opacity=0.8),
    text=hover_text,  # Add custom hover text
    hoverinfo='text'  # Display only the custom hover text
)

# Adjust the number of points in the meshgrid to increase the size of the plane
x_range = np.linspace(cleaned_df['AGE'].min()-1, 
                      cleaned_df['AGE'].max()+1, 50)  # Increase the range and mesh points

y_range = np.linspace(cleaned_df['ADIPOSITY'].min()-1, 
                      cleaned_df['ADIPOSITY'].max()+1, 50)  # Increase the range and mesh points

x_mesh, y_mesh = np.meshgrid(x_range, y_range)

z_mesh = (results['Intercept'] + 
          results['Coefficient (AGE)'] * x_mesh + 
          results['Coefficient (ADIPOSITY)'] * y_mesh)

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
        yaxis=dict(title='Adiposity', range=[cleaned_df['ADIPOSITY'].min()-3, 
                                             cleaned_df['ADIPOSITY'].max()+3],  # Adjust y range
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
    ['Coefficient (ADIPOSITY)', f"{results['Coefficient (ADIPOSITY)']:.4f}"],
    ['p-value (ADIPOSITY)', f"{results['p-value (ADIPOSITY)']:.4f}"],
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
