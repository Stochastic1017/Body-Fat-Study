# callbacks.py
from dash import Input, Output, callback
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')

# Callback for updating the box plot with jittered data (existing)
@callback(
    Output('boxplot-features', 'figure'),
    Input('boxplot-features-dropdown', 'value')
)
def update_boxplot(features):
    if not features:
        return go.Figure()

    fig = go.Figure()
    
    # Add jittered box plots for selected features
    for feature in features:
        fig.add_trace(go.Box(y=df[feature], name=feature, 
                             boxpoints='all', jitter=0.3, pointpos=-1.8))

    fig.update_layout(
        title="Box Plot with Jittered Data",
        showlegend=False,
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

# Callback for updating the correlation heatmap (existing)
@callback(
    Output('correlation-heatmap', 'figure'),
    Input('heatmap-features-dropdown', 'value')
)
def update_heatmap(selected_features):
    if not selected_features:
        return go.Figure()

    correlation_matrix = df[selected_features].corr()

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
        height=500
    )

    return heatmap_fig

# Callback for updating the scatter plot with histograms and OLS regression (new)
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
                   marker=dict(
                               size=10, 
                               opacity=0.5, 
                               color="#E97451")),
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

    # Create a more detailed and aesthetically pleasing OLS summary table
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

    # Update subplot backgrounds
    fig.update_xaxes(showgrid=True, gridcolor='lightgrey', row=1, col=1)
    fig.update_yaxes(showgrid=True, gridcolor='lightgrey', row=1, col=1)
    fig.update_xaxes(showgrid=True, gridcolor='lightgrey', row=2, col=2)
    fig.update_yaxes(showgrid=True, gridcolor='lightgrey', row=2, col=2)

    return fig