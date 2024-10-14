
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from estimation_page.estimation_dashboard import estimation_layout
from landing_page.cover_page import landing_layout
from first_page.introduction_description import first_layout
from second_page.exploratory_data_visualization import second_layout
from third_page.data_cleaning_imputation_description import third_layout
from fourth_page.find_best_predictors_description import fourth_layout
from fifth_page.mlr_description import fifth_layout

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
    elif pathname == '/estimation_page.estimation_dashboard':
        return estimation_layout
    elif pathname == '/first_page.introduction_description':
        return first_layout
    elif pathname == '/second_page.exploratory_data_visualization':
        return second_layout
    elif pathname == '/third_page.data_cleaning_imputation_description':
        return third_layout
    elif pathname == '/fourth_page.find_best_predictors_description':
        return fourth_layout
    elif pathname == '/fifth_page.mlr_description':
        return fifth_layout
    else:
        return landing_layout

if __name__ == '__main__':
    app.run_server(debug=True)
