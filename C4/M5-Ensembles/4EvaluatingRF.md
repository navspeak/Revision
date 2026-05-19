# Evaluating Random Forests

Random Forests use the same evaluation metrics as any supervised model — but they also offer **two built-in tools** you don't get with single models:

- **Out-of-Bag (OOB) error**
- **Feature importance**

---

## Standard Metrics

Classification:

```
accuracy_score, precision, recall, F1, ROC-AUC, classification_report, confusion_matrix
```

Regression:

```
MSE, RMSE, MAE, R²
```

These are computed exactly as you'd compute them for any model — on a held-out test set.

---

## Out-of-Bag (OOB) Error

Recall — each tree is trained on a bootstrap sample of the data. **Roughly 37% of rows are NOT included** in any given tree's training set (the math: probability of being unsampled in a draw of N from N with replacement → e⁻¹ ≈ 0.37).

These "out-of-bag" rows are essentially **free validation data** — the tree never saw them.

### How OOB works

```
For each training point i:
   Find all trees that did NOT include point i in their bootstrap sample.
   Use only those trees to predict point i.
   Record whether they got it right.

OOB error = error rate across all such predictions.
```

This gives a **reliable performance estimate without needing a separate validation set**.

### In sklearn

```python
model = RandomForestClassifier(n_estimators=200, oob_score=True, random_state=42)
model.fit(X_train, y_train)

print(f'OOB score: {model.oob_score_:.3f}')   # accuracy or R² depending on task
```

```
OOB ≈ cross-validation accuracy → you get a reliable estimate "for free"
```

You can even use OOB instead of cross-validation when tuning — saves significant compute on large data.

---

## Feature Importance

Same idea as in single Decision Trees, but **averaged across all trees** in the forest. This averaging makes RF importance **much more stable** than single-tree importance.

```
Importance(feature j) = mean impurity reduction caused by splits on j
                       averaged over all trees
                       normalised so total = 1
```

In sklearn:

```python
model.feature_importances_
# array([0.21, 0.18, 0.12, 0.09, ...])

import pandas as pd
fi = pd.DataFrame({
    'feature':    feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
```

### Why RF Feature Importance Is Better Than Single Tree

```
Single tree: one feature dominates the root → others may rank artificially low
Random Forest: many trees use different splits → ranking averages out

→ much more reliable for understanding which features really matter
```

### Same Limitations

Despite being more stable, tree-based importance still has the same issues:

```
- Bias toward high-cardinality features (more split options)
- Doesn't show direction (positive or negative effect)
- Relative — depends on which other features are in the model
```

For more rigorous attribution, use **permutation importance** or **SHAP** — both work great with Random Forest.

---

## Advantages and Disadvantages

| Advantages | Disadvantages |
|------------|---------------|
| High accuracy, generalises well | Less interpretable than a single tree |
| Handles numerical + categorical natively | Computationally heavy (many trees) |
| Reduces overfitting via diverse trees | Slower predictions (must traverse all trees) |
| Built-in feature importance | Can't extrapolate beyond training range |
| Built-in OOB error → no need for separate validation | May overkill for small/simple datasets |
| Robust to outliers and missing data | Memory-heavy for large forests |
| Parallelisable — trains fast | Tuning many hyperparameters takes effort |

---

## Hyperparameters Recap

| Hyperparameter | sklearn name | Effect |
|----------------|--------------|--------|
| Number of trees | `n_estimators` | More = lower variance (diminishing returns) |
| Max depth | `max_depth` | Limits each tree's depth |
| Features per split | `max_features` | Controls tree diversity |
| Min samples per split | `min_samples_split` | Pre-pruning |
| Min samples per leaf | `min_samples_leaf` | Pre-pruning |
| Bootstrap | `bootstrap` | Use bootstrap sampling (True by default) |
| Sample size per tree | `max_samples` | Fraction of training data per tree |
| Class weighting | `class_weight` | Handle imbalanced classes |
| Random state | `random_state` | Reproducibility |
| Parallel jobs | `n_jobs` | -1 = use all cores |

Hyperparameters of the **base decision trees** also apply (depth, min_samples, etc.) — they affect each individual tree in the forest.

---

## Quick Decision Guide

```
n_estimators:   start at 100, push to 300-500 for marginal gains
max_features:   leave default ('sqrt' for classifier, 1.0 for regressor)
max_depth:      leave None unless overfitting badly
min_samples_*:  bump up if data is noisy
n_jobs:         always -1 (parallelise)
oob_score:      True (free validation)
random_state:   42 (reproducibility)
```

For most problems these defaults give you 95% of the achievable accuracy.

---

## Summary

```
Standard metrics work as usual (accuracy, RMSE, R², F1, ...)

Two RF-specific tools:
   1. OOB error      → built-in validation, no separate set needed
   2. Feature importance → stable averaged ranking across trees

Random Forest tuning is forgiving — defaults usually work well.
```

> Always set `oob_score=True` — it's a free reliability check on your model.
