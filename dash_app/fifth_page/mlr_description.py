
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dash import dcc, html
from fifth_page.mlr_visualization import regression_layout, diagnostic_layout

# Main layout for the fifth page
fifth_layout = html.Div([
    html.H1("Fitting Multiple Linear Regression Model",
        style={'text-align': 'center', 'color': '#EE6C4D'}),

    html.H3("Equation of the multiple linear model:",
            style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''
    After fitting a preliminary multiple linear regression model, we find that $$\\texttt{IDNO}: 39$$ is outside the cook's distance and has a significant impact on the regression model.
    Due to this, we remove that corresponding observation and fit the regression model.
                 
    Our final multiple linear regression model equation:
    $$
    \\hat{\\texttt{BODYFAT}} = -31.8595 + (0.0554) \\cdot \\texttt{AGE} + (0.5281) \\cdot \\texttt{ABDOMEN}
    $$
''', mathjax=True),

    regression_layout,

    html.H3("Model diagnostics:",
            style={'text-align': 'left', 'color': '#293241'}),

    diagnostic_layout,

    html.Div([
        # Previous Page button
        dcc.Link('Go to Previous Page', href='/fourth_page.find_best_predictors_description', 
                 style={
                    'color': '#ee6c4d',
                    'fontSize': '20px',
                    'textDecoration': 'none',
                    'fontWeight': 'bold',
                    'padding': '10px',
                    'border': '2px solid #ee6c4d',
                    'borderRadius': '10px',
                    'backgroundColor': '#f7f7f7',
                    'textAlign': 'center',
                    'display': 'inline-block',
                    'transition': 'all 0.3s ease',
                    'boxShadow': '3px 3px 5px rgba(0, 0, 0, 0.2)'}),

        # Next Page button
        dcc.Link('Go Back to Calculator', href='/landing_page.cover_page', style={
                    'color': '#ee6c4d',
                    'fontSize': '20px',
                    'textDecoration': 'none',
                    'fontWeight': 'bold',
                    'padding': '10px',
                    'border': '2px solid #ee6c4d',
                    'borderRadius': '10px',
                    'backgroundColor': '#f7f7f7',
                    'textAlign': 'center',
                    'display': 'inline-block',
                    'transition': 'all 0.3s ease',
                    'boxShadow': '3px 3px 5px rgba(0, 0, 0, 0.2)'
        })
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '20px'})
])
