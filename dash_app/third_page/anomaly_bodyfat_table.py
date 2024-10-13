
from dash import dash_table, dcc, html, callback
from dash.dependencies import Input, Output
from model.prior_bmi_model_based_anomaly_detection import find_anomalies
import pandas as pd

# Load the dataset
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')

# Define the layout
anomaly_detection_layout = html.Div([
    html.H3("Interactive Body Fat Anomalies Table", 
            style={'text-align': 'center', 'color': '#293241'}),

    html.Label('Select Deviation Threshold:'),
    dcc.Slider(
        id='threshold-slider',
        min=1,
        max=20,
        step=1,
        value=11,
        marks={i: f'{i}%' for i in range(1, 21)}
    ),
    html.Div(id='threshold-value', style={'text-align': 'center', 'margin-bottom': '10px'}),

    dash_table.DataTable(
        id='anomaly-table',
        columns=[],
        data=[],
        sort_action="native",
        sort_mode="multi",
        row_deletable=False,
        page_action="native",
        page_current=0,
        page_size=10,
        style_header={
            'backgroundColor': '#293241',
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center'
        },
        style_cell={
            'textAlign': 'center'
        }
    )
])

# Callback to update the table based on the selected threshold
@callback(
    [Output('anomaly-table', 'data'),
     Output('anomaly-table', 'columns'),
     Output('threshold-value', 'children')],
    [Input('threshold-slider', 'value')]
)
def update_anomaly_table(threshold):
    # Call the anomaly detection function with the selected threshold
    anomalies_df = find_anomalies(df, threshold=threshold)

    # Update the table data and columns
    columns = [{"name": col, "id": col} for col in anomalies_df.columns]
    data = anomalies_df.to_dict('records')

    # Format the threshold text with extra spacing
    threshold_text = html.Div([
        html.Span(f"Chosen Threshold: {threshold}%", style={'font-weight': 'bold'}),
        html.Br(),
        html.Span(f"Number of Anomalies: {len(anomalies_df)}", style={'margin-top': '10px'})
    ])

    return data, columns, threshold_text
