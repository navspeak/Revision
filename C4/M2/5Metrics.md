# Regression Metrics — From First Principles

All metrics answer one question: **how wrong is the model?**

They build on each other logically. Each one fixes a problem with the previous one.

---

## Dataset

| Student | Hours (x) | Score (y) | Predicted (ŷ) | Residual (y − ŷ) |
|---------|-----------|-----------|--------------|-----------------|
| A | 1 | 52 | 51.6 | +0.4 |
| B | 2 | 58 | 58.3 | −0.3 |
| C | 3 | 65 | 65.0 | 0.0 |
| D | 4 | 71 | 71.7 | −0.7 |
| E | 5 | 79 | 78.4 | +0.6 |

**Model:** ŷ = 44.9 + 6.7 × Hours
**Mean of y:** ȳ = (52+58+65+71+79) / 5 = **65**

---

## Step 1 — Mean Error (ME)

The most obvious idea: just average the residuals.

```
ME = Σ(yᵢ − ŷᵢ) / n
   = (0.4 + (−0.3) + 0.0 + (−0.7) + 0.6) / 5
   = 0.0 / 5
   = 0.0
```

**Problem:** Positive and negative errors cancel out. A model that is wildly wrong in both directions still gets ME = 0. Useless as a metric.

**Fix:** Get rid of the sign.

---

## Step 2 — MAE (Mean Absolute Error)

Take the absolute value of each residual before averaging.

```
MAE = Σ|yᵢ − ŷᵢ| / n

|residuals| = |0.4|, |−0.3|, |0.0|, |−0.7|, |0.6|
            =  0.4,   0.3,   0.0,   0.7,   0.6

MAE = (0.4 + 0.3 + 0.0 + 0.7 + 0.6) / 5
    = 2.0 / 5
    = 0.40
```

On average the model is off by **0.40 score points**.

**Problem:** Treats all errors equally — a small error and a large error contribute proportionally. Does not penalise large mistakes more. Also, absolute value is not differentiable at 0 (harder to use in calculus/gradient descent).

**Fix:** Square the errors instead.

---

## Step 3 — SSE (Sum of Squared Errors)

Square each residual and sum them all up.

```
SSE = Σ(yᵢ − ŷᵢ)²

residuals²:  0.4² = 0.16
            (−0.3)² = 0.09
             0.0²  = 0.00
            (−0.7)² = 0.49
             0.6²  = 0.36

SSE = 0.16 + 0.09 + 0.00 + 0.49 + 0.36 = 1.10
```

Squaring does two things:
- Removes the sign (like absolute value)
- Penalises large errors more heavily (an error of 2 contributes 4×, not 2×)

**This is what OLS minimises** — it finds the β₀ and β₁ that produce the smallest SSE.

**Problem:** SSE grows with dataset size. 1000 rows will have a bigger SSE than 5 rows even if both models fit equally well. Hard to compare across datasets.

**Fix:** Divide by n.

---

## Step 4 — MSE (Mean Squared Error)

Divide SSE by the number of observations.

```
MSE = SSE / n
    = 1.10 / 5
    = 0.22
```

Now comparable across datasets of different sizes.

**This is what gradient descent minimises** (since n is a constant, minimising MSE = minimising SSE — same best line).

**Problem:** Units are squared (score²). Hard to interpret — what does 0.22 score² mean?

**Fix:** Take the square root.

---

## Step 5 — RMSE (Root Mean Squared Error)

```
RMSE = √MSE
     = √0.22
     = 0.47
```

Back in the **original units** (score points). The model is off by about **0.47 score points** on average.

**Thumb rule:** RMSE < std dev of y → model beats naïve mean prediction.

```
std dev of y = √(Σ(y − ȳ)² / n)

(y − ȳ): −13, −7, 0, +6, +14
(y − ȳ)²: 169, 49, 0, 36, 196  →  sum = 450

std dev = √(450/5) = √90 = 9.49

RMSE (0.47) << std dev (9.49)  →  model is far better than just predicting the mean ✓
```

**Problem:** 0.47 score points — is that good or bad? Depends on the scale of y. Doesn't tell you the error as a proportion of the actual value.

**Fix:** Express as a percentage.

---

## Step 6 — MAPE (Mean Absolute Percentage Error)

Divide each absolute error by the actual value, then average and multiply by 100.

```
MAPE = mean(|yᵢ − ŷᵢ| / yᵢ) × 100

Student A: |0.4| / 52  = 0.0077  →  0.77%
Student B: |0.3| / 58  = 0.0052  →  0.52%
Student C: |0.0| / 65  = 0.0000  →  0.00%
Student D: |0.7| / 71  = 0.0099  →  0.99%
Student E: |0.6| / 79  = 0.0076  →  0.76%

MAPE = (0.77 + 0.52 + 0.00 + 0.99 + 0.76) / 5 = 0.61%
```

Model is off by **0.61% on average** — immediately interpretable, regardless of scale.

**Thumb rule:** MAPE < 10% → good; 10–20% → acceptable; > 20% → poor.

**Caution:** Breaks down when y is close to 0 (division by near-zero explodes).

---

## Step 7 — SST (Total Sum of Squares)

Now shift focus: instead of "how wrong is the model", ask **"how much variance is there in y to explain?"**

### What is ȳ?

ȳ is the **mean of all actual y values** — not a random guess, but the most informed prediction you can make **without using any features**.

If someone says "predict a student's score but you can't use their study hours" — your best single guess for everyone is the average score.

```
ȳ = (52 + 58 + 65 + 71 + 79) / 5 = 65
```

Predict **65 for every student**, regardless of how much they studied. This is the **baseline model**.

| Student | Actual y | ȳ prediction | Error |
|---------|----------|-------------|-------|
| A | 52 | 65 | −13 |
| B | 58 | 65 | −7 |
| C | 65 | 65 | 0 |
| D | 71 | 65 | +6 |
| E | 79 | 65 | +14 |

SST measures the total spread of actual y values around ȳ — the total error if you just predicted the mean every time.

```
SST = Σ(yᵢ − ȳ)²        ȳ = 65

(y − ȳ): 52−65=−13,  58−65=−7,  65−65=0,  71−65=+6,  79−65=+14
(y − ȳ)²:     169,        49,        0,        36,        196

SST = 169 + 49 + 0 + 36 + 196 = 450
```

SST = 450 — the total error of the dumb baseline. Your model must beat this to be useful.

---

## Step 8 — SSR (Sum of Squares Regression)

SSR is the variance **explained** by the model — how much of SST the model accounts for.

It measures how far the **predictions** move away from the mean. If the model has learned something useful, its predictions will spread away from ȳ toward the actual values.

| Student | ŷ (predicted) | ȳ | ŷ − ȳ | (ŷ − ȳ)² |
|---------|--------------|---|-------|----------|
| A | 51.6 | 65 | −13.4 | 179.56 |
| B | 58.3 | 65 | −6.7 | 44.89 |
| C | 65.0 | 65 | 0.0 | 0.00 |
| D | 71.7 | 65 | +6.7 | 44.89 |
| E | 78.4 | 65 | +13.4 | 179.56 |

```
SSR = 179.56 + 44.89 + 0.00 + 44.89 + 179.56 = 448.90
```

**Relationship:**

```
SST  =  SSR  +  SSE
450  =  448.90 + 1.10   ✓

SST  = total variance in y
SSR  = variance explained by the model
SSE  = variance left unexplained (residuals)
```

---

## Step 9 — R² (R-Squared)

R² is the proportion of total variance explained by the model.

```
R² = SSR / SST
   = 448.90 / 450
   = 0.998

or equivalently:

R² = 1 − (SSE / SST)
   = 1 − (1.10 / 450)
   = 1 − 0.0024
   = 0.998
```

**The model explains 99.8% of the variance in scores.** The remaining 0.2% is unexplained noise.

In other words: R² measures **how much better your model is than just guessing the mean**.

```
R² = 0   → your model is no better than guessing ȳ for everyone
R² = 1   → your model is perfect
R² = 0.9 → your model reduced 90% of the error that ȳ would have made
```

| R² | Meaning |
|----|---------|
| 1.0 | Perfect — model explains all variance |
| 0.998 | Excellent — 99.8% explained |
| 0.6 | Moderate — 40% still unexplained |
| 0.0 | No better than predicting ȳ every time |
| < 0 | Worse than predicting the mean |

---

## Two Types of Metrics

These metrics fall into two distinct groups — each answers a different question:

| Type | Question | Metrics |
|------|----------|---------|
| **Explanation** | How well does the model explain the variation in the data? | R², Adjusted R² |
| **Prediction** | How far are predictions from actual values? | MAE, MSE, RMSE, MAPE |

**Explanation metrics** look at the big picture — does the model capture the pattern?
**Prediction metrics** look at individual errors — how wrong is each prediction?

A model can have a high R² (explains the pattern well) but still have a large RMSE (individual predictions are off). Keeping both in view gives a complete picture of model performance.

> The same loss functions used during training (SSE, MSE) are the starting point for evaluation — training minimises them, evaluation measures them on new data.

---

## All Metrics at a Glance

| Metric | Type | Formula | Value | Interpretation |
|--------|------|---------|-------|----------------|
| ME | — | Σ(y−ŷ)/n | 0.00 | Useless — errors cancel |
| MAE | Prediction | Σ\|y−ŷ\|/n | 0.40 | Off by 0.40 score pts on avg |
| SSE | — | Σ(y−ŷ)² | 1.10 | Total squared error; OLS minimises this |
| MSE | Prediction | SSE/n | 0.22 | Normalised squared error; gradient descent minimises this |
| RMSE | Prediction | √MSE | 0.47 | Off by 0.47 score pts (same units as y) |
| MAPE | Prediction | mean(\|y−ŷ\|/y)×100 | 0.61% | Off by 0.61% of actual value |
| SST | — | Σ(y−ȳ)² | 450 | Total variance in y (baseline) |
| SSR | — | Σ(ŷ−ȳ)² | 448.90 | Variance explained by model |
| R² | Explanation | SSR/SST | 0.998 | 99.8% of variance explained |

---

## sklearn Functions

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, r2_score
import numpy as np

mae  = mean_absolute_error(y_true, y_pred)           # MAE
mse  = mean_squared_error(y_true, y_pred)            # MSE
rmse = np.sqrt(mean_squared_error(y_true, y_pred))   # RMSE — no built-in, wrap with √
mape = mean_absolute_percentage_error(y_true, y_pred) * 100  # MAPE — sklearn returns 0–1, multiply by 100 for %
r2   = r2_score(y_true, y_pred)                      # R²

# Adjusted R² — no built-in, calculate manually
n, p = X_test.shape
adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

# SSE, MSE, SST, SSR — no built-in functions
sse = sum((y_true - y_pred) ** 2)
sst = sum((y_true - y_true.mean()) ** 2)
ssr = sst - sse
```

| Metric | sklearn function | Note | Formula |
|--------|-----------------|------|---------|
| MAE | `mean_absolute_error()` | Direct | Σ\|yᵢ − ŷᵢ\| / n |
| MSE | `mean_squared_error()` | Direct | Σ(yᵢ − ŷᵢ)² / n |
| SSE (from MSE) | `mean_squared_error() × len(y)` | MSE × n — NOT MSE² | Σ(yᵢ − ŷᵢ)² = MSE × n |
| RMSE | `np.sqrt(mean_squared_error())` | No dedicated function | √(Σ(yᵢ − ŷᵢ)² / n) |
| MAPE | `mean_absolute_percentage_error() × 100` | Returns fraction — multiply by 100 for % | mean(\|yᵢ − ŷᵢ\| / yᵢ) × 100 |
| R² | `r2_score()` | Direct | 1 − SSE/SST = SSR/SST |
| Adj R² | Manual formula | No built-in | 1 − (1 − R²) × (n−1) / (n−p−1) |
| SSE | Manual formula | No built-in | Σ(yᵢ − ŷᵢ)² |
| SST | Manual formula | No built-in | Σ(yᵢ − ȳ)² |
| SSR | Manual formula | No built-in | SST − SSE = Σ(ŷᵢ − ȳ)² |

---

## The Logical Chain

```
Mean Error → errors cancel → fix with |absolute value| → MAE
                           → fix with squaring        → SSE → ÷n → MSE → √ → RMSE
                                                                  → ÷y  → MAPE

How much variance is there?  → SST
How much did the model explain? → SSR = SST − SSE
What fraction was explained?    → R² = SSR / SST
```
