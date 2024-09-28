from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np
from scipy import stats
import pandas as pd
from plotly.subplots import make_subplots

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')

# Define the layout
layout = html.Div([
    html.H1("Exploratory Analysis and Data Visualization",
            style={'text-align': 'center', 'color': '#ee6c4d'}),
    
    html.Div([
        html.Div([
            dcc.Graph(id='correlation-heatmap', style={'height': '500px'}),
            html.P("Features Included in Heatmap:"),
            dcc.Dropdown(
                id='heatmap-features-dropdown',
                options=[{'label': col, 'value': col} for col in df.columns[1:]],  # Options from column names
                placeholder='Choose Features',
                multi=True,
                value=df.columns[1:4]  # Default features (choose first few columns as default)
            ),
        ], style={'width': '100%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='scatter-hist-plot', style={'height': '600px'}),
            html.Div([
                html.Div([
                    html.P("X-axis feature:"),
                    dcc.Dropdown(
                        id='x-axis-feature',
                        options=[{'label': col, 'value': col} for col in df.columns[1:]],
                        value=df.columns[1]
                    ),
                ], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([
                    html.P("Y-axis feature:"),
                    dcc.Dropdown(
                        id='y-axis-feature',
                        options=[{'label': col, 'value': col} for col in df.columns[1:]],
                        value=df.columns[2]
                    ),
                ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
            ]),
        ], style={'width': '100%', 'display': 'inline-block'}),
    ]),

html.Div([
    # Previous Page button
    dcc.Link('Go to Previous Page', href='/first_page', style={
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
    }),

    # Next Page button
    dcc.Link('Go to Next Page', href='/landing_page', style={
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
], style={
    'display': 'flex',
    'justifyContent': 'space-between',
    'padding': '20px'
})
])

# Callback to update correlation heatmap based on selected features
@callback(
    Output('correlation-heatmap', 'figure'),
    Input('heatmap-features-dropdown', 'value')
)
def update_heatmap(selected_features):
    if not selected_features:  # Fallback in case no features are selected
        return go.Figure()

    filtered_df = df[selected_features]
    correlation_matrix = filtered_df.corr()

    heatmap_fig = go.Figure(
        data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='Inferno',
            zmin=-1,
            zmax=1
        )
    )

    heatmap_fig.update_layout(
        title="Correlation Matrix Heatmap",
        xaxis_nticks=36,
        height=500
    )

    return heatmap_fig

# Callback to update scatter plot with histograms
@callback(
    Output('scatter-hist-plot', 'figure'),
    Input('x-axis-feature', 'value'),
    Input('y-axis-feature', 'value')
)
def update_scatter_hist(x_feature, y_feature):
    # Create subplot figure
    fig = make_subplots(
        rows=2, cols=2,
        column_widths=[0.8, 0.2],
        row_heights=[0.2, 0.8],
        specs=[[{"type": "xy"}, {"type": "xy"}],
               [{"type": "xy"}, {"type": "xy"}]]
    )

    # Add scatter plot
    fig.add_trace(
        go.Scatter(x=df[x_feature], y=df[y_feature], mode='markers', name='Scatter'),
        row=2, col=1
    )

    # Add histogram for x-axis
    fig.add_trace(
        go.Histogram(x=df[x_feature], name=f'{x_feature} distribution'),
        row=1, col=1
    )

    # Add histogram for y-axis
    fig.add_trace(
        go.Histogram(y=df[y_feature], name=f'{y_feature} distribution'),
        row=2, col=2
    )

    # Add KDE plots
    kde_x = stats.gaussian_kde(df[x_feature].dropna())
    x_range = np.linspace(df[x_feature].min(), df[x_feature].max(), 100)
    fig.add_trace(
        go.Scatter(x=x_range, y=kde_x(x_range), mode='lines', name=f'{x_feature} KDE'),
        row=1, col=1
    )

    kde_y = stats.gaussian_kde(df[y_feature].dropna())
    y_range = np.linspace(df[y_feature].min(), df[y_feature].max(), 100)
    fig.add_trace(
        go.Scatter(x=kde_y(y_range), y=y_range, mode='lines', name=f'{y_feature} KDE'),
        row=2, col=2
    )

    # Update layout
    fig.update_layout(
        title=f"Scatter Plot with Histograms: {x_feature} vs {y_feature}",
        height=600,
        showlegend=False
    )

    fig.update_xaxes(title_text=x_feature, row=2, col=1)
    fig.update_yaxes(title_text=y_feature, row=2, col=1)

    return fig
