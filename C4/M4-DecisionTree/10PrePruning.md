# Pre-Pruning (Early Stopping)

Stop the tree from growing **before** it overfits — by imposing rules during training.

Pre-pruning is guided by the principle of **diminishing returns**: each new split makes nodes slightly purer, but the improvement eventually becomes marginal while the overfitting risk grows.

---

## The Main Hyperparameters

### `max_depth`

Limits how many levels the tree can grow.

```
max_depth=3:
            [Root]
            /    \
          ...    ...
        depth 2  depth 2
         /  \    /  \
       leaf leaf leaf leaf       ← forced to be leaves at depth 3
```

```
Shallow tree (depth 3) → may underfit
Deep tree (depth 30)   → almost always overfits
Typical good values    → 3 to 10
```

### `min_samples_split`

A node must contain **at least N samples** before it can be split.

```
min_samples_split=20 → nodes with fewer than 20 points become leaves
```

Prevents the tree from creating tiny branches for handful-of-cases situations.

### `min_samples_leaf`

Each leaf must have at least N points. Tighter than `min_samples_split` because it constrains the result of any split.

```
min_samples_leaf=10 → no leaf can have fewer than 10 training points
```

Makes leaf predictions more stable — avoids leaves with just 1–2 points.

### `min_impurity_decrease`

A split is only made if it reduces impurity by more than this threshold.

```
min_impurity_decrease=0.01 → tiny improvements are ignored
```

Prevents the algorithm from chasing micro-improvements (which often capture noise).

### `max_leaf_nodes`

Cap the total number of leaf nodes:

```
max_leaf_nodes=20 → tree builds in best-first order, stops at 20 leaves
```

A direct way to bound model complexity.

---

## How These Three Guards Work — Worked Examples

`min_samples_split`, `min_samples_leaf`, and `min_impurity_decrease` each block splits for different reasons. All three are checked independently — any one can veto a split.

### `min_samples_split=20`

Node must have **at least 20 samples** to even attempt a split.

```
Node A: 25 samples  →  can split ✓ (25 ≥ 20)
Node B: 15 samples  →  cannot split — declared a leaf ✗
```

```
            [Root: 100]
              /     \
        [N=25]      [N=15]    ← N=15 < 20 → forced leaf
         can         must
         split       stop
```

Stops the tree from creating tiny branches for handfuls of points.

### `min_samples_leaf=10`

Every leaf must have **at least 10 samples**. A split is rejected if either child would be smaller.

```
Node with 50 samples, candidate split would produce:
   Child 1: 45 samples  ✓
   Child 2: 5 samples   ✗  (< 10)
   → split REJECTED, node stays a leaf

Another candidate split on same node:
   Child 1: 30 samples  ✓
   Child 2: 20 samples  ✓
   → split ALLOWED
```

Tighter than `min_samples_split` — constrains the children, not just the parent.

### `min_impurity_decrease=0.001`

The split must reduce impurity by **at least 0.001** (after weighting).

```
Node: Gini = 0.45 (50 samples)
   ├── Child 1: Gini = 0.44 (25 samples)
   └── Child 2: Gini = 0.45 (25 samples)

Weighted child Gini = 0.5×0.44 + 0.5×0.45 = 0.445
Reduction          = 0.45 − 0.445 = 0.005

0.005 > 0.001 → split allowed ✓
```

vs

```
Node: Gini = 0.45
   ├── Child 1: Gini = 0.4499 (25 samples)
   └── Child 2: Gini = 0.4500 (25 samples)

Reduction = 0.00005
0.00005 < 0.001 → split REJECTED ✗
```

Stops the algorithm from chasing tiny noise-driven improvements.

### All three together

```python
DecisionTreeClassifier(
    min_samples_split=20,
    min_samples_leaf=10,
    min_impurity_decrease=0.001
)
```

For a node with 40 samples (Gini = 0.40), best candidate split would produce:

```
├── Child 1: 8 samples, Gini = 0.30
└── Child 2: 32 samples, Gini = 0.20

1. parent samples 40 ≥ 20 ✓
2. min(8, 32) = 8 ≥ 10? ✗  ← FAILS
3. (irrelevant — already rejected)

Split REJECTED
```

Next-best candidate:

```
├── Child 1: 18 samples, Gini = 0.32
└── Child 2: 22 samples, Gini = 0.28

1. parent samples 40 ≥ 20 ✓
2. min(18, 22) = 18 ≥ 10 ✓
3. Reduction = 0.40 − (18/40 × 0.32 + 22/40 × 0.28)
             = 0.40 − 0.298
             = 0.102
   0.102 ≥ 0.001 ✓

Split ALLOWED
```

The first candidate was rejected only because of `min_samples_leaf`. Each guard has its own role.

### What each blocks

| Hyperparameter | Blocks what |
|----------------|-------------|
| `min_samples_split` | Parent is too small to attempt a split |
| `min_samples_leaf` | A child would be too small |
| `min_impurity_decrease` | Improvement is too small (chasing noise) |

> All three are "guards" against fragile splits. They run independently — any one can veto a split.

---

## Class Probability Threshold (Classification Only)

Another stopping rule: if one class already dominates a node strongly enough (e.g. 90%+), further splitting won't add value:

```
Node with 95 Yes, 5 No (95% pure)
   → declare it a leaf, predict "Yes"
   → don't bother splitting further
```

In sklearn this is controlled indirectly via `min_impurity_decrease`.

---

## sklearn Example

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(
    max_depth=5,
    min_samples_split=20,
    min_samples_leaf=10,
    min_impurity_decrease=0.001,
    random_state=42
)
model.fit(X_train, y_train)
```

---

## Effect of Pre-Pruning

```
Smaller, more compact trees
Easier to interpret
Faster to predict with
Less prone to overfitting
```

---

## The Risk — Underfitting

Aggressive pre-pruning can also hurt:

```
Too aggressive:
   max_depth=2 → tree too shallow → misses real patterns
   → high train error AND high test error → underfit
```

You're trading off bias and variance. The right values depend on data — find them with **cross-validation** (GridSearchCV).

---

## Tuning Pre-Pruning Hyperparameters

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'max_depth':        [3, 5, 7, 10, 15, None],
    'min_samples_split':[2, 10, 20, 50],
    'min_samples_leaf': [1, 5, 10, 20]
}

grid = GridSearchCV(DecisionTreeClassifier(random_state=42), param_grid, cv=5)
grid.fit(X_train, y_train)

print(grid.best_params_)
```

CV picks the combination that gives the best balance.

---

## Summary

| Hyperparameter | Effect |
|----------------|--------|
| `max_depth` | Cap tree depth |
| `min_samples_split` | Min samples needed to attempt a split |
| `min_samples_leaf` | Min samples each leaf must have |
| `min_impurity_decrease` | Min improvement needed to allow a split |
| `max_leaf_nodes` | Cap total leaves |

> Pre-pruning is the simpler, faster approach. **Always set at least `max_depth`** when using a decision tree — never leave it unbounded.
