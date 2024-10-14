
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import itertools
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import root_mean_squared_error
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import scipy.stats as stats
from scipy.interpolate import UnivariateSpline
from statsmodels.nonparametric.smoothers_lowess import lowess
from statsmodels.stats.outliers_influence import variance_inflation_factor


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

# Function to calculate VIF for a subset of features
def calculate_vif(X_subset):
    if X_subset.shape[1] == 1:
        # If there's only one feature, VIF can't be calculated, so return np.nan
        return np.nan
    else:
        vif_data = pd.DataFrame()
        vif_data['Feature'] = X_subset.columns
        vif_data['VIF'] = [variance_inflation_factor(X_subset.values, i) for i in range(X_subset.shape[1])]
        return vif_data['VIF'].mean()
    
# Function to fit all combinations of features
def fit_all_combinations(X_train, X_test, y_train, y_test):
    feature_names = X_train.columns
    all_combinations = []
    
    # Generate all non-empty subsets of features
    for r in range(1, len(feature_names) + 1):
        subsets = itertools.combinations(feature_names, r)
        all_combinations.extend(subsets)
    
    # List to store results
    results = []
    
    for combo in all_combinations:
        # Select the subset of features
        X_train_subset = X_train[list(combo)]
        X_test_subset = X_test[list(combo)]
        
        # Add a constant term to the model (intercept)
        X_train_subset = sm.add_constant(X_train_subset)
        X_test_subset = sm.add_constant(X_test_subset)
        
        # Fit the model
        model = sm.OLS(y_train, X_train_subset).fit()
        
        # Make predictions on the test set
        y_pred = model.predict(X_test_subset)
        
        # Calculate R-squared, RMSE, and VIF
        r_squared = model.rsquared
        rmse = root_mean_squared_error(y_test, y_pred)
        mean_vif = calculate_vif(X_train_subset.drop(columns='const'))  # Drop intercept for VIF calculation
        
        # Store the results
        results.append({
            'Features': ', '.join(combo),
            'R-squared': r_squared,
            'RMSE': rmse,
            'Mean VIF': mean_vif
        })
    
    # Create a DataFrame from the results
    results_df = pd.DataFrame(results)
    
    # Sort the DataFrame by RMSE from lowest to highest
    results_df = results_df.sort_values(by='RMSE', ascending=True).reset_index(drop=True)
    
    return results_df

def two_dim_regression(df, results, feature_1, feature_2):
    # Create custom hover text
    hover_text = [
        f"IDNO: {int(row['IDNO'])}<br>AGE: {row['AGE']}<br>ABDOMEN: {row['ABDOMEN']}<br>BODYFAT: {row['BODYFAT']}"
        for index, row in df.iterrows()
    ]

    # 3D scatter plot with custom hovertext
    scatter = go.Scatter3d(
        x=df[feature_1],
        y=df[feature_2],
        z=df['BODYFAT'],
        mode='markers',
        marker=dict(size=3.5, color=df['BODYFAT'], colorscale='Inferno', opacity=0.8),
        text=hover_text,  # Add custom hover text
        hoverinfo='text'  # Display only the custom hover text
    )

    # Adjust the number of points in the meshgrid to increase the size of the plane
    x_range = np.linspace(df[feature_1].min()-1, 
                          df[feature_1].max()+1, 50)  # Increase the range and mesh points

    y_range = np.linspace(df[feature_2].min()-1, 
                          df[feature_2].max()+1, 50)  # Increase the range and mesh points

    x_mesh, y_mesh = np.meshgrid(x_range, y_range)

    z_mesh = (results['Intercept'] + 
              results[f'Coefficient ({feature_1})'] * x_mesh + 
              results[f'Coefficient ({feature_2})'] * y_mesh)

    plane = go.Surface(
        x=x_mesh,
        y=y_mesh,
        z=z_mesh,
        opacity=0.35,
        showscale=False,  # Disable color scale
        surfacecolor=np.full_like(z_mesh, 0.0),  # Set plane color to black
        colorscale="Greys",  # Black color for the plane
        name='Regression Plane'
    )

    # Adjust the layout to make the plot more cube-like by setting equal axis ranges
    plot_layout = go.Layout(
        scene=dict(
            xaxis=dict(title=f"{feature_1} (in years)", range=[df[feature_1].min()-3, 
                                               df['AGE'].max()+3],  # Adjust x range
                    nticks=10),
            yaxis=dict(title=f"{feature_2} (in cm)", range=[df[feature_2].min()-3, 
                                               df[feature_2].max()+3],  # Adjust y range
                    nticks=10),
            zaxis=dict(title='Bodyfat (in %)', range=[df['BODYFAT'].min()-3, 
                                                   df['BODYFAT'].max()+3],  # Adjust z range
                    nticks=10),
            aspectmode='cube'  # This ensures the plot will be more cube-like
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )

    # Create the table
    table_data = [
        ['Metric', 'Value'],
        ['Intercept', f"{results['Intercept']:.4f}"],
        ['p-value (Intercept)', f"{results['p-value (Intercept)']:.4f}"],
        ['Coefficient (AGE)', f"{results['Coefficient (AGE)']:.4f}"],
        ['p-value (AGE)', f"{results['p-value (AGE)']:.4f}"],
        ['Coefficient (ABDOMEN)', f"{results['Coefficient (ABDOMEN)']:.4f}"],
        ['p-value (ABDOMEN)', f"{results['p-value (ABDOMEN)']:.4f}"],
        ['R-squared (Test set)', f"{results['R-squared (Test set)']:.4f}"],
        ['Adjusted R-squared (Test set)', f"{results['Adjusted R-squared (Test set)']:.4f}"],
        ['RMSE (Test set)', f"{results['RMSE (Test set)']:.4f}"],
        ['F-statistic', f"{results['F-statistic']:.4f}"],
        ['p-value (F-statistic)', f"{results['p-value (F-statistic)']:.4f}"],
        ['AIC', f"{results['AIC']:.4f}"],
        ['BIC', f"{results['BIC']:.4f}"]
    ]

    return scatter, plane, plot_layout, table_data

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

def generate_diagnostic_plots(results, df):
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
        x=fitted_values, 
        y=residuals, 
        mode='markers',
        marker=dict(color='black', size=9, opacity=0.5),
        hovertext=df['IDNO'],
        hoverinfo='text+x+y',
        name='Residuals vs Fitted'
    ), row=1, col=1)

    # Add LOESS smoothing line for Residuals vs Fitted
    lowess_result = lowess(residuals, fitted_values, frac=2/3, it=5)
    fig.add_trace(go.Scatter(
        x=lowess_result[:, 0], 
        y=lowess_result[:, 1], 
        mode='lines',
        line=dict(color='red', width=2),
        name='loess smoothing curve',
    ), row=1, col=1)

    # 2. Normal Q-Q plot (Standardized residuals)
    qq_theoretical = np.sort(stats.norm.ppf(np.linspace(0.001, 0.999, len(standardized_residuals))))
    qq_sample = np.sort(standardized_residuals)
    fig.add_trace(go.Scatter(
        x=qq_theoretical, 
        y=qq_sample, 
        mode='markers',
        marker=dict(color='black', size=9, opacity=0.5),
        hovertext=df['IDNO'],
        hoverinfo='text+x+y',
        name='Normal Q-Q'
    ), row=1, col=2)

    # Add diagonal reference line
    fig.add_trace(go.Scatter(
        x=qq_theoretical, 
        y=qq_theoretical, 
        mode='lines',
        line=dict(color='red', width=2),
    ), row=1, col=2)

    # 3. Scale-Location plot (Square root of standardized residuals vs fitted values)
    sqrt_standardized_residuals = np.sqrt(np.abs(standardized_residuals))
    fig.add_trace(go.Scatter(
        x=fitted_values, 
        y=sqrt_standardized_residuals, 
        mode='markers',
        marker=dict(color='black', size=9, opacity=0.5),
        hovertext=df['IDNO'],
        hoverinfo='text+x+y',
        name='Scale-Location'
    ), row=2, col=1)

    # Add LOESS smoothing line for Scale-Location plot
    lowess_result = lowess(sqrt_standardized_residuals, fitted_values, frac=2/3, it=5)
    fig.add_trace(go.Scatter(
        x=lowess_result[:, 0], 
        y=lowess_result[:, 1], 
        mode='lines',
        line=dict(color='red', width=2),
        name='loess smoothing curve',
    ), row=2, col=1)

    # 4. Residuals vs Leverage plot
    fig.add_trace(go.Scatter(
        x=leverage, 
        y=standardized_residuals, 
        mode='markers',
        marker=dict(color='black', size=9, opacity=0.5),
        hovertext=df['IDNO'],
        hoverinfo='text+x+y',
        name='Residuals vs Leverage'
    ), row=2, col=2)

    # Add LOESS smoothing line for Residuals vs Leverage plot
    lowess_leverage = lowess(standardized_residuals, leverage, frac=2/3, it=5)
    fig.add_trace(go.Scatter(
        x=lowess_leverage[:, 0], 
        y=lowess_leverage[:, 1], 
        mode='lines',
        line=dict(color='red', width=2),
        name='loess smoothing curve',
    ), row=2, col=2)

    # Set background color to white and grid color to light grey
    fig.update_layout(
        title="Regression Diagnostics",
        height=800, width=1200,
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=False  # Remove legend
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
