# Cross-Validation

A reliable way to evaluate a model — and to pick hyperparameters — without depending on one lucky/unlucky split.

---

## The Problem with a Single Split

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
model.fit(X_train, y_train)
model.score(X_test, y_test)   # → 0.83
```

Change `random_state` → score changes:

```
random_state=0:  R² = 0.78
random_state=1:  R² = 0.85
random_state=2:  R² = 0.81
random_state=3:  R² = 0.74
```

Which one is "the" performance? You don't know. One number is unreliable.

---

## k-Fold Cross-Validation

Split the data into **k equal pieces (folds)**. Train k times — each time using one different fold as the test set and the other k−1 as training. Average the k scores.

```
With k=5:

Fold 1: [TEST] [train] [train] [train] [train]
Fold 2: [train] [TEST] [train] [train] [train]
Fold 3: [train] [train] [TEST] [train] [train]
Fold 4: [train] [train] [train] [TEST] [train]
Fold 5: [train] [train] [train] [train] [TEST]

Final score = mean of 5 fold scores
```

Every data point gets used for testing exactly once. The mean is a much more stable estimate than any single split.

---

## Why k-Fold Works

```
Single split:  1 number → high variance
5-fold CV:     average of 5 → low variance, plus std dev as a stability measure
```

Common values:
- **k = 5** — most common, good balance
- **k = 10** — slightly more reliable, slower
- **k = n** (LOOCV) — extreme case, see below

---

## LOOCV — Leave-One-Out Cross-Validation

The extreme case of k-fold where **k = n** (number of rows). Each row gets its own "fold" — you train on n−1 points and test on the 1 left-out point. Repeat n times.

```
With n=5 rows:

Iter 1:  TEST=[A]   train=[B C D E]
Iter 2:  train=[A]  TEST=[B]   train=[C D E]
Iter 3:  train=[A B] TEST=[C]  train=[D E]
Iter 4:  train=[A B C] TEST=[D] train=[E]
Iter 5:  train=[A B C D] TEST=[E]
```

Final score = mean of all n test errors.

### When LOOCV makes sense

```
Very small datasets   → can't afford to lose data to a test fold
Few rows (n < 50)     → 5-fold loses 20% of data per fold; LOOCV uses n−1
```

### Trade-offs

| | k-fold (k=5/10) | LOOCV (k=n) |
|-|-----------------|-------------|
| Uses how much data per fit | (k−1)/k of total | (n−1)/n — almost all |
| Number of model fits | k | n |
| Compute cost | Low | Very high |
| Bias of estimate | Slightly higher | Very low |
| Variance of estimate | Lower | **Higher** (each fit uses nearly identical training data) |

LOOCV uses almost all data for each fit → low bias. But every fold's training set is nearly identical → fits are highly correlated → high variance in the average.

**Rule of thumb:** prefer 5-fold or 10-fold CV. Use LOOCV only for very small datasets.

### sklearn

```python
from sklearn.model_selection import LeaveOneOut, cross_val_score

scores = cross_val_score(model, X, y, cv=LeaveOneOut())   # n scores
print(scores.mean())
```

---

## CV for Hyperparameter Tuning

This is the most important use of CV — not just evaluating a model, but **choosing between models or hyperparameters**.

```
For each candidate hyperparameter value:
    Run k-fold CV → get mean score
Pick the value with the highest mean CV score
```

This is what `GridSearchCV` automates.

---

## Train / Validation / Test Split

When tuning hyperparameters, the proper workflow:

```
Full data
    ↓
train_test_split → train set (e.g. 80%) | test set (20%)
    ↓                                    ↑
GridSearchCV does CV on train set     hold out, touch ONCE at the end
    ↓
Pick best hyperparameter
    ↓
Train final model on full train set
    ↓
Evaluate on held-out test set → final reported number
```

**Never tune hyperparameters using the test set** — that leaks information and gives an optimistic estimate.

---

## sklearn

```python
from sklearn.model_selection import cross_val_score, KFold, GridSearchCV

# Basic CV
scores = cross_val_score(model, X, y, cv=5, scoring='r2')
print(scores.mean(), scores.std())

# Hyperparameter tuning with CV
param_grid = {'alpha': [0.001, 0.01, 0.1, 1.0, 10]}
grid = GridSearchCV(Ridge(), param_grid, cv=5, scoring='r2')
grid.fit(X_train, y_train)

grid.best_params_     # best hyperparameter
grid.best_score_      # mean CV score at that value
grid.score(X_test, y_test)   # final test-set score
```

---

## `cv_results_` — Per-Candidate Scores

`grid.cv_results_` is a dict with detailed results for every candidate. The two most useful keys:

```python
grid.cv_results_['mean_test_score']   # mean score across folds, per candidate
grid.cv_results_['std_test_score']    # std across folds, per candidate
```

> **The key names are always `mean_test_score` / `std_test_score`** — regardless of which metric you used. The word `test_score` here means "score on the validation fold", not the metric name.

### Same key for different metrics

```python
# scoring='r2'
grid.cv_results_['mean_test_score']   # mean R²

# scoring='f1'
grid.cv_results_['mean_test_score']   # mean F1 — same key

# scoring='roc_auc'
grid.cv_results_['mean_test_score']   # mean ROC-AUC — same key
```

The metric **name doesn't appear in the key** — only the values change.

### Building a results table

```python
pd.DataFrame({
    'alpha':   param_grid['alpha'],
    'mean_f1': grid.cv_results_['mean_test_score'].round(3),   # rename label as you like
    'std_f1':  grid.cv_results_['std_test_score'].round(3)
})
```

The dict key stays `'mean_test_score'`. Only your dataframe column label changes.

### Exception — Multi-Metric Scoring

If you pass multiple metrics, sklearn appends the metric name to the key:

```python
grid = GridSearchCV(model, param_grid, cv=5,
                    scoring=['accuracy', 'f1'],
                    refit='f1')

grid.cv_results_['mean_test_accuracy']
grid.cv_results_['mean_test_f1']
```

With a single `scoring=` string, it's always just `mean_test_score` / `std_test_score`.

---

## Summary

| | Single split | k-fold CV |
|-|--------------|-----------|
| Number of evaluations | 1 | k |
| Reliable? | No — varies with random_state | Yes — mean of k |
| Use for tuning? | Bad idea | Yes — `GridSearchCV` |
| Compute cost | Low | k× higher |

> CV is the standard way to evaluate ML models — both for reporting performance and for choosing hyperparameters.
