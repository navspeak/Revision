# Feature Importance

Decision trees not only make predictions but also tell you **which features mattered most** in those predictions.

This is one of the most useful by-products of decision trees — easy interpretability of feature contributions.

---

## How It's Computed

Each time a feature is used to split the data, it **reduces impurity** in the resulting subgroups. The larger the reduction, the more useful that split.

Feature importance for feature Xⱼ:

```
Importance(Xⱼ) = Σ ΔImpurity   over all splits using Xⱼ
```

Where ΔImpurity is the decrease in Gini / Entropy / Variance produced by that split.

After summing over all splits, importances are **normalised** so they sum to 1 across all features.

```
Feature        Importance
BP             0.45
Cholesterol    0.30
Age            0.15
Sex            0.07
Smoker         0.03
              -----
              1.00
```

---

## Interpreting Feature Importance

```
High importance → feature consistently improves predictions
                  → main driver of the tree's decisions

Low importance  → either provides little discriminatory power
                  → or is overshadowed by stronger predictors (which split first)
```

### Example

In a tree predicting heart disease:

```
BP            → 0.45   ← splits high in the tree, big impurity drops
Cholesterol   → 0.30
Age           → 0.15
Sex           → 0.07
Smoker        → 0.03   ← rarely used or weak splits
```

Blood pressure and cholesterol are the dominant predictors. Smoker contributes little — perhaps because BP already captures most of its effect.

---

## sklearn

After fitting:

```python
model.feature_importances_
# array([0.45, 0.30, 0.15, 0.07, 0.03])

import pandas as pd
importance = pd.DataFrame({
    'feature':    feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(importance)
```

---

## Effect of Pruning on Importance

When a tree is pruned, weaker branches disappear — features that contributed little may **vanish entirely** from the model:

```
Before pruning:                After pruning:
  BP:           0.30             BP:           0.45
  Chol:         0.20             Chol:         0.35
  Age:          0.15             Age:          0.20
  Sex:          0.10             Sex:          0.00  ← dropped
  Smoker:       0.10             Smoker:       0.00  ← dropped
  Exercise:     0.08
  Diet:         0.07
```

Strong features become more prominent. Pruning **sharpens the picture** of which features really matter — similar to how Lasso zeroes out unimportant coefficients.

---

## Limitations

Tree-based feature importance has known issues:

### 1. Bias toward high-cardinality features

A categorical feature with many levels (e.g. zip code with 1000 values) has many split opportunities. It can appear **artificially important** because there are simply more ways to split on it.

### 2. Instability

Trees are sensitive to small changes in data. Slight changes in training data can flip which feature wins at a node, swinging importance scores significantly.

```
Same data, different random_state → different tree → different importance ranking
```

### 3. Relative, not absolute

Importance is measured **relative to the other features in the model**. Remove a strong predictor — others' importance shoots up artificially:

```
With BP in model:        Without BP:
  BP:    0.45              Cholesterol: 0.55  ← suddenly looks more important
  Chol:  0.30              Age:         0.30
  Age:   0.15
```

### 4. Doesn't show direction

Unlike linear regression coefficients (positive/negative), tree importance only shows **magnitude** — it doesn't tell you whether a feature increases or decreases the predicted outcome.

---

## Better Alternatives (for Serious Work)

For more robust feature importance:

```
Permutation importance     → permute one feature at a time, measure performance drop
SHAP values                → game-theoretic attribution, shows direction too
Random Forest importance   → averaged over many trees → more stable
```

These reduce instability and bias issues of single-tree importance.

---

## Summary

```
feature_importances_  → relative score (sums to 1)
Computed from         → impurity reduction at each split
Useful for            → quick interpretability, identifying drivers
Limitations           → bias to high-cardinality, instability, relative only
```

> Use feature importance for **direction**, not certainty. Validate with permutation importance or SHAP for serious analysis.
