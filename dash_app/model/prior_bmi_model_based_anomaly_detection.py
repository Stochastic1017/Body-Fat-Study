
import pandas as pd

# Define the prior body fat model
def prior_bmi_model(adiposity, age):
    """
    Calculate the predicted body fat percentage using the prior model.
    
    --- inputs ---
    height (float): Height of the individual (in inches).
    weight (float): Weight of the individual (in pounds).
    age (int): Age of the individual (in years).
    
    --- output ---
    bodyfat (float): Predicted body fat percentage.
    """

    # Body fat percentage estimation based on BMI and age
    return 48.1 - (848 * (1 / adiposity)) + (0.079 * age) + (0.05 * age) + (39.0 * (1 / adiposity))

# Function to find anomalies based on the prior model
def find_anomalies(df, threshold):
    """
    Find anomalies in the dataset where the body fat values deviate significantly 
    from the predicted body fat using the prior model.
    
    --- inputs ---
    df (pd.DataFrame): Input dataframe with columns IDNO, BODYFAT, HEIGHT, WEIGHT, AGE.
    threshold (float): The deviation threshold above which a BODYFAT value is considered anomalous.
    
    --- output ---
    anomalies (pd.DataFrame): DataFrame containing rows where BODYFAT values 
                              significantly deviate from predicted body fat.
    """
    required_columns = ['IDNO', 'BODYFAT', 'ADIPOSITY', 'AGE']
    
    # Check if required columns are present
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Dataset must contain the following columns: {required_columns}")
    
    anomalies = []

    # Iterate over each row in the DataFrame
    for i, row in df.iterrows():
        idno = row['IDNO']
        bodyfat_actual = row['BODYFAT']
        adiposity = row['ADIPOSITY']
        age = row['AGE']

        bodyfat_predicted = prior_bmi_model(adiposity, age)

        # Skip rows with invalid predictions
        if bodyfat_predicted is None:
            continue

        deviation = abs(bodyfat_actual - bodyfat_predicted)
        
        # If the actual body fat deviates significantly from the predicted, flag it as an anomaly
        if deviation > threshold:
            anomalies.append({
                'IDNO': int(idno),
                'BODYFAT_ACTUAL': bodyfat_actual,
                'BODYFAT_PREDICTED': bodyfat_predicted,
                'DEVIATION': deviation
            })
    
    # Return the anomalies as a DataFrame
    return pd.DataFrame(anomalies)

# Function to clean anomalies and impute data for the model
def clean_df(df, anomalies):
    """
    Updates the 'BODYFAT' column in the main dataframe with the predicted body fat values 
    from the anomalies dataframe for the matching IDs.

    --- inputs ---
    df (pd.DataFrame): Original dataframe containing the 'BODYFAT' column.
    anomalies (pd.DataFrame): DataFrame containing the predicted 'BODYFAT' values and 'IDNO' for anomalies.
    
    --- output ---
    df (pd.DataFrame): Updated DataFrame with corrected 'BODYFAT' values.
    """
    # Merge df with anomalies on 'IDNO' to match rows and update the 'BODYFAT' column
    df_updated = pd.merge(df, anomalies[['IDNO', 'BODYFAT_PREDICTED']], on='IDNO', how='left')

    # Update 'BODYFAT' with the predicted values where available
    df_updated['BODYFAT'] = df_updated['BODYFAT_PREDICTED'].combine_first(df_updated['BODYFAT'])

    # Drop the extra 'BODYFAT_PREDICTED' column that was added during the merge
    df_updated.drop(columns=['BODYFAT_PREDICTED'], inplace=True)

    return df_updated
