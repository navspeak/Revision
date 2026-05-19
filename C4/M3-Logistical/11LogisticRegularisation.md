# Regularisation in Logistic Regression

Same idea as Ridge / Lasso — but applied to Logistic Regression. Penalise large coefficients to prevent overfitting.

---

## The Cost Function

Plain LR minimises log-loss:

```
Log-loss = −(1/n) × Σ[y log(p) + (1−y) log(1−p)]
```

Regularised LR adds a penalty term:

```
L2 (Ridge):   Log-loss + λ × Σβ²
L1 (Lasso):   Log-loss + λ × Σ|β|
```

Same penalty shapes as linear regression — same behaviour:
- **L2** shrinks coefficients smoothly toward 0
- **L1** drives some coefficients exactly to 0 (feature selection)

---

## sklearn's C — Not Alpha

Here's the **gotcha** — sklearn's `LogisticRegression` uses `C`, not `alpha`:

```
C = 1 / λ

Small C  → strong regularisation  (large λ)
Large C  → weak regularisation    (small λ)
C = ∞    → no regularisation
```

Why the inversion? Historical convention from SVMs. It just means **smaller C = more shrinkage** — opposite of Ridge/Lasso where larger `alpha` = more shrinkage.

| Parameter | Direction |
|-----------|-----------|
| Ridge / Lasso `alpha` | bigger = more regularisation |
| LogisticRegression `C` | smaller = more regularisation |

SVM = Support Vector Machine — another classification algorithm (predates Logistic Regression's popularity in sklearn).
---

## Default Behaviour

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
# Equivalent to:
# LogisticRegression(C=1.0, penalty='l2', solver='lbfgs')
```

By default sklearn applies **L2 regularisation with C=1.0** — you cannot turn it off accidentally. To disable:

```python
LogisticRegression(penalty=None)   # no regularisation
```

---

## Penalty Options

```python
LogisticRegression(penalty='l2')           # default — Ridge-like
LogisticRegression(penalty='l1', solver='liblinear')   # Lasso-like
LogisticRegression(penalty='elasticnet', solver='saga', l1_ratio=0.5)
LogisticRegression(penalty=None)           # no penalty
```

L1 requires `solver='liblinear'` or `'saga'` (`lbfgs` doesn't support L1).

---

## Tuning C

Use `GridSearchCV` with cross-validation:

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'C':       [0.001, 0.01, 0.1, 1.0, 10, 100],
    'penalty': ['l1', 'l2']
}

grid = GridSearchCV(
    LogisticRegression(solver='liblinear', max_iter=1000),
    param_grid,
    cv=5,
    scoring='accuracy'
)
grid.fit(X_train, y_train)

print(grid.best_params_)     # best C and penalty
print(grid.best_score_)      # best mean CV score
```

Standardise features first — same reason as linear regression.

---

## Summary

| | Linear (Ridge/Lasso) | Logistic Regression |
|-|----------------------|---------------------|
| Strength parameter | `alpha` (= λ) | `C` (= 1/λ) |
| More regularisation | Larger alpha | Smaller C |
| L2 penalty | `Ridge(alpha=...)` | `LogisticRegression(penalty='l2', C=...)` |
| L1 penalty | `Lasso(alpha=...)` | `LogisticRegression(penalty='l1', solver='liblinear', C=...)` |
| Default | None (`LinearRegression`) | L2 with C=1.0 |
| Tune via | GridSearchCV | GridSearchCV |

> Logistic Regression has L2 on by default — and `C` is inverted relative to `alpha`. Mixing those up is the most common confusion.
