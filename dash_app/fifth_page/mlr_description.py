
from dash import dcc, html
from fifth_page.mlr_visualization import regression_layout, combination_table_layout, diagnostic_layout

# Main layout for the fifth page
fifth_layout = html.Div([
    html.H1("Fitting Multiple Linear Regression Model",
        style={'text-align': 'center', 'color': '#EE6C4D'}),

    html.H3("Finding the best feature combination for MLR model:",
            style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''
    Based on our analysis, we considered a set of features — AGE, ADIPOSITY, and ABDOMEN — yielding a total of $$2^4 = 16$$ possible feature combinations.

    The objective is to determine the most suitable feature combination based on the following criteria:
    
    1. **Low Root Mean Square Error (RMSE)**: This indicates better predictive accuracy.
    
    2. **Ease of Measurement**: Simpler or more accessible measurements are preferable for practical use.
    
    3. **Minimized Variance Inflation Factor (VIF)**: To avoid multicollinearity, we aim to choose features that have low VIF values, ensuring that predictors are not highly correlated with each other.
''', mathjax=True),

    combination_table_layout,

    dcc.Markdown('''
    After evaluating all combinations, we observe that the feature combination of **AGE** and **ADIPOSITY** strikes the ideal balance between several important factors:
    - **R-squared** and **RMSE**: This model captures a substantial portion of the variance in the body fat data, and the predictive error remains low, indicating the model's accuracy on unseen data.
    - **Ease of Measurement**: Only AGE, WEIGHT, and HEIGHT is required in order to compute the predictors, which is extremely practical for estimating bodyfat.
    - **VIF**: The model maintains low multicollinearity, suggesting that the predictors are largely independent and contribute uniquely to the prediction of body fat.

    This model balances statistical rigor with practical considerations, offering both accuracy and simplicity for real-world applications.`
''', mathjax=True),

    html.H3("Equation of the multiple linear model:",
            style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''
    Our final multiple linear regression model equation:
    $$
    \\hat{\\text{BODYFAT}} = -18.3929 + (0.1056) \\cdot \\text{Age} + (1.3360) \\cdot \\text{Adiposity})
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
        dcc.Link('Go to Next Page', href='/landing_page.cover_page', style={
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
