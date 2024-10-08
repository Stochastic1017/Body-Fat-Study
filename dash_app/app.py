
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from landing_page.cover_page import landing_layout
from first_page.introduction_description import first_layout
from second_page.exploratory_data_visualization import second_layout
from third_page.vif_model_description_visualization import third_layout

app = Dash(__name__, 
           suppress_callback_exceptions=True, 
           external_scripts=['https://cdn.plot.ly/plotly-latest.min.js'])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/landing_page.cover_page':
        return landing_layout
    elif pathname == '/first_page.introduction_description':
        return first_layout
    elif pathname == '/second_page.exploratory_data_visualization':
        return second_layout
    elif pathname == '/third_page.vif_model_description_visualization':
        return third_layout
    else:
        return landing_layout

if __name__ == '__main__':
    app.run_server(debug=True)
