from dash import html, dcc

layout = html.Div([
    html.H3("Additional Insights:", style={'text-align': 'left', 'color': '#293241'}),

    html.P("This page provides further insights and detailed visualizations about body fat estimation."),
    
    # Add additional visualizations or content here
    
    # Link to navigate back to the first page
    dcc.Link('Go Back to Introduction', href='/first_page', style={
        'fontSize': '18px',
        'padding': '10px',
        'borderRadius': '10px',
        'backgroundColor': '#f7f7f7',
        'color': '#ee6c4d',
        'textDecoration': 'none',
        'border': '2px solid #ee6c4d',
        'display': 'inline-block',
        'marginTop': '20px'
    })
])
