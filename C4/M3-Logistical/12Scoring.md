# Scoring APIs — `.score()` and `cross_val_score()`

Two sklearn shortcuts that come up everywhere. Both are about **evaluating** a model.

---

## `.score(X, y)` — One-Line Default Metric

Every sklearn estimator has a `.score()` method that computes a default metric.

```python
model = LinearRegression().fit(X_train, y_train)
score = model.score(X_test, y_test)
```

Equivalent to:

```python
y_pred = model.predict(X_test)
score  = r2_score(y_test, y_pred)
```

The default metric depends on the model type:

| Model | `.score()` returns |
|-------|--------------------|
| Regression (LinearRegression, Ridge, Lasso) | **R²** |
| Classification (LogisticRegression, RandomForest, etc.) | **Accuracy** |
| Clustering (KMeans) | Negative inertia |

If you want a different metric (precision, F1, RMSE), use the explicit function from `sklearn.metrics` instead.

---

## `cross_val_score()` — k-Fold CV in One Call

Runs k-fold cross-validation and returns an array of scores.

```python
from sklearn.model_selection import cross_val_score

model = LinearRegression()
cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
```

What happens under the hood:

```
Split X, y into 5 folds.
For each fold i (1 to 5):
    Train model on the other 4 folds
    Score it on fold i using R²
Return an array of 5 scores
```

### Parameters

| Parameter | Meaning |
|-----------|---------|
| `model` | Unfitted estimator |
| `X, y` | Full data — function splits internally |
| `cv` | Number of folds (default = 5) |
| `scoring` | Metric — `'r2'`, `'accuracy'`, `'f1'`, `'neg_mean_squared_error'`, ... |

> Pass full `X, y` (not `X_train, X_test`) — `cross_val_score` does the splitting itself.

---

## Reading the Output

```python
cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
# array([0.81, 0.85, 0.79, 0.83, 0.80])

print(f'Mean R2: {cv_scores.mean():.3f}')   # 0.816  → how good
print(f'Std  R2: {cv_scores.std():.3f}')    # 0.022  → how stable
```

- **Mean** — your reliable estimate of model performance
- **Std** — stability across folds:

```
Low std (e.g. 0.02)  → consistent → trustworthy estimate
High std (e.g. 0.15) → wildly different per fold → unstable, maybe too little data
```

Always report **both**.

---

## Common `scoring` Values

| Problem | Common scoring strings |
|---------|------------------------|
| Regression | `'r2'`, `'neg_mean_squared_error'`, `'neg_mean_absolute_error'` |
| Binary classification | `'accuracy'`, `'f1'`, `'precision'`, `'recall'`, `'roc_auc'` |
| Multiclass | `'accuracy'`, `'f1_macro'`, `'f1_weighted'` |

> sklearn uses `'neg_mean_squared_error'` (negative) because by convention higher = better. Negate the result to get back to plain MSE.

---

## `.score()` vs `cross_val_score()`

| | `.score()` | `cross_val_score()` |
|-|-----------|--------------------|
| What it does | Score on one set | k-fold CV |
| Returns | One number | Array of k scores |
| Reliable? | Depends on the split | Yes — averaged over k |
| Metric choice | Fixed (default per model) | Configurable via `scoring=` |
| Use when | Quick one-off check | Proper evaluation, tuning |

---

## Maths Involved

### `.score()` for Regression — R²

```
R² = 1 − SSE/SST

SSE = Σ(yᵢ − ŷᵢ)²        ← residual sum of squares
SST = Σ(yᵢ − ȳ)²          ← total sum of squares

ȳ = mean of y
```

**Example:**

```
y      = [10, 20, 30, 40, 50]
ŷ      = [12, 19, 31, 38, 49]
ȳ      = 30

SSE = (10−12)² + (20−19)² + (30−31)² + (40−38)² + (50−49)²
    = 4 + 1 + 1 + 4 + 1 = 11

SST = (10−30)² + (20−30)² + (30−30)² + (40−30)² + (50−30)²
    = 400 + 100 + 0 + 100 + 400 = 1000

R² = 1 − 11/1000 = 0.989
```

### `.score()` for Classification — Accuracy

```
Accuracy = (# correct) / (total) = Σ 1[yᵢ = ŷᵢ] / n
```

Where `1[·]` is the indicator function — 1 if true, 0 otherwise.

```
y     = [0, 1, 1, 0, 1]
ŷ     = [0, 1, 0, 0, 1]
match = [✓, ✓, ✗, ✓, ✓]

Accuracy = 4/5 = 0.80
```

### `cross_val_score()` — Aggregation

After running k folds you have k scores `s₁, s₂, ..., sₖ`:

```
Mean = (1/k) × Σ sᵢ

Std  = √( (1/k) × Σ (sᵢ − mean)² )
```

**Example with 5 folds:**

```
cv_scores = [0.81, 0.85, 0.79, 0.83, 0.80]

Mean = (0.81 + 0.85 + 0.79 + 0.83 + 0.80) / 5
     = 4.08 / 5
     = 0.816

Variance = ((0.81−0.816)² + (0.85−0.816)² + (0.79−0.816)² + (0.83−0.816)² + (0.80−0.816)²) / 5
         = (0.000036 + 0.001156 + 0.000676 + 0.000196 + 0.000256) / 5
         = 0.00232 / 5
         = 0.000464

Std = √0.000464 ≈ 0.0215
```

---

## Summary

```python
# Quick check on a single test set
model.score(X_test, y_test)

# Reliable evaluation across folds
cross_val_score(model, X, y, cv=5, scoring='r2').mean()
```

Use `.score()` for a fast sanity check. Use `cross_val_score()` whenever you actually want to **trust the number**.
