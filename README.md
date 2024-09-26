# Body Fat Study

## Introduction

Accurate measurement of body fat is inconvenient/costly and it is desirable to have easy methods of estimating body fat that are not inconvenient/costly. In this project, we come up with a simple, robust, and accurate model (i.e. “rule-of-thumb”) to estimate percentage of body fat using clinically available measurements. Our “rule-of-thumb” will be based on a real data set of *252* men with measurements of their percentage of body fat and various body circumference measurements.

## About the Dataset

A variety of popular health books suggest that the readers assess their health, at least in part, by estimating their percentage of body fat. In Bailey (1994), for instance, the reader can estimate body fat from tables using their age and various skin-fold measurements obtained by using a caliper. Other texts give predictive equations for body fat using body circumference measurements (e.g. abdominal circumference) and/or skin-fold measurements. See, for instance, Behnke and Wilmore (1974), pp. 66-67; Wilmore (1976), p. 247; or Katch and McArdle (1977), pp. 120-132).

Percentage of body fat for an individual can be estimated once body density has been determined. Folks (e.g. Siri (1956)) assume that the body consists of two components - lean body tissue and fat tissue. Letting:

* $D=$ Body Density ($\text{gm}/\text{cm}^3$)
* $A=$ Proportion of Lean Body Tissue
* $B=$ Propoertion of Fat Tissue ($A+B=1$)
* $a=$ Density of Lean Body Tissue ($\text{gm}/\text{cm}^3$)
* $b=$ Desntiy of Fat Tissue ($\text{gm}/\text{cm}^3$)

we have:

$$D = \frac{1}{(A/a) + (B/b)}$$

Solving for $B$, we find:

$$B=\frac{1}{D} \times \bigg[\frac{ab}{(a-b)}\bigg] - \bigg[\frac{b}{a-b}\bigg]$$

Using the estimes $a=1.10\;\text{gm}/\text{cm}^3$ and $b=0.90\;\text{gm}/\text{cm}^3$  (see Katch and McArdle (1977), p. 111 or Wilmore (1976), p. 123) we come up with "Siri's equation":

$$\text{Percentage of Body Fat (i.e. 100 $\times B$)}=\frac{495}{D}-450$$
