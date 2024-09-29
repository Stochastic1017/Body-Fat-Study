from dash import dash_table, html, dcc
import pandas as pd

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')

data_table_layout = html.Div([
    html.H3("Interactable Data Table:", 
            style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''
The commonly available measurements include age, weight, height, bmi, and various
body circumference measurements. In particular, the variables listed below (from left to
right in the data set) are:

* ID number of individual: `IDNO`
* Percent body fat from Siri's (1956) equation: `BODYFAT`
* Density determined from underwater weighing: `DENSITY`
* Age (years): `AGE`
* Weight (lbs): `WEIGHT`
* Height (inches): `HEIGHT`
* Adioposity (bmi): `ADIPOSITY`
* Neck circumference (cm): `NECK`
* Chest circumference (cm): `CHEST`
* Abdomen 2 circumference (cm): `ABDOMEN`
* Hip circumference (cm): `HIP`
* Thigh circumference (cm): `THIGH`
* Knee circumference (cm): `KNEE`
* Ankle circumference (cm): `ANKLE`
* Biceps (extended) circumference (cm): `BICEPS`
* Forearm circumference (cm): `FOREARM`
* Wrist circumference (cm): `WRIST`   

Measurement standards are listed in Benhke and Wilmore (1974), pp. 45-48 where, for
instance, the abdomen 2 circumference is measured "laterally, at the level of the iliac
crests, and anteriorly, at the umbilicus."                      
''', mathjax=True),

    html.Div([ dash_table.DataTable(
    id='datatable-interactivity',
    columns=[
        {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
    ],
    data=df.to_dict('records'),
    sort_action="native",
    sort_mode="multi",
    row_selectable="multi",
    row_deletable=False,
    selected_columns=[],
    selected_rows=[],
    page_action="native",
    page_current= 0,
    page_size= 15,
    style_header={
    'color': 'white',
    'backgroundColor': '#293241',
    'fontWeight': 'bold',
    'textAlign': 'center'},
    style_cell={
    'textAlign': 'center'},)])
])
