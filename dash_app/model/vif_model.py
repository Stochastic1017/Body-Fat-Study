
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.linear_model import LinearRegression

def compute_vif(df):
    """Compute Variance Inflation Factor (VIF)"""
    vif_data = pd.DataFrame()
    vif_data['Feature'] = df.columns
    vif_data['VIF'] = [variance_inflation_factor(df.values, i) for i in range(len(df.columns))]
    return vif_data


def remove_multicollinearity(X, threshold=20):
    """
    Iteratively removes features with VIF above a given threshold to reduce multicollinearity.
    
    Parameters:
    X : pandas DataFrame
        The input data with features.
    threshold : float
        The VIF threshold. Features with VIF above this will be removed.
    
    Returns:
    pandas DataFrame
        The DataFrame with reduced multicollinearity (features with VIF > threshold removed).
    """
    Multicol = True
    curr_X = X.copy()
    while Multicol:
        vif_X = compute_vif(curr_X).sort_values(by='VIF', ascending=False)
        if vif_X['VIF'].iloc[0] > threshold:
            curr_X = curr_X.drop(columns=[vif_X['Feature'].iloc[0]])    
        else:
            Multicol = False
    return curr_X


df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')
vif_min_df = remove_multicollinearity( df.iloc[:, 2:len(df.columns)] )
y = df['BODYFAT']

lm = LinearRegression().fit(vif_min_df, y)
coefficient = lm.coef_
intercept = lm.intercept_