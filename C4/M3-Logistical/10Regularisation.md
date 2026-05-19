# Regularisation — L1 (Lasso) and L2 (Ridge)

A way to **prevent overfitting** by penalising large coefficients during fitting.

---

## The Problem

With many features and limited data, linear regression coefficients can blow up to fit noise in the training data. The model gets 100% on training but fails on test.

```
Train R² = 0.99   ← memorised training set
Test  R² = 0.45   ← can't generalise
```

A symptom: coefficients like β = [+500, −800, +1200, ...] — wildly large values that cancel each other on training data but explode on new data.

---

## The Fix

Don't just minimise the error — minimise error **plus** a penalty on the size of the coefficients:

```
Plain LR:        minimise SSE
Regularised:     minimise SSE + λ × (penalty on β)
```

The model now has to balance fitting the data against keeping coefficients small. **λ (lambda)** is the regularisation strength — a hyperparameter you tune.

---

## Where Do "L1" and "L2" Come From?

The number is the **power** β is raised to in the penalty:

```
L2 = β²    ← exponent 2  →  "L2 norm"
L1 = |β¹|  ← exponent 1  →  "L1 norm"
```

### The general pattern — Lp norms

```
L0 norm:  count of non-zero βᵢ        (theory only, hard to optimise)
L1 norm:  Σ |βᵢ|                       ← Lasso
L2 norm:  √(Σ βᵢ²)  →  squared form: Σ βᵢ²   ← Ridge
L∞ norm:  max(|βᵢ|)
```

### Why L1 and L2 are the standard ones

```
L1 (|β|)  → sparse — produces exact zeros (corner at β=0)
L2 (β²)   → smooth — shrinks but never to zero (smooth at β=0)
```

The derivative behaviour of |β| vs β² is what makes the difference — not arbitrary naming.

---

## Two Penalty Types

### L2 — Ridge

```
Penalty = λ × Σβᵢ²

Total cost: SSE + λ × Σβᵢ²
```

Squared penalty — shrinks all coefficients smoothly toward 0 but **never to exactly 0**.

### L1 — Lasso

```
Penalty = λ × Σ|βᵢ|

Total cost: SSE + λ × Σ|βᵢ|
```

Absolute value penalty — can drive some coefficients to **exactly 0**. Effectively performs **feature selection**.

---

## Geometric Intuition

Think of the cost function as contour lines and the penalty as a constraint region:

```
Ridge constraint (L2):  Σβ² ≤ t   →  circle (smooth boundary)
Lasso constraint (L1):  Σ|β| ≤ t  →  diamond (sharp corners)
```

The optimum is where the contour first touches the constraint region:
- **Circle (Ridge):** likely touched on a smooth part → both β₁ and β₂ are small but non-zero
- **Diamond (Lasso):** likely touched on a corner → some β is exactly 0

That's why L1 produces sparse solutions (zeroes) and L2 doesn't.

---

## Why Ridge Never Hits Exactly Zero (Calculus View)

The shape of the penalty's derivative tells you everything.

### Ridge — Smooth Penalty

Penalty term: **β²**. Its derivative is **2β**:

```
d(β²)/dβ = 2β

At β = 1.0   → gradient = 2.0   (strong pull toward 0)
At β = 0.1   → gradient = 0.2   (weak pull)
At β = 0.01  → gradient = 0.02  (very weak pull)
At β = 0     → gradient = 0     (no pull at all)
```

The pull toward zero **weakens as β shrinks**. As β approaches 0, the penalty's "force" also approaches 0 — so the data's pull always wins (even when tiny), and β asymptotes to zero but **never reaches it**.

```
        Ridge penalty:  β²

              ___
             /   \         smooth bowl
            /     \        gradient = 0 at β = 0
           /       \       β never gets stuck at 0
   ___ ___/         \___ ___
              β = 0
```

### Lasso — Non-Smooth Penalty

Penalty term: **|β|**. Its derivative is constant — **+1 or −1**:

```
d|β|/dβ = sign(β) = +1 if β > 0,  −1 if β < 0

At β = 1.0   → gradient = +1
At β = 0.1   → gradient = +1    (same!)
At β = 0.01  → gradient = +1    (same!)
At β = 0     → corner — gradient is undefined
```

The pull toward zero **never weakens**. If the data's force is less than λ, the penalty wins all the way down — β gets pushed to exactly 0 and **stays stuck there** at the corner.

```
        Lasso penalty:  |β|

              \   /         sharp V shape
               \ /          corner at β = 0
                V           β gets pinned here

              β = 0
```

### One-Line Summary

```
Ridge → smooth minimum at 0  → β approaches 0 asymptotically, never reaches it
Lasso → corner at 0          → β snaps to exactly 0 when penalty wins
```

---

## Effect of λ

| λ value | Behaviour |
|---------|-----------|
| λ = 0 | No penalty — same as plain LR |
| λ small | Light shrinkage |
| λ moderate | Balanced — usually best |
| λ very large | Coefficients near 0 — underfits |

There's a sweet spot. Find it with **cross-validation** (`GridSearchCV`).

---

## L1 vs L2 — When to Use Which

| | Ridge (L2) | Lasso (L1) |
|-|------------|------------|
| Shrinks toward 0 | Yes | Yes |
| Forces exact 0 | No | Yes |
| Feature selection | No | Yes |
| With correlated features | Distributes weight across them | Picks one, drops others |
| Use when | Many features all somewhat useful | Many features, want sparsity |

There's also **Elastic Net** — a mix of L1 and L2 — useful when you want both shrinkage and sparsity.

---

## Standardisation Matters

The penalty treats all coefficients equally — so if x₁ is in millions and x₂ is in percentages, the penalty hits x₁'s coefficient much harder by sheer scale.

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)   # mean=0, std=1 for each feature
```

**Always standardise features before regularising.**

---

## sklearn

```python
from sklearn.linear_model import Ridge, Lasso, ElasticNet

ridge = Ridge(alpha=1.0)       # alpha = λ
lasso = Lasso(alpha=0.1)
elnet = ElasticNet(alpha=0.1, l1_ratio=0.5)   # 50/50 mix of L1 and L2

ridge.fit(X_train, y_train)
ridge.coef_
```

Tune `alpha` with `GridSearchCV` — see `9CrossValidation.md`.

---

## Is Regularisation Always Applicable?

No — not always needed, and can hurt in some cases.

### When it helps

```
Many features (especially p > n)            → very likely needed
Multicollinearity (correlated features)     → Ridge stabilises
Small dataset                                → prevents overfitting
Noisy data                                   → reduces sensitivity
Need feature selection                       → Lasso
```

### When it doesn't help (or hurts)

```
Few features, lots of data    → plain LR is fine, regularisation just adds bias
Truly linear relationship     → no overfitting to prevent
You want exact coefficients   → regularisation biases them down
```

### The Bias-Variance Trade-off

Regularisation adds **bias** to reduce **variance**:

```
No regularisation     → low bias,  high variance  (may overfit)
Some regularisation   → moderate bias, lower variance  (often best)
Too much (λ huge)     → high bias, low variance  (underfits — predicts ≈ ȳ)
```

If your model isn't overfitting, you're adding bias for no benefit.

### How to Decide

Don't guess — let CV decide. Include `alpha=0` in the grid:

```python
GridSearchCV(Ridge(), {'alpha': [0, 0.001, 0.01, 0.1, 1, 10, 100]}, cv=5)
```

If CV picks 0 → your data didn't need it.

### Logistic Regression — Regularisation is On by Default

```python
LogisticRegression()              # L2 with C=1.0 (default)
LogisticRegression(penalty=None)  # disable regularisation
```

For small clean datasets with few features, disabling can give better results.

---

## p vs n — When You Need Regularisation

```
p = number of features (columns of X)
n = number of rows (samples)

p << n  →  "p is much less than n"  →  few features, many rows
```

### Examples

| Dataset | n | p | Verdict |
|---------|---|---|---------|
| Housing prices | 10,000 rows | 8 features | p << n — plenty of data |
| Gene expression | 100 patients | 20,000 genes | p >> n — regularisation essential |
| Survey data | 50,000 responses | 30 cols | p << n — plain LR fine |
| NLP bag-of-words | 5,000 docs | 50,000 words | p >> n — regularisation essential |

### Why It Matters

```
p << n (lots of data per feature)
   → model has enough signal to estimate each coefficient reliably
   → plain LR is fine

p ≈ n or p > n (few rows per feature)
   → model can perfectly memorise training data
   → coefficients become unreliable / explode
   → regularisation essential

p >> n (more features than rows)
   → OLS literally breaks — (XᵀX) is non-invertible
   → must use regularisation (Ridge / Lasso)
```

### Rule of Thumb

Aim for at least **10–20 rows per feature** before considering plain LR safe. Below that, regularise.

```
n / p ≥ 20   →  plain LR usually fine
n / p < 10   →  regularise
n / p < 1    →  must regularise (OLS doesn't even work)
```

> Start without regularisation, watch for overfitting (high train R², low test R²). Add regularisation if you see it.

---

## Summary

| Method | Penalty | Coefficients | Best for |
|--------|---------|--------------|----------|
| Linear | none | unrestricted, may explode | Few features, lots of data |
| Ridge (L2) | λ Σβ² | small but non-zero | Many features, all somewhat useful |
| Lasso (L1) | λ Σ\|β\| | many exactly 0 | Many features, want sparsity |
| Elastic Net | mix | mix | Want both shrinkage + sparsity |

> Regularisation is the standard tool for fighting overfitting in linear models.
