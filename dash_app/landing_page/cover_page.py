
from dash import html, dcc

landing_layout = html.Div(
    style={'height': '100vh', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center', 'alignItems': 'center', 'backgroundColor': '#f7f7f7'},
    children=[
        html.H1("Body Fat Estimation Made Easy: A Data-Driven Approach", 
                style={'fontSize': '60px', 'color': '#ee6c4d', 'textAlign': 'center', 'margin': '0'}),
        
        html.H2("Authors: Shrivats Sudhir, Xiangchen Li, Will Wang", 
                style={'fontSize': '24px', 'color': '#807A79', 'textAlign': 'center', 'margin': '20px 0'}),

        # Link to navigate to the first page (introduction)
        dcc.Link(html.Button('Start', style={
            'fontSize': '20px',
            'padding': '10px 20px',
            'borderRadius': '10px',
            'backgroundColor': '#ee6c4d',
            'color': 'white',
            'border': 'none',
            'cursor': 'pointer',
            'boxShadow': '3px 3px 5px rgba(0, 0, 0, 0.2)'
        }), href='/estimation_page.estimation_dashboard')
    ]
)
