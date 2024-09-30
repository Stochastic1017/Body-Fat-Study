
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')

# Define the layout for the correlation heatmap and VIF table
correlation_heatmap_layout = html.Div([
    html.H3("Interactable Correlation Heatmap and Variance Inflation Factor (VIF):", 
        style={'text-align': 'left', 'color': '#293241'}),
    html.P("Features Included in Heatmap and VIF calculator:"),
    dcc.Dropdown(
        id='heatmap-features-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns[1:]],  # Options from column names
        placeholder='Choose Features',
        multi=True,
        value=df.columns  # Default features (choose first few columns as default)
    ),
    dcc.Graph(id='correlation-heatmap', style={'height': '500px'}),
    dcc.Graph(id='vif-table', style={'height': '400px'}),], style={'width': '100%', 'display': 'inline-block', 'padding-bottom': '30px'})

# Function to compute VIF
def compute_vif(df):
    """Compute Variance Inflation Factor (VIF)"""
    vif_data = pd.DataFrame()
    vif_data['Feature'] = df.columns
    vif_data['VIF'] = [variance_inflation_factor(df.values, i) for i in range(len(df.columns))]
    return vif_data

# Callback to update correlation heatmap and VIF table based on selected features
@callback(
    Output('correlation-heatmap', 'figure'),
    Output('vif-table', 'figure'),
    Input('heatmap-features-dropdown', 'value')
)
def update_heatmap_and_vif(selected_features):
    if not selected_features:  # Fallback in case no features are selected
        return go.Figure(), go.Figure()

    # Filter the DataFrame based on selected features
    filtered_df = df[selected_features]

    # Compute correlation matrix
    correlation_matrix = filtered_df.corr()
    
    # Create heatmap figure
    heatmap_fig = go.Figure(
        data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='Oranges',
            zmin=-1,
            zmax=1
        )
    )
    heatmap_fig.update_layout(
        title="Correlation Matrix Heatmap",
        xaxis_nticks=36,
        height=500
    )

    # Compute VIF and create a table figure
    vif_data = compute_vif(filtered_df)
    vif_table_fig = go.Figure(
        data=[go.Table(
            header=dict(values=list(vif_data.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[vif_data.Feature, vif_data.VIF.round(2)],
                       fill_color='lavender',
                       align='left'))
        ]
    )
    vif_table_fig.update_layout(
        title="Variance Inflation Factor (VIF)",
        height=400
    )

    return heatmap_fig, vif_table_fig
