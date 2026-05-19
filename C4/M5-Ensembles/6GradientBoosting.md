# Gradient Boosting

The most important boosting algorithm. Builds models sequentially, with each new model **fitting the residuals** (errors) of the combined ensemble so far.

```
Random Forest:   trees built INDEPENDENTLY in parallel
Gradient Boost:  trees built in a CHAIN, each correcting prior mistakes
```

---

## The Mechanics — Step by Step

### Step 1 — Baseline prediction

Start with a simple model — often just the **mean of the target** (for regression):

```
ŷ(1) = mean(y_train)
```

For all training points, the initial prediction is the same.

### Step 2 — Compute residuals

Residual = actual − predicted:

```
e(1) = y − ŷ(1)
```

These are what the next learner needs to predict.

### Step 3 — Train a learner on the residuals

Fit a small tree (typically depth 3–6) whose target is `e(1)`. Its prediction is `ê(1)`.

### Step 4 — Update the ensemble

```
ŷ(2) = ŷ(1) + ν × ê(1)
```

Where ν (nu) is the **learning rate** — a small number like 0.1. This controls how much to trust each new tree.

### Step 5 — Repeat

```
Compute new residuals:  e(2) = y − ŷ(2)
Train next tree on:     e(2)
Update:                 ŷ(3) = ŷ(2) + ν × ê(2)
...
```

Continue for M rounds. The final prediction:

```
ŷ(M) = ŷ(1) + ν × Σ ê(i)
```

A weighted sum of every tree's contribution — that's the ensemble.

---

## Worked Example — House Prices

Target value: $300,000.

```
Step 1: baseline = mean of training prices ≈ $250,000
        residual = $50,000

Step 2: Tree 2 predicts residual = $40,000
        ensemble = $250,000 + 0.1 × $40,000 = $254,000
        new residual = $46,000

Step 3: Tree 3 predicts residual = $35,000
        ensemble = $254,000 + 0.1 × $35,000 = $257,500
        new residual = $42,500

... continue many rounds ...

Final ensemble ≈ $300,000   (after many small corrections)
```

Each step nudges the prediction closer. The learning rate (`ν = 0.1`) controls how cautious those nudges are.

---

## Why "Gradient"?

The name comes from interpreting **residuals as the negative gradient of a loss function**:

```
For MSE loss L = (y − ŷ)² / 2:

   dL/dŷ = −(y − ŷ) = −residual
```

So fitting a tree to the **residual** is mathematically equivalent to taking a step in the direction of the **negative gradient** of the loss.

This generalises:
- For MSE → tree fits residuals (y − ŷ)
- For log-loss → tree fits something more complex but mathematically a gradient
- For any differentiable loss → there's a "gradient" the tree fits

That's why it's called **gradient** boosting — it's gradient descent in function space.

---

## Learning Rate (ν)

The single most important hyperparameter.

```
ν = 1.0    → each tree's prediction added at full strength → fast learning, easy to overfit
ν = 0.1    → typical default — each tree contributes 10%
ν = 0.01   → very cautious — needs many more trees, often best for accuracy
```

There's a trade-off:

```
Smaller learning rate → more trees needed → slower but often better generalisation
Larger learning rate  → fewer trees needed → faster but more overfitting
```

Standard practice: **use a small learning rate (0.01–0.1) and let the number of trees be large** — with early stopping to find the right number.

---

## Classification vs Regression

The mechanics are nearly identical:

- **Regression** → trees fit numerical residuals
- **Classification** → trees fit gradients of log-loss (related to probability residuals)

The output is a probability that's then thresholded for classification — same as Logistic Regression.

---

## Why It's So Powerful

Each tree handles a small piece of the problem:

```
Tree 1: gets the gross pattern (mean)
Tree 2: gets remaining bias
Tree 3: refines further
...
Tree 100: cleans up tiny residual errors
```

This **targeted error correction** is what makes gradient boosting often the top performer on tabular data. XGBoost, LightGBM, and CatBoost are engineering optimisations of this same idea — they don't change the core algorithm.

---

## sklearn

```python
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor

model = GradientBoostingClassifier(
    n_estimators=100,       # number of trees
    learning_rate=0.1,      # ν
    max_depth=3,            # shallow trees (weak learners)
    random_state=42
)
model.fit(X_train, y_train)
```

For state-of-the-art: use `xgboost`, `lightgbm`, or `catboost` libraries — same algorithm, much faster and with extra features.

---

## Summary

```
Gradient Boosting =
   1. Start with a baseline prediction (often the mean)
   2. Compute residuals: e = y − ŷ
   3. Train a tree to predict e
   4. Add it to the ensemble: ŷ ← ŷ + ν × tree_prediction
   5. Repeat with new residuals

Key idea:    sequentially fit residuals using shallow trees
Magic:       trees correct each other's mistakes step by step
Trade-off:   higher accuracy than RF, but slower and easier to overfit
Tuning:      learning rate × number of trees is the key trade-off
```

> Gradient Boosting is the **highest-performing tabular method** when tuned carefully. XGBoost / LightGBM / CatBoost dominate Kaggle for a reason.
