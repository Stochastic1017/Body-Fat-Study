
from dash import html, dcc, dash_table
import pandas as pd

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')

first_layout = [
    html.H1("Background, Goals, and Data Description", 
            style={'text-align': 'center', 'color': '#ee6c4d'}),

    html.H3("Introduction:", 
            style={'text-align': 'left', 'color': '#293241'}),

    html.P("Accurate measurement of body fat can often be inconvenient or costly. "
           "However, it is important to have methods that make it easy to estimate body fat "
           "without these barriers. This project presents a simple, robust, and accurate model "
           "for estimating body fat percentage using measurements that are readily available in clinical settings.",
           style={'text-align': 'left', 'color': '#333'}),

    html.P("Based on a dataset of 252 men, which includes measurements of their body fat percentage "
           "and various body circumference measurements (such as chest, abdomen, and thigh), we aim to develop "
           "a 'rule-of-thumb' for estimating body fat. This model is designed to be practical and applicable "
           "to a wide range of clinical contexts, providing a reliable estimate without the need for specialized equipment.",
           style={'text-align': 'left', 'color': '#333'}),

    html.H3("About the Dataset:", 
            style={'text-align': 'left', 'color': '#293241'}),

    html.P("A variety of popular health books suggest that the readers assess their health, at least in "
           "part, by estimating their percentage of body fat. In Bailey (1994), for instance, the reader "
           "can estimate body fat from tables using their age and various skin-fold measurements "
           "obtained by using a caliper. Other texts give predictive equations for body fat using body "
           "circumference measurements (e.g. abdominal circumference) and/or skin-fold "
           "measurements. See, for instance, Behnke and Wilmore (1974), pp. 66-67; Wilmore "
           "(1976), p. 247; or Katch and McArdle (1977), pp. 120-132).",
           style={'text-align': 'left', 'color': '#333'}),

    html.P("Percentage of body fat for an individual can be estimated once body density has been "
           "determined. Folks (e.g. Siri (1956)) assume that the body consists of two components - "
           "lean body tissue and fat tissue. Letting",
           style={'text-align': 'left', 'color': '#333'}),

    dcc.Markdown('''
* $D=$ Body Density ($\\text{gm}/\\text{cm}^3$)
* $A=$ Proportion of Lean Body Tissue
* $B=$ Proportion of Fat Tissue ($A+B=1$)
* $a=$ Density of Lean Body Tissue ($\\text{gm}/\\text{cm}^3$)
* $b=$ Desntiy of Fat Tissue ($\\text{gm}/\\text{cm}^3$)

we have:

$$D = \\frac{1}{(A/a) + (B/b)}$$

Solving for $B$, we find:

$$B=\\frac{1}{D} \\times \\bigg[\\frac{ab}{(a-b)}\\bigg] - \\bigg[\\frac{b}{a-b}\\bigg]$$

Using the estimes $a=1.10\\text{ gm}/\\text{cm}^3$ and $b=0.90\\text{ gm}/\\text{cm}^3$  (see Katch and McArdle (1977), p. 111 or Wilmore (1976), p. 123) we come up with "Siri's equation":

$$\\text{Percentage of Body Fat (i.e. 100 $\\times B$)}=\\frac{495}{D}-450$$

The technique of underwater weighing "computes body volume as the difference between body weight measured in air and weight measured during water submersion. 
In other words, body volume is equal to the loss of weight in water with the appropriate
temperature correction for the water's density" (Katch and McArdle (1977), p. 113).

Using this technique:
                 
$$\\text{Body Density} = \\frac{\\text{WA}}{\\frac{\\text{WA} - \\text{WW}}{\\text{c.f.}} - \\text{LV}}$$

where (Katch and McArdle (1977), p. 115)
                 
* $\\text{WA}=$ Weight in air (kg)
* $\\text{WW}=$ Weight in water (kg)                 
* $\\text{c.f.}=$ Water correction factor ($=1$ at $39.2$ deg $F$ as one-gram of water occupies exactly on $\\text{cm}^3$ at this temperature, $=0.997$ at $76-78$ deg $F$)
* $\\text{LV}=$ Residual Lung Volume (liters)

Other methods of determining body volume are given in Behnke and Wilmore (1974), p.
22 ff.

Unfortunately, the above process of determining body volume by underwater submersion,
while accurate, can be cumbersome and difficult to use by doctors who want to and easily
quickly determine a patient’s body fat percentage based on commonly available
measurements, even if it means sacrificing some accuracy guaranteed by underwater
measurements.
''', mathjax=True),

html.Div([
    # Previous Page button
    dcc.Link('Go to Previous Page', href='/landing_page.cover_page', style={
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

    # Next Page button
    dcc.Link('Go to Next Page', href='/second_page.exploratory_data_visualization', style={
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
], style={
    'display': 'flex',
    'justifyContent': 'space-between',
    'padding': '20px'
})
]