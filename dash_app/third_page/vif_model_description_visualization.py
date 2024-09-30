
from dash import dcc, html
from third_page.vif_model_plot import vif_regression_layout

# Main layout for the second page
third_layout = html.Div([
    html.H1("Minimum Variance Inflation Factor (VIF) Regression Model",
            style={'text-align': 'center', 'color': '#EE6C4D'}),

    html.H3("Controlling Multicollinearity with VIF:", 
            style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''
        A simple yet efficient way to remove redundant predictors in regression models is by controlling for multicollinearity. 
        Multicollinearity occurs when predictor variables are highly correlated with one another, which inflates the variance of the 
        regression coefficients and makes the model unstable.

        One of the best methods to identify multicollinearity is to calculate the **Variance Inflation Factor (VIF)**. A general rule 
        of thumb is to choose predictors with VIF values below a chosen threshold (here, we have it at 15). Here's how you can remove 
        predictors with high VIF values iteratively:
'''),

    html.H3("Steps to Reduce Multicollinearity Using VIF:", 
            style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''
        1. Compute VIF for all predictors and sort them in descending order.
        2. Identify the predictor with the highest VIF value.
        3. If this value is greater than the chosen threshold, remove the predictor from the model.
        4. Recompute VIF and repeat the process until all remaining predictors have VIF values below the threshold.
'''),

    html.H3("Implementation of vif minimization algorithm:", 
            style={'text-align': 'left', 'color': '#293241'}),

     dcc.Markdown('''                 
        ```
        Feature        VIF
        0     AGE  10.191546
        1  WEIGHT  10.191546
        ```
                 
        This implies that after applying the multicollinearity reduction procedure to our dataset, we find that the predictors **Age** and **Weight** have 
        VIF values below 20, indicating low multicollinearity. This result aligns well with our goal of creating a practical and easy-to-use 
        rule-of-thumb for estimating body fat percentage.

        **Age** and **Weight** are particularly valuable predictors because they are simple and widely accessible metrics. Unlike other measurements 
        that may require specialized equipment (such as skinfold calipers or body circumference measurements), **Age** and **Weight** can be easily 
        recorded with minimal tools and effort.

        By focusing on these predictors, we simplify the process of estimating body fat, making it more practical for use in everyday clinical 
        settings or even self-assessments. This approach strikes a balance between statistical robustness (through multicollinearity control) and 
        real-world convenience.
'''),

    # Include 3d scatterplot with regression plane
    vif_regression_layout,

    html.Div([
        # Previous Page button
        dcc.Link('Go to Previous Page', href='/second_page.exploratory_data_visualization', 
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