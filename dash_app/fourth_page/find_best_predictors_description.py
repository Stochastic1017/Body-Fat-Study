
from dash import dcc, html
from fourth_page.f_statistic_graph import f_test_table
from fourth_page.most_significant_features import best_predictors_table

# Main layout for the fourth page
fourth_layout = html.Div([
    html.H1("Feature Optimization for Body Fat Estimation",
        style={'text-align': 'center', 'color': '#EE6C4D'}),

    html.H3("Preliminary eliminating irrelevant features:",
            style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''
        To improve model accuracy and efficiency, we begin by removing features that are either redundant or provide little value to body fat estimation.

        * $$\\texttt{DENSITY}$$: This feature is excluded as it requires underwater weighing, a process that is expensive and impractical for most body fat estimation applications.

        * $$\\texttt{WEIGHT}$$, $$\\texttt{HEIGHT}$$: Since $$\\texttt{ADIPOSITY}$$ (Body Mass Index) is a function of $$\\texttt{WEIGHT}$$ and $$\\texttt{HEIGHT}$$, these features are removed to avoid redundancy and prevent multicollinearity in the model.

        * $$\\texttt{NECK}$$, $$\\texttt{KNEE}$$, $$\\texttt{ANKLE}$$, $$\\texttt{BICEPS}$$, $$\\texttt{FOREARM}$$, $$\\texttt{WRIST}$$, $$\\texttt{HIP}$$: These distal limb measurements are less directly related to body fat percentage compared to key circumferences like ABDOMEN and CHEST. Removing them reduces noise and complexity, focusing the model on more predictive features.

        Therefore, we will choose the best predictors for our model from the following: AGE, ADIPOSITY, CHEST, ABDOMEN, and THIGH.
''', mathjax=True),

    html.H3("Goodness of fit test to test if any predictor is useful:",
            style={'text-align': 'left', 'color': '#293241'}),
    
    dcc.Markdown('''Let $\\mathcal{X} =$ {$$\\texttt{AGE}$$, $$\\texttt{ADIPOSITY}$$, $$\\texttt{CHEST}$$, $$\\texttt{ABDOMEN}$$, $$\\texttt{THIGH}$$} be the set of our features.
''', mathjax=True),

    dcc.Markdown('''For feature $i \\in \\mathcal{X}$, let $\\beta_{i}$ be the corresponding regression coefficient, consider the following null and alternate hypothesis:              
''', mathjax=True),

    html.Div([
        dcc.Markdown('''
        $$H_0: \\forall i \\in \\mathcal{X}, \\quad \\beta_{i} = 0$$
                    
        $$H_1: \\exists i \\in \\mathcal{X}, \\quad \\beta_{i} \\neq 0$$
''', mathjax=True)], style={'text-align': 'center'}),

    dcc.Markdown(''' 
    We conduct the F-test for significance as follows:

    Let $n$ represent the number of observations, and $p$ represent the number of predictors in the model.

    **Step 1: Total Sum of Squares (SST)**
                
    This measures the total variance in the dependent variable $y$:
    $$
    \\text{SST} = \\sum_{i=1}^{n} (y_i - \\bar{y})^2
    $$
    Where $\\bar{y}$ is the mean of the observed values.

    **Step 2: Residual Sum of Squares (SSE)**
                
    This measures the variance that is *not explained* by the regression model:
    $$
    \\text{SSE} = \\sum_{i=1}^{n} (y_i - \\hat{y}_i)^2
    $$
    Where $\\hat{y}_i$ is the predicted value from the model for each observation.

    **Step 3: Regression Sum of Squares (SSR)**
                
    This measures the variance that is *explained* by the model:
    $$
    \\text{SSR} = \\text{SST} - \\text{SSE}
    $$

    **Step 4: Mean Squares and F-statistic**
                
    The Mean Squared Error (MSE) and the Mean Squared Regression (MSR) are calculated as follows:
    $$
    \\text{MSE} = \\frac{\\text{SSE}}{n - p}
    \\quad \\text{and} \\quad
    \\text{MSR} = \\frac{\\text{SSR}}{p - 1}
    $$

    Finally, the F-statistic is calculated as:
    $$
    F = \\frac{\\text{MSR}}{\\text{MSE}}
    $$

    This F-statistic is compared to a critical value from the F-distribution. 
    If the F-statistic is larger than the critical value, or if the p-value is less than the significance level, we reject the null hypothesis that no predictors are useful.
    ''', mathjax=True),

    f_test_table,

    dcc.Markdown("We can see that, as the p-value $$\\approx$$ 0, we can conclude that at least one predictor is useful.", mathjax=True),

    html.H3("ANOVA-Based Stepwise Feature Selection with Holm-Bonferroni Correction:",
            style={'text-align': 'left', 'color': '#293241'}),

dcc.Markdown('''
    To determine the most significant predictors in our model, we use a combination of **F-tests** and the **Holm-Bonferroni correction**.

    1. **F-Tests for each predictor**: 
    * For each predictor, we create a reduced model by excluding that variable and compare it to the full model using an Analysis of Variance (**ANOVA**). 
    * The *F-test* evaluates whether the excluded predictor contributes significantly to explaining the variance in the response variable.
    
    * The null and alternative hypotheses for the F-test (where $$j$$ is the predictor of interest) are:

    ''', mathjax=True),
    
html.Div([
    dcc.Markdown('''
    $$H_0: \\beta_{j} = 0$$ (The predictor $j$ has no effect, i.e., the variable is not useful)

    $$H_1: \\beta_{j} \\neq 0$$ (The predictor $j$ has an effect, i.e., the variable is useful)
    ''', mathjax=True)
], style={'text-align': 'center'}),

dcc.Markdown('''
    * The *F-statistic* is calculated as:
    $$
    F = \\frac{\\left( \\text{SSR}_{\\text{reduced}} - \\text{SSR}_{\\text{full}} \\right) / (p_{\\text{reduced}} - p_{\\text{full}})}{\\text{SSR}_{\\text{full}} / (n - p_{\\text{full}})}
    $$
    * where:
        - $$\\text{SSR}_{\\text{reduced}}$$ is the sum of squared residuals for the reduced model,
        - $$\\text{SSR}_{\\text{full}}$$ is the sum of squared residuals for the full model,
        - $$p_{\\text{reduced}}$$ and $$p_{\\text{full}}$$ are the number of parameters (including the intercept) in the reduced and full models,
        - $$n$$ is the number of observations.

    2. **Holm-Bonferroni Correction**:
        * To control for the increased risk of Type I errors due to multiple hypothesis testing, we apply the **Holm-Bonferroni correction**.
        * This method adjusts the significance threshold for each predictor based on the number of comparisons.
        * The steps of the Holm-Bonferroni correction are:
            - Sort the p-values from smallest to largest: 
            $$
            p_1 \\leq p_2 \\leq \\dots \\leq p_m
            $$
            - For each p-value, calculate the adjusted threshold using $$\\alpha$$ (significance level 0.05), $$m$$ (total number of tests), $$i$$ (index of the p-value in the sorted list).
            $$
            \\alpha_{\\text{adjusted}} = \\frac{\\alpha}{m - i + 1}
            $$
        * Compare each p-value to its corresponding threshold, and reject the null hypothesis if: 
        $$
        p_i < \\alpha_{\\text{adjusted}}
        $$

    3. **Final Selection**:
        * Predictors are considered significant if their adjusted p-values remain below the corresponding Holm-Bonferroni threshold.
        * This approach ensures that only the most informative predictors are retained while controlling for false discoveries.

    This procedure helps in refining our model by retaining only the variables that add the most value to predicting the target outcome.
''', mathjax=True),

    best_predictors_table,

    html.H3("Final features chosen:",
            style={'text-align': 'left', 'color': '#293241'}),

    dcc.Markdown('''
    $$\\texttt{ABDOMEN}$$ and $$\\texttt{AGE}$$ are the statistically significant feature according to the holm-bonferroni corrected goodness of fit test.
    Therefore, we now fit a multiple linear regression model with these features.
''', mathjax=True),

    html.Div([
        # Previous Page button
        dcc.Link('Go to Previous Page', href='/third_page.data_cleaning_imputation_description', 
                 style={
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
                    'boxShadow': '3px 3px 5px rgba(0, 0, 0, 0.2)'}),

        # Next Page button
        dcc.Link('Go to Next Page', href='/fifth_page.mlr_description', style={
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
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '20px'})
])
