import plotly.graph_objs as go
from dash import dcc, html, Input, Output, State, callback

# Given model coefficients and standard errors (unchanged)
intercept = -31.8595
age_coef = 0.0554
abdomen_coef = 0.5281

# Function to predict body fat percentage
def predict_body_fat(age, abdomen):
    return intercept + age_coef * age + abdomen_coef * abdomen

# Function to get classification ranges based on age
def get_classification_ranges(age):
    if 20 <= age <= 39:
        return 0, 50, [8, 20, 25], ["Very Thin", "Normal", "High", "Obese"]  # Changed range_max to 50
    elif 40 <= age <= 59:
        return 0, 50, [11, 22, 28], ["Very Thin", "Normal", "High", "Obese"]  # Changed range_max to 50
    elif 60 <= age <= 79:
        return 0, 50, [13, 25, 30], ["Very Thin", "Normal", "High", "Obese"]  # Changed range_max to 50
    else:
        return None

# Function to generate number line plot
def generate_number_line_plot(age, body_fat):
    range_min, range_max, thresholds, labels = get_classification_ranges(age)

    fig = go.Figure()

    # Add labels
    for i, label in enumerate(labels):
        if i == 0:
            x_pos = (range_min + thresholds[0]) / 2
        elif i == len(labels) - 1:
            x_pos = (thresholds[-1] + range_max) / 2
        else:
            x_pos = (thresholds[i-1] + thresholds[i]) / 2
        
        fig.add_annotation(
            x=x_pos,
            y=0.7,
            text=f"<b>{label}<b>",
            showarrow=False,
            font=dict(size=10, color="black"),
        )

    # Add marker for predicted body fat (scatter marker is always on top)
    fig.add_trace(go.Scatter(
        x=[body_fat],
        y=[0.5],
        mode="markers",
        marker=dict(size=16, color="#EE6C4D", symbol="diamond"),
        name="Your Body Fat",
    ))

    # Customize the layout
    fig.update_layout(
        xaxis=dict(
            range=[0, 50],  # Set range from 0% to 50%
            tickmode="array",
            tickvals=[0] + thresholds + [50],  # Include 0% and 50%
            ticktext=[f"{t}%" for t in [0] + thresholds + [50]],  # Update tick text to show 0% to 50%
            showgrid=True,  # Ensure the grid is shown
            gridcolor='black',  # Set grid color to black
            gridwidth=2,  # Make the grid lines thicker
            layer="below traces"  # Ensure grid is below the marker
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,  # No grid on y-axis
            zeroline=False,
            layer="below traces"
        ),
        height=200,
        margin=dict(l=10, r=10, t=30, b=30),
        shapes=[dict(
            type="line", 
            x0=0,  # Start from 0
            x1=50,  # End at 50
            y0=0.5, 
            y1=0.5, 
            line=dict(color="black", width=2),
            layer="below"  # Place the line behind the marker
        )],
        title=dict(text=f"<b>Estimated Bodyfat:<b> {body_fat:.1f}%", x=0.5, y=0.95),
        showlegend=False,
        plot_bgcolor='#FFFFFF',  # Transparent background
        paper_bgcolor='#FFFFFF'
    )

    return fig

# Layout for the app
estimation_layout = html.Div([
    html.Div([
        html.H1("Body Fat Percentage Predictor", style={
            'text-align': 'center',
            'color': '#EE6C4D',
            'font-size': '2.5em',  # Reduced font size
            'margin-bottom': '20px',  # Reduced margin
            'font-weight': 'bold'
        }),

        # Disclaimer
        html.Div([
            html.P("Disclaimer: This model has been trained only on men over 21 years of age in the United States. Persons not fitting these descriptions should seek alternative methods for body fat estimation.", style={
                'color': '#293241',
                'font-size': '0.9em',  # Slightly smaller font size
                'margin-bottom': '10px',  # Reduced margin
                'text-align': 'center',
                'font-style': 'italic'
            })
        ]),

        # Card container for inputs
        html.Div([
            html.Label("Enter Age (years)", style={'color': '#EE6C4D', 'font-weight': 'bold', 'font-size': '1.1em', 'margin-bottom': '10px'}),
            dcc.Input(id='input-age', type='number', min=21, step=1, placeholder="Age (minimum 21)", style={
                'width': '100%', 'padding': '10px', 'border-radius': '6px', 'border': '2px solid #CCCCCC',
                'box-shadow': '3px 3px 6px rgba(0, 0, 0, 0)', 'margin-bottom': '15px'  # Adjusted shadow and margin
            }),

            html.Label("Enter Abdomen Circumference (centimeters)", style={'color': '#EE6C4D', 'font-weight': 'bold', 'font-size': '1.1em', 'margin-bottom': '10px'}),
            dcc.Input(id='input-abdomen', type='number', min=60, step=0.1, placeholder="Abdomen Circumference (minimum 60 cm)", style={
                'width': '100%', 'padding': '10px', 'border-radius': '6px', 'border': '2px solid #CCCCCC',
                'box-shadow': '3px 3px 6px rgba(0, 0, 0, 0)', 'margin-bottom': '15px'
            }),

            html.Div([
                html.P("Measure abdomen circumference laterally at the level of the iliac crests, and anteriorly at the umbilicus.", style={
                    'color': '#293241',
                    'font-size': '0.85em',
                    'margin-bottom': '10px'
                }),
                html.Img(src="https://github.com/Stochastic1017/Body-Fat-Study/blob/main/images/where_to_measure.jpg?raw=true", 
                    style={
                    'width': '100%',
                    'max-width': '350px',  # Reduced max-width
                    'height': 'auto',
                    'margin-bottom': '15px',
                    'margin-left': '40px',  # Reduced margin
                    'border-radius': '6px'
                })
            ]),

            # Predict Button
            html.Button('Predict Body Fat', id='predict-button', n_clicks=0, style={
                'width': '100%', 'padding': '10px', 'font-weight': 'bold', 'background-color': '#EE6C4D', 'color': 'white', 'border': 'none',
                'border-radius': '6px', 'font-size': '1.1em', 'cursor': 'pointer', 'margin-bottom': '15px',
                'box-shadow': '3px 3px 6px rgba(0, 0, 0, 0)', 'transition': 'background-color 0.3s ease'
            }),

            # Plot for the number line
            dcc.Graph(id='bodyfat-plot')
        ], style={
            'background-color': 'white', 'padding': '30px', 'border-radius': '10px', 'max-width': '480px',
            'margin': '0 auto', 'box-shadow': '3px 3px 3px rgba(0, 0, 0, 0)'  # Uniform shadow around the box
        }),

        # Health Indicator
        html.P('The health indicator is adapted from NIH/WHO Guidelines for BMI; Gallagher et al, American Journal of Clinical Nutrition, Vol 72, September 2000.', 
                style={
                        'color': '#293241',
                        'font-size': '0.9em',
                        'margin-bottom': '15px',
                        'text-align': 'center',
                        'font-style': 'italic'}),

        # Link to navigate to the first page (introduction)
        dcc.Link(html.Button('Further Information', style={
            'fontSize': '18px', 'font-weight': 'bold', 'padding': '8px 16px', 'borderRadius': '8px', 'backgroundColor': '#ee6c4d',
            'color': 'white', 'border': 'none', 'cursor': 'pointer', 'boxShadow': '3px 3px 6px rgba(0, 0, 0, 0.2)',
            'margin-top': '30px', 'display': 'block', 'width': '180px', 'margin-left': 'auto', 'margin-right': 'auto'
        }), href='/first_page.introduction_description', style={'textDecoration': 'none'})

    ], style={
        'background-color': '#FFFFF', 'padding': '80px 0', 'min-height': '100vh', 'display': 'flex',
        'flex-direction': 'column', 'justify-content': 'center'
    })
])

# Callback to update the plot
@callback(
    Output('bodyfat-plot', 'figure'),
    [Input('predict-button', 'n_clicks')],
    [State('input-age', 'value'),
     State('input-abdomen', 'value')]
)
def update_prediction(n_clicks, age, abdomen):
    if n_clicks > 0 and age and abdomen:
        if age < 21 or abdomen < 38:
            return {}

        predicted_bodyfat = predict_body_fat(age, abdomen)

        # Generate the plot with dynamic title
        fig = generate_number_line_plot(age, predicted_bodyfat)
        return fig

    return {}
