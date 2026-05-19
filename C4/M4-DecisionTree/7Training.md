# Training a Decision Tree — The CART Algorithm

**CART** = Classification and Regression Trees — the standard algorithm used by sklearn (and most libraries).

It builds trees by **recursive partitioning** — repeatedly splitting the data, with each split chosen to maximise prediction quality.

---

## Step by Step

```
1. Start with the entire dataset at the root
2. For each feature:
       For each candidate split (threshold / category subset):
           Compute impurity score:
              - Gini / Entropy (classification)
              - Variance (regression)
   Pick the split with the largest impurity reduction
3. Divide data into two child nodes
4. Recursively repeat steps 2–3 on each child
5. Stop when a stopping condition is met
```

This is **greedy** — at each step, it picks the locally-best split without looking ahead.

---

## Why Greedy Works

A globally-optimal tree would require trying every possible tree structure — combinatorially explosive. CART's greedy approach:

```
Cheap            → only consider one split at a time
Good in practice → works well on most data
Not optimal      → may miss a globally better tree
```

It's a trade-off between optimality and feasibility.

---

## Stopping Conditions

The tree stops growing when at least one of these is true:

| Condition | Meaning |
|-----------|---------|
| Node is pure | All points same class (classification) or zero variance (regression) |
| `max_depth` reached | Tree can't grow deeper |
| `min_samples_split` not met | Too few points to split further |
| `min_samples_leaf` not met | A child would have too few points |
| `min_impurity_decrease` not met | The split's improvement is too small |

These are **hyperparameters** you set in sklearn. They prevent the tree from growing too deep and overfitting.

---

## What's Stored After Training

For each internal node:
- The feature to split on
- The threshold (or category group) to split at

For each leaf node:
- Classification → the class label (or class probabilities)
- Regression → the mean (or median) of target values

The trained tree is then just this hierarchy of stored splits and leaf predictions.

---

## Decision Regions

After training, the feature space is partitioned into disjoint **rectangular regions** — one per leaf:

```
   Age
    │     R1   │  R3
    │ (Class A)│ (Class B)
50  │──────────│
    │     R2   │  R4
    │ (Class B)│ (Class A)
    └──────────│────────── BP
              120
```

Each region has a single prediction. New points are assigned the prediction of whichever region they fall into.

---

## sklearn

```python
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

# Classification
clf = DecisionTreeClassifier(criterion='gini', max_depth=5)
clf.fit(X_train, y_train)

# Regression
reg = DecisionTreeRegressor(criterion='squared_error', max_depth=5)
reg.fit(X_train, y_train)
```

Setting `max_depth` is the simplest way to prevent overfitting — more on this in `9PrePruning.md`.

---

## Summary

```
CART = greedy recursive partitioning
At each node → pick best (feature, split) by impurity reduction
Continue until stopping condition met
Result → tree of split rules + leaf predictions
```
