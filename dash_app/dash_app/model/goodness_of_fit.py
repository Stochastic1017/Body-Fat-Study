
import os
import sys

sys.path.append(os.getcwd())

from scipy.stats import f
import statsmodels.api as sm
import pandas as pd
import numpy as np

def general_goodness_of_fit(X, y, alpha=0.05):
    
    """
    Perform ANOVA-like goodness of fit test to see if any predictor is useful in the regression model.
    
    Parameters:
    X : pd.DataFrame
        Independent variables (predictors)
    y : pd.Series or np.array
        Dependent variable (response)
    alpha : float
        Significance level for hypothesis test (default: 0.05)
    
    Returns:
    out : pd.DataFrame
        Summary DataFrame showing SST, SSE, SSR, F-statistic, p-value, and critical F-value.
    """
    
    # Add a constant to the predictors (intercept term)
    X = sm.add_constant(X)
    
    # Fit the model
    model = sm.OLS(y, X).fit()
    
    # Get the number of observations
    n = len(y)
    
    # Total Sum of Squares (SST): Variability of the observed values from their mean
    SST = np.sum((y - np.mean(y))**2)
    
    # Error Sum of Squares (SSE): Variability of the residuals (unexplained by the model)
    SSE = np.sum(model.resid**2)
    
    # Regression Sum of Squares (SSR): Variability explained by the regression model
    SSR = SST - SSE
    
    # Mean Squared Error (MSE): Average variability in residuals
    MSE = SSE / model.df_resid
    
    # Mean Squared Regression (MSR): Average variability explained by the model
    MSR = SSR / model.df_model
    
    # F-statistic: MSR / MSE
    F_stat = MSR / MSE
    
    # Calculate the p-value from the F-distribution
    p_val = 1 - f.cdf(F_stat, model.df_model, model.df_resid)
    
    # Critical F-value for the chosen alpha level
    F_critical = f.ppf(1 - alpha, model.df_model, model.df_resid)
    
    # Output the results as a DataFrame
    out = pd.DataFrame({
        'SST': [SST],
        'SSE': [SSE],
        'SSR': [SSR],
        'F-statistic': [F_stat],
        'p-value': [p_val],
        'F-critical': [F_critical]
    })
    
    return out

# Function to create the table layout
def finding_most_significant_features(X, y, alpha=0.05):
    """
    Conducts F-tests to find the most significant features in the model using
    the Holm-Bonferroni method for multiple hypothesis testing.

    Parameters:
    ----------
    X : pd.DataFrame
        DataFrame containing the predictors (independent variables).
    y : pd.Series or np.ndarray
        The dependent variable (target) in the regression model.
    alpha : float, optional
        Significance level for hypothesis testing (default is 0.05).

    Returns:
    -------
    significant_features : list
        List of the most significant features based on the F-tests and Holm-Bonferroni correction.
    p_values : pd.Series
        Sorted p-values of the F-tests conducted for each feature.
    """

    # Add constant to X for intercept
    X = sm.add_constant(X)
    
    # Full model (with all predictors)
    full_model = sm.OLS(y, X).fit()
    
    # List to store p-values for each feature's F-test
    p_values = []

    # Perform F-test for each predictor (run reduced model by excluding one predictor)
    for feature in X.columns[1:]:  # Exclude the constant
        # Create reduced model by excluding current feature
        reduced_X = X.drop(columns=[feature])
        reduced_model = sm.OLS(y, reduced_X).fit()
        
        # Conduct ANOVA to compare reduced model to full model
        anova_results = sm.stats.anova_lm(reduced_model, full_model)
        
        # Get p-value of F-test (for this feature's inclusion)
        p_value = anova_results['Pr(>F)'][1]  # Extract the p-value for the full vs reduced comparison
        p_values.append((feature, p_value))
    
    # Convert p-values list into a DataFrame and sort by p-value
    p_values_df = pd.DataFrame(p_values, columns=['Feature', 'p-value']).sort_values(by='p-value')

    # Holm-Bonferroni correction
    num_tests = len(p_values_df)
    pvals_sorted = p_values_df['p-value'].values
    holm_bonferroni_thresholds = [alpha / (num_tests - i) for i in range(num_tests)]

    # Identify the most significant features using Holm-Bonferroni
    significant_features = []
    for i, p_value in enumerate(pvals_sorted):
        if p_value <= holm_bonferroni_thresholds[i]:
            significant_features.append(p_values_df['Feature'].values[i])
        else:
            break  # Stop once p-value exceeds its Holm-Bonferroni threshold

    return significant_features, p_values_df
