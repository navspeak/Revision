# Addressing Challenges in Linear Regression

A dataset may face several issues that make it unsuitable for a linear model. Some can be mitigated; others require rethinking the approach.

---

## 1. Scaling and Interpretability

**Problem:** Coefficients in LR are only comparable when predictors are on the **same scale**.

- `Alone Time Hours` ranges 0–10; `Extrovert` is 0 or 1 → raw coefficients can't be compared
- A large coefficient just means the predictor has a small numeric range, not that it matters more

**Fix: Min-Max Scaling**

```
x_scaled = (x - x_min) / (x_max - x_min)   →  maps all values to [0, 1]
```

```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
```

**Key point:** Scaling does NOT change model performance (R², RMSE stay the same). It only changes coefficient magnitude, making them comparable.

| After scaling | Interpretation |
|---------------|----------------|
| Extrovert: 6.19 | Extrovert has the biggest effect on friend circle size |
| Alone Time: -1.87 | Second strongest (negative) |
| Social Events: 0.29 | Weakest |

---

## 2. Multicollinearity

**Problem:** Two or more predictors are highly correlated → they carry redundant information.

**Symptoms:**
- Coefficients change wildly when you add/remove a predictor
- Individual p-values are high even though overall R² is good
- Hard to isolate the effect of a single predictor

### 2a. Correlation-Based Removal

Iterative heuristic: compute sum of absolute correlations for each feature; drop the one with highest sum; repeat.

```python
correlation_matrix = df.corr()
sum_abs_corr = correlation_matrix.abs().sum()  # Diagonal (self-corr) included but same for all
predictor_to_drop = sum_abs_corr.idxmax()
```

Watch R² as you drop — stop when R² drops sharply.

### 2b. Adjusted R²

**Problem with R²:** It always increases when you add features, even useless ones.

```
Adj R² = 1 - (1 - R²) × (n - 1) / (n - p - 1)
```

- n = number of samples, p = number of predictors
- Penalises adding features that don't improve the model
- Use Adj R² when **comparing models with different numbers of features**

```python
def adjusted_r2(r2, n, p):
    return 1 - (1 - r2) * (n - 1) / (n - p - 1)
```

### 2c. Variance Inflation Factor (VIF)

**What it measures:** How much of predictor Xᵢ's variance is explained by the other predictors.

```
VIF_i = 1 / (1 - R²_i)
```

where R²_i = R² from regressing Xᵢ on all other predictors.

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
```

| VIF | Interpretation |
|-----|----------------|
| = 1 | No correlation with other predictors |
| 1–5 | Mild, generally acceptable |
| 5–10 | Moderate — potential multicollinearity |
| ≥ 10 | Severe — consider dropping or combining |

Fix: drop the highest-VIF predictor and recalculate.

### 2d. Recursive Feature Elimination (RFE)

Systematic wrapper method: fit model → rank features by importance → drop least important → repeat.

```python
from sklearn.feature_selection import RFE

rfe = RFE(estimator=LinearRegression(), n_features_to_select=5)
rfe.fit(X, y)
X_selected = X[X.columns[rfe.support_]]
```

Compare R² and Adj R² as number of features decreases → pick the "elbow" point.

---

## 3. Categorical Predictors and VIF

**Problem:** One-hot encoded dummies are structurally correlated (they partition the same variable) → VIF artificially inflates.

**Rule:** Always use `drop_first=True` with `pd.get_dummies()` to avoid the **dummy variable trap** (perfect multicollinearity where dummies sum to 1).

```python
dummies = pd.get_dummies(df['day'], prefix='day', drop_first=True)
X = pd.concat([X_numeric, dummies], axis=1).astype(float)
```

**Interpreting VIF with categories:**
- High VIF on dummy variables is expected structural correlation — not a problem to fix
- The concern is numeric predictors with high VIF
- Assess categorical predictors as a group, not as individual dummy columns

---

## 4. Overfitting

**Problem:** Model learns noise in training data → fits training well but generalises poorly.

**Signs:**
- Train R² >> Test R² (or Train MSE << Test MSE)
- Adding more features keeps improving train score but hurts test score

**Causes:**
- Too many features relative to sample size (high p/n ratio)
- Irrelevant features — model fits their noise

**Fixes:**
1. Remove irrelevant features (use RFE, VIF, p-values)
2. Regularisation (Lasso / Ridge — covered in M4)
3. Collect more data

```python
# Always evaluate on test set, not just train
model.fit(X_train, y_train)
train_r2 = r2_score(y_train, model.predict(X_train))
test_r2  = r2_score(y_test,  model.predict(X_test))
# If train_r2 >> test_r2 → overfitting
```

**Coefficient sanity check:** If an irrelevant feature has a large coefficient, the model is fitting noise.

---

## 5. Heteroscedasticity

**Problem:** Residuals have non-constant variance — typically, errors grow larger as fitted values increase (funnel shape in residual plot).

**Symptom:** Residual vs Fitted plot shows a fan/funnel pattern.

**Why it matters:** Standard errors become biased → p-values and confidence intervals are unreliable.

**Fix: Log-transform the target variable**

```python
y_log = np.log(y)       # Apply before fitting
model.fit(X, y_log)
y_pred_log = model.predict(X)

# After prediction, back-transform
y_pred_original = np.exp(y_pred_log)
```

Good when: target is right-skewed (incomes, prices, production).

**Other transforms:** square-root (√y), Box-Cox (systematic approach to find best power transform).

| Residual pattern | Likely issue | Fix |
|-----------------|--------------|-----|
| Fan/funnel shape | Heteroscedasticity | Log-transform y |
| Curve shape | Non-linearity | Add polynomial features |
| Random scatter | ✓ No issue | None |

---

## 6. Summary — Diagnostic Checklist

| Issue | Check | Fix |
|-------|-------|-----|
| Can't compare coefficients | Are predictors on different scales? | Min-max or standardise X |
| Unstable coefficients | Correlation matrix; VIF > 10? | Drop high-VIF features |
| Too many features | Adj R² drops when removing? | RFE or p-value filtering |
| Overfitting | Train R² >> Test R²? | Remove features; regularise |
| Heteroscedasticity | Funnel shape in residual plot? | Log-transform y |

---

## 7. Python Quick Reference

```python
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import RFE
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Scale
X_scaled = MinMaxScaler().fit_transform(X)

# Adjusted R²
adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

# VIF
vif = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

# RFE
rfe = RFE(LinearRegression(), n_features_to_select=k).fit(X, y)
X_rfe = X[X.columns[rfe.support_]]

# Log-transform target
y_log = np.log(y)
model.fit(X, y_log)
y_pred = np.exp(model.predict(X_new))  # back-transform
```
