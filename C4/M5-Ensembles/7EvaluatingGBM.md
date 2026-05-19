# Evaluating Gradient Boosting

Same standard metrics as Random Forest — plus a few **boosting-specific considerations**.

---

## Standard Metrics

```
Classification:  accuracy, precision, recall, F1, ROC-AUC
Regression:      MSE, RMSE, MAE, R²
```

Compute these on a held-out test set, as usual.

---

## Feature Importance

Gradient Boosting also gives `feature_importances_` — calculated from the impurity reduction at each split, summed and averaged across all trees.

```python
model.fit(X_train, y_train)
importance = pd.DataFrame({
    'feature':    feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
```

Same caveats as RF importance:
- Biased toward high-cardinality features
- Doesn't show direction
- Better alternatives — permutation importance or SHAP

---

## Early Stopping — Critical for GBM

Gradient Boosting **can overfit if trained too long**. After enough rounds, it stops learning the signal and starts fitting noise.

### Symptom

```
Round 50:   train RMSE = 8.0,   validation RMSE = 8.5    ← still improving
Round 100:  train RMSE = 4.0,   validation RMSE = 7.8    ← still improving
Round 200:  train RMSE = 2.0,   validation RMSE = 7.5    ← peak
Round 300:  train RMSE = 1.0,   validation RMSE = 8.0    ← overfitting now
Round 500:  train RMSE = 0.3,   validation RMSE = 9.5    ← bad
```

The fix: **stop when validation error stops improving**.

### Early Stopping in sklearn

```python
from sklearn.ensemble import GradientBoostingClassifier

model = GradientBoostingClassifier(
    n_estimators=1000,                # large upper bound
    learning_rate=0.05,
    validation_fraction=0.2,          # hold out 20% for early stopping
    n_iter_no_change=20,              # stop if no improvement for 20 rounds
    tol=1e-4,                         # minimum improvement to "count"
    random_state=42
)
model.fit(X_train, y_train)

print(f'Stopped at iteration: {model.n_estimators_}')
```

### Early Stopping in XGBoost / LightGBM

These libraries make early stopping even cleaner:

```python
import xgboost as xgb

model = xgb.XGBClassifier(n_estimators=1000, learning_rate=0.05)
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    early_stopping_rounds=20,
    verbose=False
)
```

> **Always use early stopping with boosting.** It's the most important regularisation tool.

---

## Advantages and Disadvantages

| Advantages | Disadvantages |
|------------|---------------|
| Highly accurate — often state-of-the-art on tabular data | Prone to overfitting if learning rate or iterations too high |
| Handles classification and regression equally well | Computationally expensive — sequential training |
| Works with weak learners (shallow trees) | Slower than parallel methods like Random Forest |
| Focuses on hard-to-predict samples (errors) | Sensitive to noise and outliers (gets amplified) |
| Supports regularisation (shrinkage, subsampling, L1/L2) | Many hyperparameters to tune |

---

## Hyperparameters

The four most important:

| Hyperparameter | sklearn name | Typical | Effect |
|----------------|--------------|---------|--------|
| Number of trees | `n_estimators` | 100–1000 (with early stopping) | More = more capacity, more risk |
| Learning rate | `learning_rate` | 0.01–0.1 | Smaller = needs more trees, often better |
| Max tree depth | `max_depth` | 3–8 | Boosting prefers SHALLOW trees |
| Subsample | `subsample` | 0.5–1.0 | Fraction of rows per tree (regularisation) |

Other important ones:

| Hyperparameter | sklearn name | Effect |
|----------------|--------------|--------|
| Min samples per split | `min_samples_split` | Standard pre-pruning |
| Min samples per leaf | `min_samples_leaf` | Standard pre-pruning |
| Loss function | `loss` | What's being minimised (deviance, exponential, etc.) |
| Features per split | `max_features` | Adds randomness to splits |
| Validation fraction | `validation_fraction` | For early stopping |
| Tolerance | `tol` | Minimum improvement threshold |
| Random state | `random_state` | Reproducibility |

XGBoost / LightGBM add **L1 and L2 regularisation** on tree weights — `reg_alpha` and `reg_lambda` — which sklearn's GBM doesn't have.

---

## Tuning Strategy

```
1. Start with: learning_rate=0.1, n_estimators=100, max_depth=3
2. Enable early stopping with a validation set
3. Increase n_estimators (1000) — let early stopping find the right number
4. Reduce learning_rate to 0.05 or 0.01 → re-tune n_estimators
5. Try max_depth 5–7 for more complex problems
6. Add subsample=0.8 for extra regularisation
7. Use GridSearchCV or Optuna for full sweep
```

The most impactful trade-off is **learning rate × n_estimators**:

```
learning_rate=0.1, n_estimators=100   →  fast, decent
learning_rate=0.05, n_estimators=200  →  better
learning_rate=0.01, n_estimators=1000 →  often best, slowest
```

---

## Bagging vs Boosting Hyperparameters

| | Random Forest | Gradient Boosting |
|-|---------------|---------------------|
| Tree depth | Deep (none / unlimited) | Shallow (3–8) |
| Learning rate | N/A | Critical (0.01–0.1) |
| Number of trees | More always helps (up to a point) | Tightly coupled with learning rate |
| Tuning effort | Low — defaults work | Medium-high — needs careful tuning |
| Best for | Quick robust baseline | Maximum accuracy with effort |

---

## Summary

```
Evaluation:    standard metrics + feature importance
Critical:      EARLY STOPPING (always use it with boosting)
Key knobs:     learning_rate × n_estimators × max_depth × subsample
Mindset:       small learning rate + many trees + early stopping = best generalisation
```

> If you've tuned RF and want more accuracy, gradient boosting is the next step — but be ready to tune carefully and always use early stopping.
