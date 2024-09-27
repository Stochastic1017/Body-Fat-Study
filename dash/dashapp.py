from dash import Dash, dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')
app = Dash()

correlation_matrix = df.corr()

heatmap_fig = go.Figure(
    data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='Viridis'
    )
)
heatmap_fig.update_layout(title='Correlation Heatmap')

app.layout = [
    html.Div(children='Data Table'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=20)
]

app.layout = html.Div(children=[
    html.H1(children='Correlation Heatmap Example'),

    dcc.Graph(
        id='correlation-heatmap',
        figure=heatmap_fig
    )
])


if __name__ == '__main__':
    app.run(debug=True)