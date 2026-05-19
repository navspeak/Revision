# Post-Pruning — Cost Complexity Pruning

The **opposite** of pre-pruning. Grow the tree fully — often until every leaf is pure — and then **simplify it afterwards** by cutting unnecessary branches.

The goal: strike the right balance between accuracy and complexity — similar to how regularisation works in linear/logistic regression.

---

## The Cost-Complexity Function

```
R_α(T) = R(T) + α × |T|

where
   R(T) = error of the tree on training data
   |T|  = number of leaves
   α    = complexity penalty (≥ 0)
```

The model pays a cost for **both training error AND tree size**. Each leaf adds a fixed penalty `α`.

### How α Behaves

```
α = 0        → no penalty → largest tree wins (overfits)
α small      → mild penalty → moderately pruned tree
α large      → heavy penalty → very small tree (may underfit)
```

> α is a hyperparameter — exactly like λ in Ridge/Lasso.

In sklearn it's called **`ccp_alpha`** (cost complexity pruning alpha).

---

## Comparison with Regularisation

```
Ridge:   minimise   SSE       + λ × Σβ²        (penalty on coefficient size)
Lasso:   minimise   SSE       + λ × Σ|β|       (sparsity)
Trees:   minimise   error R(T) + α × |T|       (penalty on tree size)
```

Same idea — bound complexity via a tunable penalty.

---

## Cost Complexity Pruning Algorithm

```
1. Grow the full tree (every leaf pure)

2. Generate a pruning sequence:
       Iteratively remove branches that cause the smallest increase in cost.
       This produces a sequence of trees from largest to smallest.

3. Pick the optimal tree using cross-validation
       Evaluate each candidate tree's CV error.
       Choose the one minimising error on unseen data.
```

---

## The Error-vs-Complexity Curve

Plotting validation error against tree size shows the classic pattern:

```
Error
  │     ___                  validation error
  │        \_              (red, dotted)
  │          \_         ___/
  │            \_   ___/
  │              \_/                ← minimum here
  │
  │       _____________________      training error
  │      ╱                          (blue) — always decreases
  │_____╱
  │___________________________________________ #leaves
        small        ↑           large
                 best tree
```

- Training error → decreases monotonically as tree grows
- Validation error → drops first, then **rises** as tree overfits
- The minimum of the validation curve = best balance

---

## Choosing the Tree

Two common rules:

### Minimum Error Tree

The tree corresponding to the lowest validation error. If multiple trees tie, pick the smallest (Occam's razor — simpler model wins).

### One-Standard-Error Rule

The smallest tree whose validation error is within **one standard error** of the minimum:

```
Best Pruned Tree = smallest tree with error ≤ min_error + 1 SE
```

This is preferred when the validation curve is flat near the minimum — slightly smaller trees generalise better with less variance in the estimate.

---

## sklearn

```python
from sklearn.tree import DecisionTreeClassifier

# Get the pruning path (all candidate α values and corresponding impurities)
clf = DecisionTreeClassifier(random_state=42)
path = clf.cost_complexity_pruning_path(X_train, y_train)
alphas = path.ccp_alphas

# Try each alpha
import pandas as pd
results = []
for a in alphas:
    m = DecisionTreeClassifier(ccp_alpha=a, random_state=42)
    m.fit(X_train, y_train)
    results.append({
        'alpha':   a,
        'leaves':  m.get_n_leaves(),
        'depth':   m.get_depth(),
        'train':   m.score(X_train, y_train),
        'test':    m.score(X_test,  y_test)
    })
print(pd.DataFrame(results))
```

Or use GridSearchCV directly on `ccp_alpha`.

---

## Pre-Pruning vs Post-Pruning

| | Pre-Pruning | Post-Pruning |
|-|-------------|--------------|
| When | During training | After training |
| Approach | Stop growth early | Grow fully, then cut |
| Hyperparameters | `max_depth`, `min_samples_*` | `ccp_alpha` |
| Speed | Faster | Slower (grows full tree first) |
| Risk | May underfit | More principled — sees the full picture |
| sklearn | All in constructor | `ccp_alpha` parameter |

In practice both are used together — set sensible pre-pruning bounds AND tune `ccp_alpha`.

---

## Summary

```
Cost = training error + α × number of leaves
α large → smaller tree
α small → larger tree

Procedure:
   1. Build full tree
   2. Generate pruning sequence
   3. Pick best α via CV

In sklearn: ccp_alpha parameter, tuned with GridSearchCV
```

> Post-pruning is the regularisation analogue for decision trees — same role α plays as λ does in Ridge.
