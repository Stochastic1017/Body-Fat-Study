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

Using the estimes $a=1.10\text{ gm}/\text{cm}^3$ and $b=0.90\text{ gm}/\text{cm}^3$  (see Katch and McArdle (1977), p. 111 or Wilmore (1976), p. 123) we come up with "Siri's equation":

$$\text{Percentage of Body Fat (i.e. 100 $\times B$)}=\frac{495}{D}-450$$

The technique of underwater weighing "computes body volume as the difference between body weight measured in air and weight measured during water submersion. 
In other words, body volume is equal to the loss of weight in water with the appropriate
temperature correction for the water's density" (Katch and McArdle (1977), p. 113).

Using this technique:
                 
$$\\text{Body Density} = \\frac{\\text{WA}}{[(\\text{WA} - \\text{WW})/\\text{c.f.} - \\text{LV}]}$$

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
