# Body Fat Percentage Prediction using Fine-Tuned Multiple Linear Regression Model

## Web-app Link

We’ve developed an interactive web app that not only allows users to easily estimate their body fat percentage but also provides a detailed walkthrough of how the model was created. The app offers an intuitive interface, making it accessible for anyone to use. All the code and resources for the web app are available in our GitHub repository, offering full transparency and flexibility for those interested in exploring or extending the project.

link: https://uw-madison-stat-628-body-fat-study.onrender.com/ 

## Introduction

The rising prevalence of health issues like obesity and cardiovascular disease has increased the focus on body composition analysis, with body fat percentage serving as a key health indicator. This project analyzes a dataset of physical measurements to develop a predictive model for estimating body fat percentage. After data cleaning and feature selection to address multicollinearity, a multiple linear
regression model was built. This report outlines the steps of data preprocessing, model fitting, and evaluation of the model’s performance.

## Data Cleaning

To identify observations with implausible values, we use a prior body fat estimation model to flag inconsistencies.

> Healthy percentage body fat ranges: an approach for developing guidelines based on body mass index. Gallagher, Dympna et al. The American Journal of Clinical Nutrition, Volume 72, Issue 3, 694 - 701.

If the absolute difference between the model estimate and the observed data exceeds 11%, the observation is flagged as an anomaly and corrected using the model estimate.

## Multiple Linear Regression Model

We selected a multiple linear regression (MLR) model for its simplicity, interpretability, and academic rigor. MLR provides intuitive coefficients that are easily understood by non-experts, while allowing for robust feature selection through well-established statistical methods. Its balance of simplicity and
explanatory power makes it an ideal choice for this analysis.

## Feature Selection Procedure

We first remove features that are costly, redundant, or irrelevant for body fat estimation, retaining $\texttt{AGE}$, $\texttt{ADIPOSITY}$, $\texttt{ABDOMEN}$, $\texttt{CHEST}$, and $\texttt{THIGH}$. We then apply an ANOVA-based stepwise selection with Holm-Bonferroni correction to control for FWER, identifying AGE and ABDOMEN as the most significant predictors. Finally, we test feature combinations by fitting models and comparing R-squared, RMSE, and mean VIF. Models with more than two features showed excessive multicollinearity, while $\texttt{AGE}$ and $\texttt{ABDOMEN}$ provided the best trade-off between low RMSE and an acceptable mean VIF.

$$\hat{\texttt{BODYFAT}} = -31.8595 + (0.0554) \cdot \texttt{AGE} + (0.5281) \cdot \texttt{ABDOMEN}$$

## Model Diagnostics

After fitting the MLR model with BODYFAT as the response and AGE and ABDOMEN as predictors, one point outside Cook’s distance was removed. Linearity was assessed through residuals vs. fitted plots, confirming the assumption, and a Q-Q plot showed residuals were approximately normal, with minor deviations at the tails. The model achieved an R-squared of $0.6592$ and RMSE of $4.3787$ on test data, with all predictors statistically significant.

## Model Performance

### Strengths:
1. Simple and practical with only two easily measurable predictors.
2. Intuitive and easily interpretable coefficients. Good balance between predictive power and simplicity (R-squared = 0.6592).
3. Based on rigorous feature selection and diagnostics.

### Weaknesses:
1. Moderate predictive power, with potential for improvement.
2. Minor deviations in residuals at the tails suggest a slightly imperfect fit.

## Conclusion/Discussion 

This report analyzed a body fat dataset to predict body fat percentage based on physical measurements. After data cleaning and feature selection, we opted for a linear regression model for its interpretability and adherence to key assumptions. AGE and ADIPOSITY were significant predictors, with meaningful coefficients. Diagnostic checks confirmed model validity, though minor normality deviations and outliers were noted. While the model provides reliable predictions, further refinement or exploring more complex models could address non-linearities and subgroup variations.

## References

* Casella, G. and Berger, R.L. (2002) Statistical Inference. 2nd Edition, Duxbury Press, Pacific Grove.

* Christensen, R. (2019). Plane answers to complex questions: The theory of linear models (5th ed.). Springer.
  
* D. A. Belsley, K. Kuh and R. E. Welsch. Regression diagnostics: Identifying influential data and sources of collinearity. John Wiley & Sons, New York, 1980, pp. xv + 292, ISBN 0-471-05856-4.
  
* Gallagher, Dympna et al. Healthy percentage body fat ranges: an approach for developing guidelines based on body mass index. The American Journal of Clinical Nutrition, Volume 72, Issue 3, 694 - 701.
  
* Holm, S. (1979). A Simple Sequentially Rejective Multiple Test Procedure. Scandinavian Journal of Statistics, 6(2), 65–70. http://www.jstor.org/stable/4615733

* Wilke, C. (2019). Fundamentals of Data Visualization: A Primer on Making Informative and Compelling Figures. Japan: O’Reilly Media.
