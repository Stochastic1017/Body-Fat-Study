from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from landing_page import layout as landing_layout
from first_page import layout as first_layout
from second_page import layout as second_layout

app = Dash(__name__, suppress_callback_exceptions=True, external_scripts=['https://cdn.plot.ly/plotly-latest.min.js'])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/landing_page':
        return landing_layout
    elif pathname == '/first_page':
        return first_layout
    elif pathname == '/second_page':
        return second_layout
    else:
        return landing_layout  # default to landing page

if __name__ == '__main__':
    app.run_server(debug=True)