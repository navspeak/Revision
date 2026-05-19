# Linear Regression

---

## 1. What Does Linear Regression Do?

**Goal:** Predict a **continuous numeric output** (y) from one or more input variables (X).

Simple example: predict house price from area (sq ft).

```
Price = β₀ + β₁ × Area
```

This is a straight line through the data. LR finds the **best** line — the one that minimises prediction error.

---

## 2. The Model

### Simple Linear Regression (one feature)

```
ŷ = β₀ + β₁x
```

| Symbol | Name | Meaning |
|--------|------|---------|
| ŷ | Predicted value | Output of the model |
| β₀ | Intercept | Value of ŷ when x = 0 |
| β₁ | Coefficient / Slope | Change in ŷ per unit increase in x |
| x | Feature / Predictor | Input variable |

### Multiple Linear Regression (multiple features)

```
ŷ = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ
```

Each βᵢ captures the effect of xᵢ on ŷ **holding all other variables constant**.

---

## 3. How the Line is Fit — OLS

**Ordinary Least Squares (OLS):** find β₀, β₁ that minimise the sum of squared residuals.

```
Residual (error) = y - ŷ   (actual minus predicted)

Loss = Σ(yᵢ - ŷᵢ)²   ← Sum of Squared Errors (SSE)
```

Why square?
- Prevents positive and negative errors from cancelling
- Penalises large errors more than small ones

The OLS solution is a closed-form formula (no iterative training needed for small data):

```
β = (XᵀX)⁻¹ Xᵀy
```

---

## 4. Assumptions of Linear Regression

LR only works well when these hold. Violating them doesn't break the math but breaks the predictions.

| Assumption | What it means | How to check |
|-----------|--------------|--------------|
| **Linearity** | Relationship between X and y is linear | Scatter plot of X vs y; residual vs fitted plot |
| **Independence** | Observations are independent of each other | Domain knowledge; time-series data often violates this |
| **Homoscedasticity** | Residuals have constant variance across all fitted values | Residual vs fitted plot — should be random scatter, not funnel |
| **Normality of residuals** | Residuals are approximately normally distributed | QQ plot of residuals; histogram of residuals |
| **No multicollinearity** | Features are not highly correlated with each other | Correlation matrix; VIF (Variance Inflation Factor) |

> If linearity is violated → try feature transformation (log, sqrt) or a non-linear model.  
> If homoscedasticity is violated → try log-transforming the target variable.

---

## 5. Interpreting Coefficients

```
ŷ = 50000 + 300 × Area + 20000 × Bedrooms
```

- **β₀ = 50000:** baseline price when Area=0 and Bedrooms=0 (often not meaningful on its own)
- **β₁ = 300:** each additional sq ft adds ₹300 to price, *holding bedrooms constant*
- **β₂ = 20000:** each additional bedroom adds ₹20,000, *holding area constant*

### Cautions

- **Correlation ≠ causation** — a coefficient shows association, not that X causes y
- **Extrapolation** — predictions outside the range of training data are unreliable
- **Multicollinearity** — if two features are highly correlated, coefficients become unstable
- **Scale matters** — coefficients on different scales are not directly comparable without standardisation

---

## 6. Model Evaluation Metrics

### Residual-based Metrics

| Metric | Formula | Units | Notes |
|--------|---------|-------|-------|
| **SSE** | Σ(y - ŷ)² | y² | Total squared error; used by OLS to find best line |
| **MAE** | mean(\|y - ŷ\|) | Same as y | Robust to outliers; easy to interpret |
| **MSE** | SSE / n | y² | Penalises large errors more; used as loss in gradient descent |
| **RMSE** | √MSE | Same as y | Most common; interpretable in original units |
| **MAPE** | mean(\|y-ŷ\|/y)×100 | % | Error as % of actual value |

### Thumb Rules

- RMSE < Std Dev of y → model beats naïve mean prediction
- MAE << Mean of y → errors are small relative to typical value
- MAPE < 10% → good; 10–20% → acceptable; > 20% → poor

### Goodness-of-fit

**R² (R-squared)**

```
R² = 1 - SSR/SST

SSR = Σ(y - ŷ)²   (unexplained variance)
SST = Σ(y - ȳ)²   (total variance)
```

| R² | Interpretation |
|----|---------------|
| 1.0 | Perfect — model explains all variance |
| 0.0 | No better than predicting the mean every time |
| < 0 | Worse than predicting the mean |

> R² always increases when you add more features — even useless ones.  
> Use **Adjusted R²** when comparing models with different numbers of features.

**Adjusted R²**

```
Adj R² = 1 - (1 - R²) × (n - 1) / (n - p - 1)
```

Penalises adding features that don't improve the model.

```python
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_pred)
n, p = X_test.shape
adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
```

---

## 7. sklearn vs statsmodels

| | sklearn | statsmodels |
|--|---------|-------------|
| Purpose | Build and predict | Statistical inference |
| Output | Coefficients, predictions | Full OLS summary: p-values, confidence intervals, F-stat |
| Use when | You want a model to score new data | You want to understand which predictors matter |

```python
# statsmodels — formula API
import statsmodels.formula.api as sm
model = sm.ols('Sales ~ TV + Radio + Newspaper', data=train_df).fit()
print(model.summary())
# P>|t| column: if p < 0.05 → predictor is significant
```

---

## 8. Advertising Dataset — Key Results

Dataset: 200 rows, TV / Radio / Newspaper spend → Sales

| Model | Features | R² (Test) | RMSE (Test) |
|-------|----------|-----------|-------------|
| Simple LR | TV only | ~0.60 | ~3.5 |
| Multiple LR | TV + Radio + Newspaper | ~0.90 | ~1.8 |
| Multiple LR | TV + Radio only | ~0.90 | ~1.8 |

**Newspaper p-value = 0.696** → not significant, dropping it doesn't change R².  
**Residuals** show mild funnel pattern → slight heteroscedasticity.

---

## 9. Python — End-to-End

```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

X = df[['TV', 'Radio', 'Newspaper']]
y = df['Sales']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression().fit(X_train, y_train)

print("Intercept:", model.intercept_)
print("Coefficients:", dict(zip(X.columns, model.coef_)))

y_pred = model.predict(X_test)

mae  = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2   = r2_score(y_test, y_pred)
n, p = X_test.shape
adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

print(f"MAE={mae:.2f}  RMSE={rmse:.2f}  R²={r2:.3f}  Adj R²={adj_r2:.3f}")
```

---

## 10. Strengths and Limitations

| Strengths | Limitations |
|-----------|-------------|
| Simple and interpretable | Assumes linearity |
| Fast to train (closed-form OLS) | Sensitive to outliers (squared loss) |
| Coefficients have clear meaning | Requires assumption checks |
| Good baseline model | Multicollinearity distorts coefficients |
| Builds intuition for all models | Underfits complex patterns |
