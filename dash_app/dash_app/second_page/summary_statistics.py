
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats
from plotly.subplots import make_subplots

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')

# Define layout for visualizations and summary statistics
summary_statistics_layout = html.Div([
    html.H3("Data Analysis Dashboard:", style={'text-align': 'left', 'color': '#293241'}),
    
    # Dropdown for selecting feature
    html.Div([
        html.P("Choose a feature:"),
        dcc.Dropdown(
            id='feature-column',
            options=[{'label': col, 'value': col} for col in df.columns[1:]],  # Skipping the first column (likely ID)
            value=df.columns[1],
            clearable=False
        )
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    # Visualization section with subplots
    dcc.Graph(id='visualization-subplots', style={'height': '900px', 'margin-top': '20px'})
])

# Callback for updating the visualizations
@callback(
    Output('visualization-subplots', 'figure'),
    Input('feature-column', 'value')
)
def update_analysis(feature_column):
    column_data = df[feature_column].dropna()
    row_indices = df.index

    # Adding custom hover text with row information
    hover_text = [f"IDNO: {df.loc[i, 'IDNO']}, {feature_column}: {df.loc[i, feature_column]}" for i in row_indices]

    # Summary statistics (including outliers)
    summary_stats = {
        'Min': np.min(column_data),
        '25th Quantile': np.percentile(column_data, 25),
        'Median': np.median(column_data),
        '75th Quantile': np.percentile(column_data, 75),
        'Max': np.max(column_data),
        'Range': np.ptp(column_data),
        'Mean': np.mean(column_data),
        'Variance': np.var(column_data),
        'Standard Deviation': np.std(column_data),
        'IQR': stats.iqr(column_data),
        'Skew': stats.skew(column_data),
        'Kurtosis': stats.kurtosis(column_data)
    }
    
    # Outlier detection using z-scores
    z_scores = np.abs(stats.zscore(column_data))
    outliers = column_data[z_scores > 3]
    
    # Create 2x2 subplot figure
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=['Summary Statistics', 'Histogram', 'Boxplot', 'QQ-Plot'],
        specs=[[{'type': 'table'}, {'type': 'xy'}],
               [{'type': 'xy'}, {'type': 'xy'}]],
        vertical_spacing=0.2,
        horizontal_spacing=0.2
    )

    # (1,1) Summary Statistics Table
    stats_table = go.Table(
        header=dict(values=['<b>Metric</b>', '<b>Value</b>'],
                    fill_color='white',  # Set header background to white
                    align='left',
                    font=dict(size=12, color='black'),  # Set text color to black
                    line_color='black'),  # Set header border to black
        cells=dict(values=[
            ['Min', 
            '25th Quantile', 
            'Median', 
            '75th Quantile', 
            'Max', 
            'Range', 
            'Mean', 
            'Variance', 
            'Standard Deviation', 
            'IQR', 
            'Skew', 
            'Kurtosis', 
            'Outliers'],
            [f"{summary_stats['Min']:.4f}", 
            f"{summary_stats['25th Quantile']:.4f}", 
            f"{summary_stats['Median']:.4f}",
            f"{summary_stats['75th Quantile']:.4f}", 
            f"{summary_stats['Max']:.4f}", 
            f"{summary_stats['Range']:.4f}",
            f"{summary_stats['Mean']:.4f}", 
            f"{summary_stats['Variance']:.4f}", 
            f"{summary_stats['Standard Deviation']:.4f}",
            f"{summary_stats['IQR']:.4f}", 
            f"{summary_stats['Skew']:.4f}", 
            f"{summary_stats['Kurtosis']:.4f}", 
            str(outliers.tolist())]
        ], 
        fill_color='white',  # Set cell background to white
        align='left',
        font=dict(size=12, color='black'),  # Set text color to black
        line_color='black')  # Set cell border to black
    )

    # Adding the table to the figure using add_trace
    fig.add_trace(stats_table, row=1, col=1)

    # (1,2) Histogram with rug plot as marginal, black border, and fewer bins
    fig.add_trace(
        go.Histogram(
            x=column_data, 
            name='Histogram', 
            histnorm='probability density', 
            marker=dict(
                color='#EE6C4D', 
                opacity=0.8, 
                line=dict(color='black', width=1)  # Add black border to histogram bars
            ),
            nbinsx=20,  # Reduce the number of bins (you can adjust this value)
            hovertext=hover_text,
            hoverinfo='text'
        ),
        row=1, col=2
    )

    
    # (2,1) Boxplot + Outliers with custom hover text
    fig.add_trace(
        go.Box(y=column_data, name='Boxplot', 
               marker=dict(color='#EE6C4D'),
               hovertext=hover_text),
        row=2, col=1
    )
    
    # (2,2) QQ Plot to Test Normality with custom hover text
    qq_theoretical = np.linspace(np.min(column_data), np.max(column_data), len(column_data))
    qq_actual = np.sort(column_data)
    fig.add_trace(
        go.Scatter(x=qq_theoretical, 
                   y=qq_actual, 
                   mode='markers', 
                   name='QQ-Plot', 
                   marker=dict(color='#EE6C4D'),
                   hovertext=hover_text,
                   hoverinfo='text'),
        row=2, col=2
    )
    fig.add_trace(
        go.Scatter(x=qq_theoretical, 
                   y=qq_theoretical, 
                   mode='lines', 
                   name='45-degree line',
                   line=dict(color='black')),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(title=f"Data Visualizations for {feature_column}", 
                      height=900, 
                      showlegend=False, 
                      plot_bgcolor='white', 
                      paper_bgcolor='white')
    
    return fig
