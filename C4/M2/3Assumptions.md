# Assumptions of Linear Regression

---

## SSE vs MSE

```
SSE = Σ(yᵢ − ŷᵢ)²          ← sum of squared errors (total)
MSE = Σ(yᵢ − ŷᵢ)² / n      ← SSE divided by number of observations
```

**MSE = SSE / n**

### Why divide by n?

SSE grows with dataset size — 1000 rows will naturally have a bigger SSE than 5 rows, even if both models fit equally well. MSE normalises it so you can compare models across different dataset sizes.

### Concrete example (5-student dataset)

| Student | Residual | Residual² |
|---------|----------|-----------|
| A | +0.4 | 0.16 |
| B | −0.3 | 0.09 |
| C | 0.0 | 0.00 |
| D | −0.7 | 0.49 |
| E | +0.6 | 0.36 |
| | **SSE** | **1.10** |

```
SSE  = 1.10
MSE  = 1.10 / 5 = 0.22
RMSE = √0.22 = 0.47  ← back in original units (score points)
```

### The family

| Metric | Formula | Notes |
|--------|---------|-------|
| SSE | Σ(y − ŷ)² | Used in OLS to find best line |
| MSE | SSE / n | Used as loss in gradient descent |
| RMSE | √MSE | Interpretable — same units as y |

OLS minimises SSE. Gradient descent minimises MSE. Since n is a constant, minimising one is the same as minimising the other — same best line either way.

---

Linear regression produces reliable results only when 5 assumptions hold. Violating them doesn't break the math — it breaks the predictions and interpretations.

**Dataset used throughout:** 5 students, Study Hours → Exam Score

| Student | Study Hours (x) | Score (y) |
|---------|----------------|-----------|
| A | 1 | 52 |
| B | 2 | 58 |
| C | 3 | 65 |
| D | 4 | 71 |
| E | 5 | 79 |

Fitted model: **Score = 44.9 + 6.7 × Hours**

| Student | x | y | ŷ | Residual (y − ŷ) |
|---------|---|---|---|-----------------|
| A | 1 | 52 | 51.6 | +0.4 |
| B | 2 | 58 | 58.3 | −0.3 |
| C | 3 | 65 | 65.0 | 0.0 |
| D | 4 | 71 | 71.7 | −0.7 |
| E | 5 | 79 | 78.4 | +0.6 |

All 5 assumptions hold for this data. Below, each assumption is explained — and then shown violated.

---

## 1. Linearity

**What it means:** The relationship between X and y is a straight line.

**Holds ✓ — our dataset:**
```
Score
 80 |              E
 75 |          D
 70 |      C
 65 |  B
 60 | A
    └──────────────── Hours
      1   2   3   4   5
Points fall on a straight line → linearity holds
```

**Violated ✗ — scores accelerate (quadratic pattern):**

| x | y (actual) | ŷ (linear fit) | Residual |
|---|-----------|----------------|----------|
| 1 | 50 | 51.6 | −1.6 |
| 2 | 55 | 58.3 | −3.3 |
| 3 | 65 | 65.0 | 0.0 |
| 4 | 80 | 71.7 | +8.3 |
| 5 | 100 | 78.4 | +21.6 |

Residuals go: negative → near zero → large positive → **curve shape, not random**.
The line underfits the ends. A straight line cannot capture this.

**How to check — two tests:**

**Test 1 — Scatter plot of X vs y (before fitting):**
```
Holds ✓                          Violated ✗
Score                            Score
 80 |                E           100 |                E
 75 |           D                 85 |           D
 70 |      C                      65 |      C
 65 |  B                          55 |  B
 60 | A                           50 | A
    └──────── Hours                  └──────── Hours
Points in a straight line        Points curve upward
```

**Test 2 — Residuals vs Fitted plot (after fitting):**

If linearity holds → residuals scatter randomly around 0, no pattern.
If violated → residuals show a curve pattern.

```
Holds ✓ — random scatter:        Violated ✗ — curve pattern:

+1 | *              *            +20 |               *
 0 |     *                       +10 |          *
-1 |          *  *                 0 |     *
   └────────────────── ŷ          -2 | * *
                                    └────────────────── ŷ

No pattern → linearity holds     Starts negative, ends strongly
                                 positive → linearity violated
```

The residual curve tells you the model is **systematically wrong** — underpredicting at the ends means the true relationship curves.

**Fix:**
```python
# Option 1 — add polynomial feature
df['Hours²'] = df['Hours'] ** 2
model.fit(df[['Hours', 'Hours²']], y)

# Option 2 — log-transform X
df['log_Hours'] = np.log(df['Hours'])
model.fit(df[['log_Hours']], y)
```

---

## 2. Independence

**What it means:** Each observation is collected independently. One data point does not influence another.

**Holds ✓ — our dataset:**
5 different students sitting separate exams. Student A's score has no bearing on Student B's.

**Violated ✗ — time series example:**

Suppose instead of students, we measure the same person's score across 5 consecutive days of study:

| Day | Hours | Score |
|-----|-------|-------|
| 1 | 1 | 52 |
| 2 | 2 | 59 |
| 3 | 3 | 67 |
| 4 | 4 | 76 |
| 5 | 5 | 86 |

Day 5's score is influenced by day 4 (fatigue, cumulative learning). Observations are **not independent** — each one carries memory of the previous.

**How to check:** Domain knowledge (is this time-series or panel data?); Durbin-Watson test on residuals.

**Fix:** Use time-series models (ARIMA); add lag features.

---

## 3. Homoscedasticity

**What it means:** Residuals have **constant variance** across all fitted values. The spread of errors should be the same whether ŷ is small or large.

**Holds ✓ — our dataset:**
```
Residuals vs Fitted:

+1 |      A              E
 0 |           C
-1 |    B         D

Residuals are small and similar in size throughout → homoscedastic ✓
```

**Violated ✗ — errors grow as x increases (heteroscedastic):**

| x | y | ŷ | Residual |
|---|---|---|----------|
| 1 | 52 | 51.6 | +0.4 |
| 2 | 57 | 58.3 | −1.3 |
| 3 | 61 | 65.0 | −4.0 |
| 4 | 66 | 71.7 | −5.7 |
| 5 | 70 | 78.4 | −8.4 |

```
Residuals vs Fitted:

 0 | *
-2 |    *
-4 |       *
-6 |           *
-8 |               *

Funnel shape — errors grow larger as fitted value increases → heteroscedastic ✗
```

**Why it matters:** Standard errors of coefficients become unreliable → p-values and confidence intervals are wrong even if R² looks fine.

**In plain English — what does homoscedasticity mean?**

Homo = same, scedasticity = spread. Literally: **"same spread"**.

> No matter what value the model predicts, the errors should be roughly the same size.

```
Homoscedastic ✓                  Heteroscedastic ✗
Predict 50 → off by ±2           Predict 50 → off by ±1
Predict 65 → off by ±2           Predict 65 → off by ±5
Predict 80 → off by ±2           Predict 80 → off by ±12
Consistent throughout            Errors balloon as ŷ grows
```

**What causes heteroscedasticity?**

1. **Income / price data — natural multiplicative growth**
   Rich people's spending varies more than poor people's. Variation is proportional to the level of y — almost always heteroscedastic.
   ```
   Low income  → small errors
   High income → large errors
   ```

2. **Missing an important variable**
   If a feature that explains variance is left out, its effect lands in the residuals. If that feature correlates with ŷ, errors grow with ŷ.
   ```
   Predicting house price using only Area, ignoring Location.
   Small houses → small price, small error
   Large houses → large price, large error (location effect hidden in residual)
   ```

3. **Data spans very different groups**
   ```
   Predicting salary for interns + CEOs in the same model.
   Intern salaries: ₹3L–₹5L  → tight cluster, small errors
   CEO salaries:    ₹50L–₹5Cr → huge spread, large errors
   ```

4. **Outliers at one end of the scale**
   A few extreme values at the high end cause errors to cluster and grow there.

**The pattern to recognise:**
```
Errors grow as ŷ grows   → errors proportional to prediction
Errors fan out            → missing variable correlated with ŷ
Errors cluster in a group → different populations in one model
```

**How to check:** Residuals vs fitted plot — look for funnel/fan shape.

**Fix:** Log-transform the target variable (y → log y) — compresses large values, equalising the spread.

---

## 4. Normality of Residuals

**What it means:** Residuals should be approximately normally distributed — most near zero, symmetrically tapering off.

**Holds ✓ — our dataset:**
Residuals: [+0.4, −0.3, 0.0, −0.7, +0.6]
```
Small, scattered around 0, roughly symmetric → approximately normal ✓
```

**Violated ✗ — right-skewed residuals:**

| Student | Residual |
|---------|----------|
| A | +0.2 |
| B | +0.1 |
| C | +0.3 |
| D | +8.5 |
| E | +12.0 |

```
Histogram:
████████  ← most errors near 0
    █     ← one large positive outlier
        █ ← another large positive outlier

Right-skewed, not bell-shaped → normality violated ✗
```

**Why it matters:** Confidence intervals and hypothesis tests (p-values) assume normally distributed errors. Skewed residuals make these unreliable.

**How to check:** Histogram of residuals; QQ plot (points should fall on a diagonal line).

**Fix:** Log-transform y; remove outliers; use robust regression.

---

## 5. No Multicollinearity

**What it means:** The predictor features should not be highly correlated with each other.

This assumption only applies to **Multiple Linear Regression** (more than one feature).

**Holds ✓ — independent features:**

| Student | Hours (x₁) | Sleep (x₂) | Score (y) |
|---------|-----------|-----------|-----------|
| A | 1 | 8 | 52 |
| B | 2 | 7 | 58 |
| C | 3 | 6 | 65 |
| D | 4 | 8 | 71 |
| E | 5 | 7 | 79 |

Hours and Sleep have no clear pattern together → low correlation → no multicollinearity ✓

**Violated ✗ — features move together:**

| Student | Hours (x₁) | Pages Read (x₂) | Score (y) |
|---------|-----------|----------------|-----------|
| A | 1 | 10 | 52 |
| B | 2 | 20 | 58 |
| C | 3 | 30 | 65 |
| D | 4 | 40 | 71 |
| E | 5 | 50 | 79 |

x₂ = 10 × x₁ exactly. They carry **identical information**. The model cannot separate the effect of hours from pages — coefficients become unstable and meaningless.

```
Correlation(x₁, x₂) = 1.0  ← perfect multicollinearity
```

**Why it matters:** Coefficients become unreliable — small changes in data cause huge swings in β. Hard to interpret which feature actually drives y.

**How to check:** Correlation matrix; VIF (Variance Inflation Factor) — VIF ≥ 10 is a problem.

**Fix:** Drop one of the correlated features; use PCA to combine them; apply Ridge regression.

---

## Summary

| # | Assumption | Check | Violation looks like | Fix |
|---|-----------|-------|---------------------|-----|
| 1 | Linearity | Scatter plot; residuals vs fitted | Curved pattern in residuals | Add x², log-transform X |
| 2 | Independence | Domain knowledge; Durbin-Watson | Time-series data; clustered data | Time-series models; lag features |
| 3 | Homoscedasticity | Residuals vs fitted plot | Funnel shape — errors grow with ŷ | Log-transform y |
| 4 | Normality of residuals | Histogram; QQ plot | Skewed or heavy-tailed residuals | Log-transform y; remove outliers |
| 5 | No multicollinearity | Correlation matrix; VIF | VIF ≥ 10; coefficients unstable | Drop feature; Ridge regression |

> Assumptions 1–4 are about the relationship between X and y.
> Assumption 5 is about the relationship between features — only relevant when you have more than one.
