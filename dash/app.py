from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Initialize the app
app = Dash(__name__, suppress_callback_exceptions=True)

# Main layout with URL routing
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Tracks the current URL
    html.Div(id='page-content')  # Content is rendered here based on URL
])

# Callback to manage page routing based on the URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/first_page':
        from first_page import layout
        return layout
    elif pathname == '/second_page':
        from second_page import layout
        return layout
    else:
        from landing_page import layout
        return layout

if __name__ == '__main__':
    app.run_server(debug=True)
