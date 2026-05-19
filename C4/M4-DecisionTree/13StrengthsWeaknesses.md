# Strengths and Weaknesses of Decision Trees

Decision trees combine **flexibility with interpretability** — but like any model, they have real limitations.

---

## Strengths

### Easy to understand and explain

```
Rules can be followed step by step.
A doctor, manager, or non-technical stakeholder can read the tree.
```

### Handle mixed feature types natively

```
Numerical features  → use thresholds
Categorical features → use subsets
No one-hot encoding required (in principle)
```

### No feature scaling needed

```
Linear models: must scale (regularisation, gradient descent are scale-sensitive)
Trees:         scale doesn't matter — splits depend on ordering, not values
```

### Capture non-linear relationships and interactions

```
Linear models: need feature engineering for non-linearity
Trees:         naturally — that's their whole design
```

### Robust to outliers

```
Splits depend on orderings and groupings, not on the magnitude of values.
A few extreme values don't drag the model around.
```

### Visualisable

```
plot_tree() or graphviz → produces a readable diagram.
Great for communication and debugging.
```

---

## Weaknesses

### Highly prone to overfitting

```
Without pruning, trees memorise training data.
Pre-pruning + post-pruning are essential.
```

### Unstable

```
Small changes in data → very different tree.
A single noisy point can change which split wins at a node.
```

Same data resampled (e.g. bootstrap) often gives radically different trees. This instability is the **main reason ensembles work so well** (Random Forest averages over many unstable trees → stable result).

### Piecewise-constant predictions

```
Each leaf gives one constant value to its region.
Can't model smooth continuous trends elegantly — needs many leaves to approximate.
```

For regression, this often makes predictions less accurate than linear/kernel models for genuinely smooth relationships.

### Biased feature importance

```
Features with many categories or many possible thresholds
   → more opportunities to split → artificially appear more important.
```

### Often less accurate than ensembles

```
Single tree:       fast, interpretable, lower accuracy
Random Forest:     averages many trees → much better accuracy
Gradient Boosting: state-of-the-art on tabular data
```

A single tree is rarely the **best** model — but it's the **building block** for everything that follows.

---

## When to Use a Single Decision Tree

```
Want maximum interpretability         → single tree
Need to explain decisions to non-techs → single tree
Small data, simple problem            → single tree
Quick baseline                        → single tree
```

## When to Use Ensembles Instead

```
Want maximum accuracy                 → Random Forest / XGBoost / LightGBM
Tabular data, lots of features        → Gradient Boosting
Robust to noisy data                  → Random Forest
```

---

## The Bigger Picture

Decision trees are rarely the final choice for predictions — but they're **essential to understand** because:

- They form the basis of all tree-based ensembles
- They're a great mental model for non-linear relationships
- They're the most interpretable supervised ML technique

> Single tree = interpretability. Ensembles of trees = power. You need to know the single tree first.

---

## Summary

| | Strengths | Weaknesses |
|-|-----------|-----------|
| 1 | Interpretable | Overfits easily |
| 2 | Mixed feature types | Unstable to small changes |
| 3 | No scaling needed | Piecewise-constant predictions |
| 4 | Captures non-linearity | Biased feature importance |
| 5 | Robust to outliers | Often beaten by ensembles |
| 6 | Visualisable | Less accurate alone |
