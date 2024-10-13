
import itertools
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import root_mean_squared_error
from statsmodels.stats.outliers_influence import variance_inflation_factor
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.stats as stats
from scipy.interpolate import UnivariateSpline
from statsmodels.nonparametric.smoothers_lowess import lowess


def run_regression_and_summary(X_train, y_train, X_test, y_test):
    """
    Perform linear regression using statsmodels and return relevant statistics on the test set.
    """
    # Add a constant (intercept) to X_train
    X_train_with_const = sm.add_constant(X_train)

    # Fit the model using statsmodels
    model = sm.OLS(y_train, X_train_with_const).fit()

    # Add a constant (intercept) to X_test
    X_test_with_const = sm.add_constant(X_test)

    # Make predictions on the test set
    y_pred_test = model.predict(X_test_with_const)

    # Calculate residuals and fitted values for diagnostics
    residuals = model.resid  # Use the model's residuals attribute
    fitted_values = model.fittedvalues

    # Use in-built statsmodels metrics
    rmse_test = root_mean_squared_error(y_test, y_pred_test)
    r_squared_test = model.rsquared  # R-squared
    adj_r_squared_test = model.rsquared_adj  # Adjusted R-squared
    f_statistic = model.fvalue  # F-statistic
    p_value_f_statistic = model.f_pvalue  # P-value for F-statistic
    aic = model.aic  # AIC
    bic = model.bic  # BIC

    # Extract the necessary statistics from the model
    intercept = model.params['const']
    p_value_intercept = model.pvalues['const']
    
    coef_age = model.params.get('AGE', None)
    p_value_age = model.pvalues.get('AGE', None)
    
    coef_adiposity = model.params.get('ABDOMEN', None)
    p_value_adiposity = model.pvalues.get('ABDOMEN', None)

    # Create a dictionary with the required outputs
    results = {
        'Intercept': intercept,
        'p-value (Intercept)': p_value_intercept,
        'Coefficient (AGE)': coef_age,
        'p-value (AGE)': p_value_age,
        'Coefficient (ABDOMEN)': coef_adiposity,
        'p-value (ABDOMEN)': p_value_adiposity,
        'R-squared (Test set)': r_squared_test,
        'Adjusted R-squared (Test set)': adj_r_squared_test,
        'RMSE (Test set)': rmse_test,
        'F-statistic': f_statistic,
        'p-value (F-statistic)': p_value_f_statistic,
        'AIC': aic,
        'BIC': bic,
        'Residuals': residuals,
        'Fitted Values': fitted_values,
        'Leverage': model.get_influence().hat_matrix_diag,  # Leverage values
        'Standardized Residuals': model.get_influence().resid_studentized_internal,  # Standardized residuals
        'Cook\'s Distance': model.get_influence().cooks_distance[0]  # Cook's distance
    }
    
    return results

# Helper function to calculate LOESS-like smooth line
def loess_smoothing(x, y, smoothing_factor=1.5):  # Increased smoothing factor
    try:
        sorted_indices = np.argsort(x)
        sorted_x = np.array(x)[sorted_indices]
        sorted_y = np.array(y)[sorted_indices]
        # Use Univariate Spline for smoothing (LOESS-like)
        spline = UnivariateSpline(sorted_x, sorted_y, s=smoothing_factor)
        return sorted_x, spline(sorted_x)
    except Exception as e:
        print(f"Error in LOESS smoothing: {e}")
        # Return unsmoothed line as fallback if spline fails
        return x, y

def generate_diagnostic_plots(results):
    residuals = results['Residuals']
    fitted_values = results['Fitted Values']
    leverage = results['Leverage']
    standardized_residuals = results['Standardized Residuals']

    # Subplot layout
    fig = make_subplots(rows=2, cols=2, subplot_titles=(
        'Residuals vs Fitted',
        'Normal Q-Q',
        'Scale-Location',
        'Residuals vs Leverage'
    ))

    # 1. Residuals vs Fitted plot
    fig.add_trace(go.Scatter(
        x=fitted_values, y=residuals, mode='markers',
        marker=dict(color='black', size=8, opacity=0.5),
        name='Residuals vs Fitted'
    ), row=1, col=1)

    # Add LOESS smoothing line for Residuals vs Fitted
    lowess_result = lowess(residuals, fitted_values, frac=2/3, it=5)
    fig.add_trace(go.Scatter(
        x=lowess_result[:, 0], y=lowess_result[:, 1], mode='lines',
        line=dict(color='red', width=2), showlegend=True
    ), row=1, col=1)

    # 2. Normal Q-Q plot (Standardized residuals)
    qq_theoretical = np.sort(stats.norm.ppf(np.linspace(0.001, 0.999, len(standardized_residuals))))
    qq_sample = np.sort(standardized_residuals)
    fig.add_trace(go.Scatter(
        x=qq_theoretical, y=qq_sample, mode='markers',
        marker=dict(color='black', size=8, opacity=0.5),
        name='Normal Q-Q'
    ), row=1, col=2)
    fig.add_trace(go.Scatter(
        x=qq_theoretical, y=qq_theoretical, mode='lines',
        line=dict(color='red', width=2), showlegend=True
    ), row=1, col=2)

    # 3. Scale-Location plot (Square root of standardized residuals vs fitted values)
    sqrt_standardized_residuals = np.sqrt(np.abs(standardized_residuals))
    fig.add_trace(go.Scatter(
        x=fitted_values, y=sqrt_standardized_residuals, mode='markers',
        marker=dict(color='black', size=8, opacity=0.5),
        name='Scale-Location'
    ), row=2, col=1)

    # Add LOESS smoothing line for Scale-Location plot
    lowess_result = lowess(sqrt_standardized_residuals, fitted_values, frac=2/3, it=5)
    fig.add_trace(go.Scatter(
        x=lowess_result[:, 0], y=lowess_result[:, 1], mode='lines',
        line=dict(color='red', width=2), showlegend=True
    ), row=2, col=1)

    # 4. Residuals vs Leverage plot
    fig.add_trace(go.Scatter(
        x=leverage, y=standardized_residuals, mode='markers',
        marker=dict(color='black', size=8, opacity=0.5),
        name='Residuals vs Leverage'
    ), row=2, col=2)

    # Add zero line to Residuals vs Leverage plot
    fig.add_trace(go.Scatter(
        x=[min(leverage), max(leverage)], y=[0, 0], mode='lines',
        line=dict(color='red', dash='dash', width=2), showlegend=False
    ), row=2, col=2)

    # Set background color to white and grid color to light grey
    fig.update_layout(
        title="Regression Diagnostics (R-style)",
        height=800, width=1200,
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=False
    )

    # Update axis labels and grid
    fig.update_xaxes(title_text="Fitted Values", row=1, col=1, gridcolor='lightgrey')
    fig.update_yaxes(title_text="Residuals", row=1, col=1, gridcolor='lightgrey')
    fig.update_xaxes(title_text="Theoretical Quantiles", row=1, col=2, gridcolor='lightgrey')
    fig.update_yaxes(title_text="Standardized Residuals", row=1, col=2, gridcolor='lightgrey')
    fig.update_xaxes(title_text="Fitted Values", row=2, col=1, gridcolor='lightgrey')
    fig.update_yaxes(title_text="√|Standardized Residuals|", row=2, col=1, gridcolor='lightgrey')
    fig.update_xaxes(title_text="Leverage", row=2, col=2, gridcolor='lightgrey')
    fig.update_yaxes(title_text="Standardized Residuals", row=2, col=2, gridcolor='lightgrey')

    return fig
