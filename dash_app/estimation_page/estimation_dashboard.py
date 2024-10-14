
from dash import dcc, html, Input, Output, callback
import numpy as np

# Given model coefficients and standard errors (unchanged)
intercept = -31.8595
age_coef = 0.554
abdomen_coef = 0.5281
intercept_se = 2.41157
age_se = 0.02644
abdomen_se = 0.02139

# Confidence Interval calculation function (unchanged)
def predict_with_confidence_interval(age, abdomen):
    predicted_bodyfat = intercept + age_coef * age + abdomen_coef * abdomen
    z_value = 1.96
    se_pred = np.sqrt(intercept_se**2 + (age * age_se)**2 + (abdomen * abdomen_se)**2)
    lower_bound = predicted_bodyfat - z_value * se_pred
    upper_bound = predicted_bodyfat + z_value * se_pred
    return predicted_bodyfat, lower_bound, upper_bound

# Layout for the app
estimation_layout = html.Div([
    html.Div([
        html.H1("Body Fat Percentage Predictor", style={
            'text-align': 'center',
            'color': '#FFFFFF',
            'font-size': '3em',
            'margin-bottom': '40px',
            'font-weight': 'bold'
        }),

        # Disclaimer
        html.Div([
            html.P("Disclaimer: This model has been trained only on men over 21 years of age in the United States. Persons not fitting these descriptions should seek alternative methods for body fat estimation.", style={
                'color': '#FFFFFF',
                'font-size': '1em',
                'margin-bottom': '20px',
                'text-align': 'center',
                'font-style': 'italic'
            })
        ]),

        # Card container for inputs
        html.Div([
            html.Label("Enter Age (years):", style={'color': '#FFFFFF', 'font-size': '1.2em', 'margin-bottom': '10px'}),
            dcc.Input(id='input-age', type='number', min=21, step=1, placeholder="Age (minimum 21)", style={
                'width': '100%', 'padding': '12px', 'border-radius': '8px', 'border': '2px solid #CCCCCC',
                'box-shadow': '2px 2px 6px rgba(0, 0, 0, 0.1)', 'margin-bottom': '20px'
            }),

            html.Label("Enter Abdomen Circumference (cm):", style={'color': '#FFFFFF', 'font-size': '1.2em', 'margin-bottom': '10px'}),
            dcc.Input(id='input-abdomen', type='number', min=38, step=0.1, placeholder="Abdomen Circumference (minimum 38 cm)", style={
                'width': '100%', 'padding': '12px', 'border-radius': '8px', 'border': '2px solid #CCCCCC',
                'box-shadow': '2px 2px 6px rgba(0, 0, 0, 0.1)', 'margin-bottom': '20px'
            }),

            html.Div([
                html.P("Measure abdomen circumference laterally at the level of the iliac crests, and anteriorly at the umbilicus.", style={
                    'color': '#FFFFFF',
                    'font-size': '0.9em',
                    'margin-bottom': '10px'
                }),
                html.Img(src="/api/placeholder/400/300", alt="Abdomen measurement guide", style={
                    'width': '100%',
                    'max-width': '400px',
                    'height': 'auto',
                    'margin-bottom': '20px',
                    'border-radius': '8px'
                })
            ]),

            # Predict Button
            html.Button('Predict Body Fat', id='predict-button', n_clicks=0, style={
                'width': '100%', 'padding': '12px', 'background-color': '#29a19c', 'color': 'white', 'border': 'none',
                'border-radius': '8px', 'font-size': '1.2em', 'cursor': 'pointer', 'margin-bottom': '20px',
                'box-shadow': '2px 2px 6px rgba(0, 0, 0, 0.1)', 'transition': 'background-color 0.3s ease'
            }),

            # Output Container
            html.Div(id='output-prediction', style={
                'background-color': '#FFFFFF', 'border-radius': '8px', 'padding': '20px',
                'box-shadow': '2px 2px 6px rgba(0, 0, 0, 0.1)', 'font-size': '1.5em',
                'color': '#000', 'font-weight': 'bold', 'text-align': 'center', 'margin-top': '20px'
            }),
        ], style={
            'background-color': '#293241', 'padding': '40px', 'border-radius': '12px', 'max-width': '500px',
            'margin': '0 auto', 'box-shadow': '2px 2px 12px rgba(0, 0, 0, 0.2)'
        }),

        # Link to navigate to the first page (introduction)
        dcc.Link(html.Button('Further Information', style={
            'fontSize': '20px', 'padding': '10px 20px', 'borderRadius': '10px', 'backgroundColor': '#ee6c4d',
            'color': 'white', 'border': 'none', 'cursor': 'pointer', 'boxShadow': '3px 3px 5px rgba(0, 0, 0, 0.2)',
            'margin-top': '40px', 'display': 'block', 'width': '200px', 'margin-left': 'auto', 'margin-right': 'auto'
        }), href='/first_page.introduction_description')
    ], style={
        'background-color': '#343a40', 'padding': '100px 0', 'min-height': '100vh', 'display': 'flex',
        'flex-direction': 'column', 'justify-content': 'center'
    })
])

# Callback to update the prediction result
@callback(
    Output('output-prediction', 'children'),
    [Input('input-age', 'value'),
     Input('input-abdomen', 'value'),
     Input('predict-button', 'n_clicks')]
)
def update_prediction(age, abdomen, n_clicks):
    if n_clicks > 0 and age and abdomen:
        if age < 21:
            return "Age must be 21 or older."
        if abdomen < 38:
            return "Abdomen circumference must be at least 38 cm."
        predicted_bodyfat, lower_bound, upper_bound = predict_with_confidence_interval(age, abdomen)
        return (f"Predicted Body Fat Percentage: {predicted_bodyfat:.2f}%\n"
                f"95% Confidence Interval: [{lower_bound:.2f}%, {upper_bound:.2f}%]")
    return "Please enter valid values for Age and Abdomen Circumference."
