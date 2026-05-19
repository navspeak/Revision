# GridSearchCV — Theory

**Problem it solves:** picking the best hyperparameter values without guessing.

You have hyperparameters like `C`, `alpha`, `max_depth`. There's no formula to find the optimal value — you have to try several and pick the best. GridSearchCV automates that trial.

---

## The "Grid" Part

You define a **grid** of candidate values:

```python
param_grid = {
    'C': [0.001, 0.01, 0.1, 1, 10, 100],
    'penalty': ['l1', 'l2']
}
```

GridSearchCV tries **every combination** in the grid:

```
6 values of C × 2 penalties = 12 combinations
```

If you add another hyperparameter with 4 values → 12 × 4 = 48 combinations.

> Grid size grows exponentially — be careful with too many parameters.

---

## The "CV" Part

For **each combination**, GridSearchCV runs k-fold cross-validation:

```
For each (C, penalty) combination:
    Run 5-fold CV
    → 5 scores
    → mean CV score
```

So with 12 combinations and 5-fold CV → **12 × 5 = 60 model fits** total.

---

## The Selection

After all combinations are scored, GridSearchCV picks the one with the **highest mean CV score**:

```python
grid.best_params_   # the winning combination
grid.best_score_    # its mean CV score
```

Then it **refits** the model on the full training data using the best params:

```python
grid.predict(X_test)   # uses the best model already retrained
```

---

## Full Workflow

```
1. Define param_grid
2. For each combination in grid:
       Run k-fold CV
       Record mean score
3. Pick combination with highest mean score
4. Retrain on full training set with best params
5. Evaluate ONCE on held-out test set
```

---

## Can I Use GridSearchCV Instead of train_test_split?

No — they do different things. You usually use **both together**.

```
train_test_split  → splits data into train and final test set
GridSearchCV      → tunes hyperparameters using CV on the train set
```

### The right workflow

```python
# Step 1: split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Step 2: tune on train using CV
grid = GridSearchCV(model, param_grid, cv=5)
grid.fit(X_train, y_train)

# Step 3: evaluate ONCE on test
grid.score(X_test, y_test)
```

The test set is held back **untouched** for the final honest evaluation. GridSearchCV never sees it.

### Why not skip train_test_split?

If you do GridSearchCV on the **full data**:

```python
grid.fit(X, y)              # uses everything for CV
grid.best_score_            # this is on validation folds, but...
```

There's **no held-out set left** to honestly evaluate the final model. The CV scores are slightly optimistic because the same data was used to pick the hyperparameters.

You need fresh, untouched data to report the final performance — that's why `train_test_split` first.

### Mental model

```
Full data
   ↓
train_test_split
   ↓
┌─────────┴──────────┐
↓                     ↓
train set            test set
   ↓                     ↓
GridSearchCV         held back
(internal CV)      touched once at the end
   ↓
best model
   ↓
.score(X_test, y_test)
```

> `train_test_split` is for the final honest evaluation. `GridSearchCV` is for picking hyperparameters. They're not interchangeable — you need both.

---

## Why Not Just Pick on Test Set?

You'd be **tuning on the test set** — which leaks information and gives an optimistic estimate of generalisation.

```
Train  →  used to fit each candidate model
CV     →  used to compare candidates (inside GridSearchCV)
Test   →  used ONCE at the end to report honest performance
```

The test set is sacred — touch it only once.

---

## Worked Example

```python
from sklearn.model_selection import GridSearchCV

param_grid = {'C': [0.01, 0.1, 1, 10]}
grid = GridSearchCV(LogisticRegression(), param_grid, cv=5, scoring='accuracy')
grid.fit(X_train, y_train)

# 4 candidates × 5 folds = 20 model fits

print(grid.best_params_)   # e.g. {'C': 1}
print(grid.best_score_)    # e.g. 0.87 (mean CV accuracy)
print(grid.score(X_test, y_test))   # final honest test accuracy
```

---

## Visualising the Search

```
       C=0.01  C=0.1   C=1     C=10
fold1   0.72    0.81    0.86    0.84
fold2   0.70    0.83    0.88    0.85
fold3   0.74    0.79    0.85    0.83
fold4   0.71    0.80    0.87    0.84
fold5   0.73    0.82    0.89    0.85
--------------------------------------
mean    0.72    0.81    0.87    0.84   ← C=1 wins
std     0.02    0.02    0.02    0.01
```

---

## The `scoring=` Parameter

`scoring=` tells GridSearchCV **which metric to maximise** when comparing candidates. The right choice depends on the problem.

### For Classification (LogisticRegression, etc.)

```python
scoring='accuracy'   # (# correct) / total
scoring='precision'  # of predicted positives, how many are real?
scoring='recall'     # of actual positives, how many caught?
scoring='f1'         # harmonic mean of precision and recall
scoring='roc_auc'    # area under ROC curve
```

**When to use which:**

```
Balanced classes              → 'accuracy'
Imbalanced (e.g. fraud)       → 'f1', 'recall', 'roc_auc'
FP is costly                  → 'precision'
FN is costly                  → 'recall'
```

Example — fraud detection:

```python
# Wrong choice — accuracy will pick a useless model on imbalanced data
GridSearchCV(..., scoring='accuracy')

# Right choice — recall picks the model that catches fraud
GridSearchCV(..., scoring='recall')
```

### For Regression (LinearRegression, Ridge, Lasso)

Accuracy doesn't apply — there's no "correct/incorrect" for a continuous prediction. Use regression metrics:

```python
scoring='r2'                          # R²
scoring='neg_mean_squared_error'      # −MSE
scoring='neg_mean_absolute_error'     # −MAE
scoring='neg_root_mean_squared_error' # −RMSE
```

Why negative? GridSearchCV picks the **maximum** score. MSE/MAE are "lower is better" — negating flips them so max = best.

Example with Ridge:

```python
param_grid = {'alpha': [0.001, 0.01, 0.1, 1, 10, 100]}

grid = GridSearchCV(Ridge(), param_grid, cv=5, scoring='r2')
grid.fit(X_train, y_train)

print(grid.best_params_)    # e.g. {'alpha': 1.0}
print(grid.best_score_)     # e.g. 0.82 (mean CV R²)
```

Or with MSE:

```python
grid = GridSearchCV(Ridge(), param_grid, cv=5, scoring='neg_mean_squared_error')
grid.fit(X_train, y_train)

# Convert back to plain MSE for reporting
mse = -grid.best_score_
print(f'Best MSE: {mse:.3f}')
```

### Default `scoring=None`

If you don't specify, GridSearchCV uses the model's `.score()` default:

```
Regression       → R²
Classification   → accuracy
```

Explicit is better — always pick `scoring=` deliberately based on the problem.

### Scoring Summary

| Problem | Common scoring strings |
|---------|------------------------|
| Regression | `'r2'`, `'neg_mean_squared_error'`, `'neg_mean_absolute_error'` |
| Balanced classification | `'accuracy'` |
| Imbalanced classification | `'f1'`, `'recall'`, `'roc_auc'` |
| FP costly | `'precision'` |
| FN costly | `'recall'` |

> `scoring=` is how you tell GridSearchCV **what counts as a "good" model** — pick it based on the business problem, not by default.

---

## Limitations

- **Combinatorial explosion** — more params → exponentially more fits
- **Expensive** — k-fold × grid size — can take minutes/hours
- **Coarse** — only checks the values you give; misses anything in between

For wide searches use `RandomizedSearchCV` (samples random combinations) or Bayesian optimisation.

---

## Summary

```
GridSearchCV = (define grid) × (k-fold CV) × (pick best)
```

It's the standard way to tune hyperparameters in sklearn. The cost is many model fits, but you only do it once, and you get the best model for free at the end.
