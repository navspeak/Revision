# Other Ensemble Methods — Beyond Bagging and Basic Boosting

Ensembles aren't just Random Forest and basic Gradient Boosting. There's a wider family of techniques and a small zoo of optimised boosting libraries that dominate modern tabular ML.

---

## Stacking — A Different Way to Combine Models

So far we've combined models of the **same type** (many trees). **Stacking** combines outputs from **different model types** via a meta-learner.

```
Layer 1 (base models):
   Logistic Regression  → prediction_LR
   Random Forest        → prediction_RF
   SVM                  → prediction_SVM
   Neural Network       → prediction_NN

Layer 2 (meta-learner):
   Take all four predictions as features
   Train another model (often Logistic Regression) to combine them
   → final prediction
```

The meta-learner **learns when to trust each base model**. If Logistic Regression is best for certain types of inputs and Random Forest for others, the meta-learner can figure that out.

### When stacking helps

```
✓ Different models capture different patterns
✓ You have enough data to train a meta-model robustly
✓ Maximum accuracy matters more than simplicity
```

### Downsides

```
✗ More complex to implement and maintain
✗ Risk of overfitting the meta-learner
✗ Slow at prediction time (need to run all base models)
✗ Hard to interpret
```

sklearn provides `StackingClassifier` and `StackingRegressor`:

```python
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

base = [
    ('lr', LogisticRegression()),
    ('rf', RandomForestClassifier()),
    ('svm', SVC(probability=True))
]
stack = StackingClassifier(estimators=base, final_estimator=LogisticRegression())
stack.fit(X_train, y_train)
```

---

## Subsampling Methods

A general principle: **diversity comes from showing different data / features** to each model.

| Method | Diversity from |
|--------|---------------|
| Bagging | Random row sampling (bootstrap) |
| Random Subspaces | Random feature sampling |
| Random Patches | Both rows and features sampled |
| Random Forest | Bagging + per-split feature subsetting |

Random Forest is the most popular member of this family — it pulls all these tricks together.

---

## AdaBoost — The Original Boosting Method

**AdaBoost (Adaptive Boosting)**, 1995. The simpler ancestor of Gradient Boosting.

```
Idea: reweight TRAINING POINTS based on whether previous models got them right.

Round 1: Train weak learner on equally-weighted data
         Identify misclassified points → INCREASE their weight
Round 2: Train weak learner on reweighted data (focuses on hard cases)
         Identify still-misclassified points → INCREASE their weight again
Round 3: ...
```

Each model focuses harder on examples that previous models kept getting wrong. The final prediction is a **weighted vote** where better-performing models get more say.

### Key features

```
✓ Simple and intuitive
✓ Works well on clean data
✓ Effective even with very weak learners (decision stumps — depth 1)
✗ Sensitive to noisy data — outliers get reweighted up and dominate
✗ Mostly replaced by Gradient Boosting in practice
```

In sklearn:

```python
from sklearn.ensemble import AdaBoostClassifier

model = AdaBoostClassifier(n_estimators=50, learning_rate=1.0, random_state=42)
```

### AdaBoost vs Gradient Boosting

```
AdaBoost:        reweights data points based on errors
Gradient Boost:  fits new trees to the residuals (gradients) of the loss
```

Both are "sequential error correction" — different implementations of the same idea.

---

## XGBoost — eXtreme Gradient Boosting

The boosting library that **won Kaggle for years**. Published 2014.

```
Same Gradient Boosting concept, with serious engineering improvements:

✓ Built-in L1 and L2 regularisation on tree weights
✓ Parallel tree construction (within each tree, not across)
✓ Sparse-aware split finding — efficient on sparse data
✓ Handles missing values natively (chooses best direction at each split)
✓ Early stopping built in
✓ Distributed training support
✓ GPU acceleration
```

These optimisations made XGBoost **dramatically faster** and **more accurate** than vanilla gradient boosting.

```python
import xgboost as xgb

model = xgb.XGBClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=5,
    reg_alpha=0.1,        # L1 regularisation
    reg_lambda=1.0,       # L2 regularisation
    random_state=42
)
model.fit(X_train, y_train, eval_set=[(X_val, y_val)], early_stopping_rounds=20)
```

Industry standard for tabular ML for years.

---

## LightGBM — Microsoft's Speed Champion

Published 2016 by Microsoft. **Faster** than XGBoost on most datasets, with comparable accuracy.

```
Two key innovations:

1. Histogram-based splitting:
   Bin continuous features into discrete buckets (e.g. 256 bins).
   Searching for the best split = scanning buckets, not raw values.
   Much faster, much less memory.

2. Leaf-wise growth (vs level-wise):
   - Level-wise (XGBoost/sklearn): grow ALL leaves at depth k before going to k+1.
   - Leaf-wise (LightGBM): grow ONLY the leaf that reduces loss most.
   → asymmetric trees that fit the data more precisely.
```

This makes LightGBM **scale to millions of rows** while staying fast and using less RAM.

```python
from lightgbm import LGBMClassifier

model = LGBMClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=-1,        # no limit (rely on num_leaves instead)
    num_leaves=31,       # leaf-wise growth → control via leaf count, not depth
    random_state=42
)
```

### Trade-off

Leaf-wise growth is more aggressive — can **overfit faster than XGBoost** if not regularised. Use `min_data_in_leaf`, `num_leaves`, and early stopping carefully.

---

## CatBoost — Native Categorical Handling

Published 2017 by Yandex. The category specialist.

```
Standard approach to categoricals:
   - One-hot encode → explodes feature count for high-cardinality features
   - Or label encode → arbitrary ordering, often hurts performance

CatBoost approach:
   - Handles categorical features directly with built-in target encoding
   - Uses a clever ordered-boosting scheme to avoid target leakage
```

### Key features

```
✓ No need to one-hot encode categoricals
✓ Strong default hyperparameters — often works well "out of the box"
✓ Robust to overfitting via "ordered boosting"
✓ GPU acceleration
✓ Less sensitive to hyperparameter tuning than XGBoost
```

```python
from catboost import CatBoostClassifier

model = CatBoostClassifier(
    iterations=200,
    learning_rate=0.1,
    depth=6,
    cat_features=['city', 'category'],   # tell it which features are categorical
    verbose=0,
    random_state=42
)
```

Particularly strong when you have **lots of categorical features** (e.g. user IDs, product categories).

---

## Summary — When to Use Which

| Library | Best for | Speed | Tuning effort |
|---------|----------|-------|---------------|
| **AdaBoost** | Educational, simple problems | Medium | Low |
| **sklearn GBM** | Light use, baseline | Slow | Medium |
| **XGBoost** | Industry standard, lots of features | Fast | Medium-high |
| **LightGBM** | Big data, fastest training | Very fast | Medium |
| **CatBoost** | Many categorical features | Fast | Low (good defaults) |
| **Random Forest** | Easy baseline, robust | Fast | Low |
| **Stacking** | Maximum accuracy, no time constraint | Slow | High |

---

## The Bigger Picture

All of these methods share **one core idea**: combining learners produces stronger and more reliable predictions than any single model. They differ in:

- **How** models are combined (parallel, sequential, meta-learner)
- **What** kind of diversity they create (data, features, model types)
- **Which** errors they target (variance vs bias)

```
Bagging family:       Random Forest, Random Subspaces, Extra Trees
Boosting family:      AdaBoost, GBM, XGBoost, LightGBM, CatBoost
Stacking family:      different model types + meta-learner
```

The principle is the same. The implementation choices give you a tool for every situation.

---

## In Practice

For most tabular problems:

```
Quick baseline       → Random Forest
Want better accuracy → LightGBM or XGBoost
Many categoricals    → CatBoost
Maximum ceiling      → Stack RF + XGBoost + LightGBM
```

> All variants exist because real-world data is varied — different speeds, sizes, and feature types call for different tools. The ensemble principle binds them all.
