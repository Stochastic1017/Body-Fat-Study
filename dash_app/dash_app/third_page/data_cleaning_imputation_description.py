
from dash import dcc, html
from third_page.anomaly_bodyfat_table import anomaly_detection_layout

# Main layout for the second page
third_layout = html.Div([
    html.H1("Data Cleaning and Imputation Procedures",
            style={'text-align': 'center', 'color': '#EE6C4D'}),

    html.H3("Using prior models for imputation:", 
            style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''
        Upon examining the `BODYFAT` column, we identified certain values that are implausible. 
        For example, `IDNO=182` has a recorded `BODYFAT=0`, which is physiologically impossible. 
        Similarly, `IDNO=172` has a `BODYFAT=1.9`, which is highly improbable given the associated feature values. 
        To systematically identify other observations with similarly implausible values, 
        we employ a prior body fat estimation model to flag potential inconsistencies.
'''),

    html.H3("Prior model used for data imputation:", 
            style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''
        The data imputation model is based on the following reference:
                 
        > *Healthy percentage body fat ranges: an approach for developing guidelines based on body mass index. Gallagher, Dympna et al. The American Journal of Clinical Nutrition, Volume 72, Issue 3, 694 - 701.*
        
        The equation used is given below (after substituting $\\text{sex}=1$ for males):
        
        $$\\text{Percentage Body Fat} = 48.1 - 848 \\times (1/\\text{BMI}) + 0.079 \\times \\text{age} + 0.05 \\times \\text{age} + 39.0 \\times (1/\\text{BMI})$$
        
        where $$\\text{BMI} = 703 \\times \\frac{\\text{WEIGHT}}{\\text{HEIGHT}^2}$$.        
                 
        We compare these model-derived body fat estimates with the actual `BODYFAT` values in the dataset. 
        If the absolute difference exceeds a predefined threshold (currently $8\\%$), the data is flagged as an anomaly for further investigation and corrected using the model estimate.                
''', mathjax=True),

    # Anomaly detection table
    anomaly_detection_layout,

    html.H3("Advantages of imputation procedure:", 
            style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''     
    * **Robust identification of anomalies:**  Relies on a prior body fat estimation model backed by scientific research (Gallagher et al.). This approach ensures that all flagged data points are scientifically and statistically justified.
    
    * **Explainable and Interpretable:** As the model follows a multiple linear regression model with deterministic coefficients, it is easily explainable ans interpretable to a general audience. 

    * **Threshold based flexibility:** Gives us the ability to control sensitivity of anomaly detector, thus allow the flexibility for a more or less strict based on the acceptable level of deviation in body fat values.

    * **Handles Data Imputation Efficiently:** Allows us to both identify and correct the data by implementing a model-imputed body fat values for anomalous entries.             
'''),

    html.H3("Disadvantages of imputation procedure:", 
                style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''     
    * **Potential Data Loss:** Imputing data based on the prior model can lead to loss of original information, especially when the model is not perfectly aligned with the characteristics of the dataset.
    
    * **Explainable and Interpretable:** As the model follows a multiple linear regression model with deterministic coefficients, it is easily explainable ans interpretable to a general audience. 

    * **Threshold based flexibility:** Gives us the ability to control sensitivity of anomaly detector, thus allow the flexibility for a more or less strict based on the acceptable level of deviation in body fat values.

    * **Handles Data Imputation Efficiently:** Allows us to both identify and correct the data by implementing a model-imputed body fat values for anomalous entries.             
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
