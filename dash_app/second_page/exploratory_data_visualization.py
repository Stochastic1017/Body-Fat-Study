# second_page.py
from dash import dcc, html
from second_page.box_plot import box_plot_layout
from second_page.correlation_heatmap import correlation_heatmap_layout
from second_page.scatter_plot import scatter_plot_layout
from second_page.data_table import data_table_layout
import second_page.callbacks  # Ensure to import the callbacks file to register them

# Main layout for the second page
second_layout = html.Div([
    html.H1("Exploratory Analysis and Data Visualization",
            style={'text-align': 'center', 'color': '#ee6c4d'}),

    # Include Data Table
    data_table_layout,

    # Include the Box Plot layout
    box_plot_layout,

    # Include the Correlation Heatmap layout
    correlation_heatmap_layout,

    # Include the Scatter Plot layout
    scatter_plot_layout,

    html.Div([
        # Previous Page button
        dcc.Link('Go to Previous Page', href='/first_page.introduction_description', style={
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
