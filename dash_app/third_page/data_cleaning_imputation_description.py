
from dash import dcc, html
from third_page.anomaly_bodyfat_table import anomaly_detection_layout

# Main layout for the second page
third_layout = html.Div([
    html.H1("Data Cleaning and Imputation Procedures",
            style={'text-align': 'center', 'color': '#EE6C4D'}),

    html.H3("Using prior models for imputation:", 
            style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''
        Upon examining the $$\\texttt{BODYFAT}$$ column, we identified certain values that are implausible. 
        For example, $$\\texttt{IDNO}:182$$ has a recorded $$\\texttt{BODYFAT}:0$$, which is physiologically impossible. 
        Similarly, $$\\texttt{IDNO}:172$$ has a $$\\texttt{BODYFAT}:1.9$$, which is highly improbable given the associated feature values. 
        To systematically identify other observations with similarly implausible values, 
        we employ a prior body fat estimation model to flag potential inconsistencies.
''', mathjax=True),

    html.H3("Prior model used for data imputation:", 
            style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''
        The data imputation model is based on the following reference:
                 
        > *Healthy percentage body fat ranges: an approach for developing guidelines based on body mass index. Gallagher, Dympna et al. The American Journal of Clinical Nutrition, Volume 72, Issue 3, 694 - 701.*
        
        The equation used is given below (after substituting $$\\texttt{sex}: 1$$ for males):
        
        $$
        \\texttt{BODYFAT} = 48.1 - 848 \\times (1/\\texttt{ADIPOSITY}) + 0.079 \\times \\texttt{AGE} + 0.05 \\times \\texttt{AGE} + 39.0 \\times (1/\\texttt{ADIPOSITY})
        $$
                 
        We compare these model-derived body fat estimates with the actual $$\\texttt{BODYFAT}$$ values in the dataset. 
        If the absolute difference exceeds a predefined threshold (currently $$11\\%$$), the data is flagged as an anomaly for further investigation and corrected using the model estimate.                
''', mathjax=True),

    # Anomaly detection table
    anomaly_detection_layout,

        dcc.Markdown('''
        We can see that at threshold $$11\\%$$, the $$\\texttt{IDNO}:182$$ with $$\\texttt{BODYFAT}:0$$ is not flagged as an outlier.
        Due to this, we fix that observation by plugging in the prior model estimation manually.
''', mathjax=True),

    html.H3("Advantages of Imputation Procedure:", 
            style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''     
    * **Scientifically backed anomaly detection:** Utilizes a prior body fat estimation model (Gallagher et al.), ensuring anomalies are flagged based on established research.
        
    * **High interpretability:** Follows a simple linear regression model, making it easy to explain to non-technical audiences.

    * **Adjustable sensitivity:** The threshold-based approach provides flexibility in controlling the strictness of anomaly detection, depending on acceptable deviations.

    * **Effective imputation:** Corrects anomalies with model-driven imputation, maintaining data integrity while filling gaps efficiently.             
    '''),

    html.H3("Disadvantages of Imputation Procedure:", 
            style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''     
    * **Risk of over-imputation:** Excessive reliance on the model may overwrite valid but unusual data points, leading to potential loss of original data.

    * **Model bias:** The model assumes uniform behavior across individuals, which may not account for unique variations or population-specific characteristics.

    * **Limited flexibility:** The procedure relies heavily on one estimation model, which may not capture the full complexity of human body fat distribution.

    * **Threshold sensitivity:** While the threshold offers flexibility, setting it too high or low may either miss genuine outliers or over-correct data.
    '''),

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
        dcc.Link('Go to Next Page', href='/fourth_page.find_best_predictors_description', style={
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
