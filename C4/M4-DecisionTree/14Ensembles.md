# Ensembles — Why a Forest Beats a Single Tree

A single decision tree is **interpretable but unstable** — small changes in training data lead to very different trees. The fix: combine **many trees** into one prediction.

```
Single tree   → high variance, unstable
Many trees    → average them → stable, accurate
```

This is the **ensemble idea**: collect many "okay" models and combine them into one strong model. It's the foundation of almost every state-of-the-art tabular ML system today.

---

## Why Ensembles Work

### The intuition — wisdom of crowds

```
Ask one person to guess the number of jellybeans in a jar → noisy guess
Ask 1000 people and take the average    → very close to truth
```

Each person makes some error, but errors **cancel out** when averaged. The crowd is wiser than the individual.

### In ML terms — bias and variance

```
Single deep tree:
   low bias    (fits training data well)
   high variance (very sensitive to changes in data)

Average of many deep trees:
   low bias    (still fits well)
   LOW variance (errors cancel out across trees)
```

Ensembles **reduce variance** without increasing bias — best of both worlds.

For this to work, the individual trees should:
- Be **accurate enough** (better than random)
- Be **diverse** — make different mistakes, so errors cancel

If all trees are identical, averaging doesn't help. Diversity is the key.

---

## How to Get Diverse Trees

Two main strategies, each leading to a different ensemble family:

### Bagging (Bootstrap Aggregating)

Train each tree on a **different random sample** of the data:

```
Training data: 1000 rows

Tree 1: trained on 1000 rows sampled WITH replacement (bootstrap)
Tree 2: trained on 1000 rows sampled WITH replacement
...
Tree N: same
```

Each tree sees a slightly different dataset → makes slightly different decisions.

For classification, **majority vote** across trees. For regression, **average** the predictions.

### Random Subspaces

Each tree only considers a **random subset of features** at each split:

```
At each split:
   instead of considering all 30 features
   only consider a random 5 features
```

This forces trees to use different features, increasing diversity beyond just bootstrap.

---

## Random Forest = Bagging + Random Subspaces

The most popular ensemble:

```
Random Forest:
   1. Train N trees (typically 100-500)
   2. Each tree:
        - Uses a bootstrap sample of training data
        - At each split, considers a random subset of features
   3. Final prediction:
        - Classification: majority vote
        - Regression: mean of tree predictions
```

```
                  ┌──────────────────────────┐
   New point ──→  │  Tree 1   Tree 2 ... TreeN │  ──→  Average / Vote ──→  Final prediction
                  └──────────────────────────┘
```

### Why it's so popular

```
✓ Robust to overfitting (averaging cancels per-tree noise)
✓ Handles non-linearity natively (it's still trees)
✓ Works on mixed data types
✓ No feature scaling needed
✓ Built-in feature importance
✓ Almost no hyperparameter tuning needed (defaults often work)
✓ Parallelisable (each tree is independent)
```

In sklearn:

```python
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
```

---

## Boosting — A Different Approach

Boosting trains trees **sequentially**, with each new tree correcting the previous tree's mistakes:

```
Tree 1: predict y → some errors
Tree 2: train to fix Tree 1's errors → reduces residual error
Tree 3: train to fix Tree 1+2's combined errors
...
Final prediction = weighted sum of all trees
```

Whereas Bagging trees are **independent**, Boosting trees are **dependent** — each builds on the previous.

### Common boosting algorithms

| Algorithm | sklearn module | Notes |
|-----------|---------------|-------|
| AdaBoost | `AdaBoostClassifier` | Classic, simple to understand |
| Gradient Boosting | `GradientBoostingClassifier` | More powerful, used widely |
| XGBoost | `xgboost` (3rd party) | State-of-the-art, fast |
| LightGBM | `lightgbm` (3rd party) | Microsoft's, very fast |
| CatBoost | `catboost` (3rd party) | Handles categorical features natively |

These dominate Kaggle competitions and production ML on tabular data.

---

## Bagging vs Boosting

| | Bagging (Random Forest) | Boosting (GBM, XGBoost) |
|-|------------------------|------------------------|
| Training | Parallel — trees independent | Sequential — each fixes the previous |
| Reduces | Variance | Bias |
| Risk | Less overfitting | More overfitting if tuned poorly |
| Speed | Fast (parallel) | Slower (sequential) |
| Tuning | Few hyperparameters | Many hyperparameters |
| Accuracy ceiling | Good | Often higher |
| Trees used | Deep trees | Shallow trees (depth 3-6) |

In practice:
- **Random Forest** → strong baseline, low effort, robust
- **Gradient Boosting / XGBoost** → highest accuracy, needs tuning

---

## What Ensembles Lose

The big trade-off: **interpretability**.

```
Single tree    → can be drawn, rules read off
100 trees      → no longer one set of rules → hard to explain
```

You still get **feature importance** (averaged across trees), but the full decision path is gone. For deeply interpretable models, you still want a single tree.

```
Need interpretability  → single Decision Tree
Need accuracy          → Random Forest / Gradient Boosting
```

---

## Why Decision Trees Matter Even Though Single Trees Are Rarely Used

Even though single trees are rarely the best predictor:

- **They're the building block** of every ensemble
- **Understanding splits, impurity, pruning** carries directly into Random Forest, XGBoost, LightGBM
- **No ensemble works without understanding the base learner first**

> Master single trees → ensembles become a natural extension.

---

## Summary

```
Single tree           → interpretable, unstable
Bagging (RF)          → many trees on random samples → averages out variance
Boosting (XGBoost)    → many trees in sequence → reduces residual error
Both reduce error far below single tree, at cost of interpretability
```

| Method | Strategy | Typical use |
|--------|----------|-------------|
| Decision Tree | One tree | Interpretability |
| Random Forest | Bagging + random subspaces | Strong baseline |
| Gradient Boosting | Sequential error correction | Highest accuracy |
| AdaBoost | Reweighting mistakes | Classic, educational |

> Decision Trees → foundation. Ensembles → the real power of tree-based methods.
