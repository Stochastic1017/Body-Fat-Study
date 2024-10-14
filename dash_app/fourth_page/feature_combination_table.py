
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from sklearn.model_selection import train_test_split
from model.multiple_regression import fit_all_combinations

# Load the data
cleaned_df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/cleaned_bodyfat_11.csv')

# Separate features and response
X = cleaned_df[["AGE", "ADIPOSITY", "ABDOMEN", "CHEST", "THIGH"]]
y = cleaned_df["BODYFAT"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

# Get model performance for all combination of features
results_df = fit_all_combinations(X_train, X_test, y_train, y_test)

# Format numbers to 4 decimal points
results_df = results_df.map(lambda x: f"{x:.4f}" if isinstance(x, (int, float)) else x)

# Handle NaN values in the Mean VIF column (replace NaN with 0)
results_df['Mean VIF'] = pd.to_numeric(results_df['Mean VIF'], errors='coerce').fillna(0)

# Replace NaN values in the VIF column to avoid issues with color generation
vif_column = results_df['Mean VIF'].fillna(0)

# Create a color scale for the 'Mean VIF' column (white to light orange)
def get_orange_gradient(value, max_value):
    # Ensure the intensity is between 0 and 1
    intensity = min(value / max_value if max_value > 0 else 0, 1)
    # RGB values for light orange: 255, 204, 153
    return f'rgba(255, 204, 153, {intensity})'

vif_colors = vif_column.apply(lambda x: get_orange_gradient(x, vif_column.max())).tolist()

# Creating the table figure
table_fig = go.Figure(data=[go.Table(
    header=dict(
        values=[f"<b>{col}</b>" for col in results_df.columns],  # Bold headers
        fill_color='#293241',  # Header background color
        font=dict(color='white', size=12),  # White text
        align='center'  # Center align headers
    ),
    cells=dict(
        values=[results_df[col] for col in results_df.columns],  # Table data
        fill_color=[
            ['white'] * len(vif_column),  # All cells white except VIF
            ['white'] * len(vif_column),
            ['white'] * len(vif_column),
            vif_colors  # Gradient for VIF
        ],  # Gradient for 'Mean VIF' column
        align='center'  # Center align cells
    )
)])

# Return the layout for the table
combination_table_layout = html.Div([
    dcc.Graph(
        id='results-table',
        figure=table_fig,
        style={'height': '800px'},
    )
], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'width': '100%'})
