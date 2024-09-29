from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import statsmodels.api as sm
import numpy as np
from scipy import stats

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')

# Define the layout
layout = html.Div([
    html.H1("Exploratory Analysis and Data Visualization",
            style={'text-align': 'center', 'color': '#ee6c4d'}),
    
    # Section for interactable box plots with jittered points
    html.H3("Interactable Box Plots with Jittered Data:", 
        style={'text-align': 'left', 'color': '#293241'}),
    html.Div([
        dcc.Graph(id='boxplot-features', style={'height': '500px'}),
        html.P("Select Features for Box Plots:"),
        dcc.Dropdown(
            id='boxplot-features-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns[1:]],  # Options from column names
            placeholder='Choose Features',
            multi=True,
            value=df.columns[1:5]  # Default features
        ),
    ], style={'width': '100%', 'display': 'inline-block', 'padding-bottom': '30px'}),
    
    # Section for correlation heatmap
    html.H3("Interactable Correlation Heatmap:", 
        style={'text-align': 'left', 'color': '#293241'}),
    html.Div([
        dcc.Graph(id='correlation-heatmap', style={'height': '500px'}),
        html.P("Features Included in Heatmap:"),
        dcc.Dropdown(
            id='heatmap-features-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns[1:]],  # Options from column names
            placeholder='Choose Features',
            multi=True,
            value=df.columns[1:10]  # Default features (choose first few columns as default)
        ),
    ], style={'width': '100%', 'display': 'inline-block'}),

    # Scatter plot and histogram section
    html.H3("Interactable Density Histogram and Scatterplot:", 
        style={'text-align': 'left', 'color': '#293241'}),
    html.Div([
        html.Div([
            html.P("X-axis feature:"),
            dcc.Dropdown(
                id='x-axis-feature',
                options=[{'label': col, 'value': col} for col in df.columns[1:]],
                value=df.columns[3]
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
    dcc.Graph(id='scatter-hist-plot', style={'height': '600px'}),
    
    # Navigation buttons
    html.Div([
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
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '20px', 'backgroundColor': 'white'})
])

# Callback to update box plot with jittered data based on selected features
@callback(
    Output('boxplot-features', 'figure'),
    Input('boxplot-features-dropdown', 'value')
)
def update_boxplots(selected_features):
    if not selected_features:
        return go.Figure()

    # Create figure with box plots and jittered data
    fig = go.Figure()
    for feature in selected_features:
        # Add box plot
        fig.add_trace(go.Box(y=df[feature], name=feature, boxpoints='all',
                             jitter=0.3, pointpos=-1.8))

    # Update layout
    fig.update_layout(
        title="Box Plots with Jittered Data for Selected Features",
        yaxis_title="Values",
        boxmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig

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
            colorscale='Oranges',
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

# Callback to update scatter plot with histograms and OLS
@callback(
    Output('scatter-hist-plot', 'figure'),
    Input('x-axis-feature', 'value'),
    Input('y-axis-feature', 'value')
)
def update_scatter_hist(x_feature, y_feature):
    # Create subplot figure
    fig = make_subplots(
        rows=2, cols=2,
        column_widths=[0.15, 0.1],
        row_heights=[0.1, 0.1],
        specs=[[{"type": "xy"}, {"type": "table"}],
               [{"type": "xy"}, {"type": "xy"}]]
    )

    # Add scatter plot
    fig.add_trace(
        go.Scatter(x=df[x_feature], 
                   y=df[y_feature], 
                   mode='markers', 
                   name='Scatter',
                   marker=dict(size=10, opacity=0.5, color="#E97451")),
        row=2, col=1
    )

    # Add OLS regression line
    x_vals = sm.add_constant(df[x_feature])
    ols_model = sm.OLS(df[y_feature], x_vals).fit()
    ols_line = ols_model.params.iloc[0] + ols_model.params.iloc[1] * df[x_feature]
    fig.add_trace(
        go.Scatter(x=df[x_feature], 
                   y=ols_line, 
                   mode='lines', 
                   name='OLS Line', 
                   line=dict(color='black')),
        row=2, col=1
    )

    # Add histogram for x-axis
    fig.add_trace(
        go.Histogram(x=df[x_feature], 
                     name=f'{x_feature} distribution', 
                     histnorm="probability density",
                     marker=dict(color='#9FE7F5', opacity=0.5)),
        row=1, col=1
    )

    # Add histogram for y-axis
    fig.add_trace(
        go.Histogram(y=df[y_feature], 
                     name=f'{y_feature} distribution', 
                     histnorm="probability density",
                     marker=dict(color="#F27F0C", opacity=0.5)),
        row=2, col=2
    )

    # Add KDE plots
    kde_x = stats.gaussian_kde(df[x_feature].dropna())
    x_range = np.linspace(df[x_feature].min(), df[x_feature].max(), 100)
    fig.add_trace(
        go.Scatter(x=x_range, 
                   y=kde_x(x_range), 
                   mode='lines', 
                   name=f'{x_feature} KDE', 
                   line=dict(color='#0197F6')),
        row=1, col=1
    )

    kde_y = stats.gaussian_kde(df[y_feature].dropna())
    y_range = np.linspace(df[y_feature].min(), df[y_feature].max(), 100)
    fig.add_trace(
        go.Scatter(x=kde_y(y_range), 
                   y=y_range, 
                   mode='lines', 
                   name=f'{y_feature} KDE', 
                   line=dict(color='#FF5B00')),
        row=2, col=2
    )

    # Create a more detailed OLS summary table
    ols_summary_table = [
        ['Coefficient', f"{ols_model.params.iloc[1]:.4f}"],
        ['Intercept', f"{ols_model.params.iloc[0]:.4f}"],
        ['P-value (coef)', f"{ols_model.pvalues.iloc[1]:.4e}"],
        ['P-value (intercept)', f"{ols_model.pvalues.iloc[0]:.4e}"],
        ['R-squared', f"{ols_model.rsquared:.4f}"],
        ['Adjusted R-squared', f"{ols_model.rsquared_adj:.4f}"],
        ['F-statistic', f"{ols_model.fvalue:.2f}"],
        ['Prob (F-statistic)', f"{ols_model.f_pvalue:.4e}"],
        ['AIC', f"{ols_model.aic:.2f}"],
        ['BIC', f"{ols_model.bic:.2f}"]
    ]

    fig.add_trace(go.Table(
        header=dict(values=[f'<b>{y_feature} ~ {x_feature}</b>', '<b>Details</b>'],
                    fill_color='#E6F3FF',
                    align='left',
                    font=dict(size=12, color='black')),
        cells=dict(values=list(zip(*ols_summary_table)),
                   fill_color=[['#F0F8FF', 'white']*7],
                   align='left',
                   font=dict(size=12))),
        row=1, col=2)

    # Update layout
    fig.update_layout(
        title=f"Scatter Plot with Histograms: {x_feature} vs {y_feature}",
        height=800,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    fig.update_xaxes(title_text=x_feature, row=2, col=1, showgrid=True, gridcolor='lightgrey')
    fig.update_yaxes(title_text=y_feature, row=2, col=1, showgrid=True, gridcolor='lightgrey')

    return fig
