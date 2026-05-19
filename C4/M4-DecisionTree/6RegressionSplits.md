# Splitting for Regression — Variance Reduction

For regression trees, the target is **numerical**, not categorical. So Gini and Entropy don't apply.

Instead, we want subgroups where the **target values are tightly clustered** around a central value. The natural measure: **variance**.

---

## Variance as Impurity

For a node with target values y₁, y₂, ..., yₙ:

```
Var = (1/n) × Σ(yᵢ − ȳ)²

where ȳ = mean of values in the node
```

- All values equal → variance = 0 → pure
- Values spread out → variance large → impure

---

## Variance Reduction

Same logic as Gini/Entropy: take a **weighted average** of the children's variances:

```
Var(children) = (n₁/n) × Var₁ + (n₂/n) × Var₂

Variance Reduction = Var(parent) − Var(children)
```

The split with the **largest variance reduction** is chosen.

---

## Worked Example

Target = "years until heart risk", 10 patients:

```
y = {11.5, 8, 8.5, 10, 10, 12, 3, 9, 7, 6}
ȳ = 8.9
```

### Parent variance

```
Var(parent) = (1/10) × Σ(yᵢ − 8.9)²
            ≈ 4.0
```

### After splitting on Age

```
Region 1: {11.5, 8, 8.5, 10, 10, 12}   (n=6)
  mean ≈ 10.0
  variance ≈ 2.1

Region 2: {3, 9, 7, 6}                  (n=4)
  mean ≈ 6.25
  variance ≈ 0.9
```

### Weighted children variance

```
Var(children) = (6/10) × 2.1 + (4/10) × 0.9
              = 1.26 + 0.36
              = 1.62
```

### Variance Reduction

```
Reduction = 4.0 − 1.62 = 2.38
```

A large reduction → this is an effective split.

---

## Same Logic, Different Metric

```
Classification → reduce Gini or Entropy
Regression     → reduce Variance
```

The algorithm is otherwise identical — try every feature × every split, pick the one that reduces impurity (= variance) most.

---

## sklearn

```python
from sklearn.tree import DecisionTreeRegressor

# Default — uses MSE (= variance, since variance is mean squared deviation)
DecisionTreeRegressor(criterion='squared_error')

# Alternative — uses absolute error
DecisionTreeRegressor(criterion='absolute_error')
```

`squared_error` corresponds to variance reduction (the default).

---

## Summary

```
Regression target  → variance is the impurity measure
Pure leaf          → all values equal (variance = 0)
Best split         → maximises variance reduction
```

> Same machinery as classification — only the impurity metric changes.
