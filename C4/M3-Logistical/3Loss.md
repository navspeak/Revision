# Loss in Logistic Regression

Log-loss is the **cost function** for Logistic Regression — same role as MSE is for Linear Regression:

```
Linear Regression:    Cost = MSE      = (1/n) × Σ(y − ŷ)²
Logistic Regression:  Cost = Log-loss = −(1/n) × Σ[y log(p) + (1−y) log(1−p)]
```

Gradient descent minimises it the same way — compute partial derivatives of log-loss with respect to each β, nudge β in the direction that reduces it.

---

## Why Not MSE for Logistic Regression?

Linear Regression minimises SSE / MSE. Logistic Regression uses a different cost function because squaring the sigmoid produces a **non-convex** surface full of local minima — gradient descent would get stuck.

---

## Why Not Squared Error?

In Linear Regression, MSE produces a smooth bowl — one global minimum gradient descent can always find.

After wrapping in sigmoid, squaring creates a bumpy, non-convex surface:

```
MSE after sigmoid:

Loss
  │      /\      /\
  │    /    \  /    \
  │  /  bad  \/  bad
  │/___________________
        β values
   Multiple local minima — gradient descent gets stuck
```

The fix: use a loss function designed for probabilities — **log-loss**.

---

## Likelihood

Before log-loss, understand **likelihood**.

The model outputs P(y=1 | X) = p. For a single training example:

```
If actual label y = 1:   want high p  → likelihood = p
If actual label y = 0:   want low p   → likelihood = 1 − p
```

Combined into one formula:

```
likelihood = p^y × (1−p)^(1−y)

y = 1: p¹ × (1−p)⁰ = p           ← want this high
y = 0: p⁰ × (1−p)¹ = 1−p         ← want this high
```

For all n training examples:

```
Likelihood = ∏ᵢ [ pᵢ^yᵢ × (1−pᵢ)^(1−yᵢ) ]
```

**Goal:** find β that maximises this product — **Maximum Likelihood Estimation (MLE)**.

---

## Log-Likelihood

Products are hard to optimise (small floating-point numbers, overflow). Apply log:

```
log-likelihood = Σᵢ [ yᵢ log(pᵢ) + (1−yᵢ) log(1−pᵢ) ]
```

Maximising log-likelihood is equivalent to maximising likelihood (log is monotonic).

---

## Log-Loss (Binary Cross-Entropy)

Gradient descent **minimises** loss, so negate the log-likelihood:

```
Log-Loss = −(1/n) × Σᵢ [ yᵢ log(pᵢ) + (1−yᵢ) log(1−pᵢ) ]
```

This is also called **binary cross-entropy**.

### Step-by-Step Example

3 training examples:

| i | yᵢ (actual) | pᵢ = P(y=1) | yᵢ log(pᵢ) | (1−yᵢ) log(1−pᵢ) | Sum |
|---|------------|-------------|------------|-------------------|-----|
| 1 | 1 | 0.9 | 1×log(0.9) = −0.105 | 0×log(0.1) = 0 | −0.105 |
| 2 | 0 | 0.2 | 0×log(0.2) = 0 | 1×log(0.8) = −0.223 | −0.223 |
| 3 | 1 | 0.6 | 1×log(0.6) = −0.511 | 0×log(0.4) = 0 | −0.511 |

```
Log-Loss = −(1/3) × (−0.105 + (−0.223) + (−0.511))
         = −(1/3) × (−0.839)
         = 0.280
```

---

## What Log Does to Probabilities

```
log(p) as p → 1:   log(1.0)  =  0.0     ← no penalty, correct and confident
log(p) at p = 0.5: log(0.5)  = −0.693
log(p) as p → 0:   log(0.01) = −4.605   ← heavy penalty, wrong and confident
```

The loss grows **non-linearly**: being confidently wrong is punished very heavily.

```
y=1, predict p=0.99:  loss ≈ 0.01   (correct, confident)
y=1, predict p=0.50:  loss ≈ 0.69   (uncertain)
y=1, predict p=0.01:  loss ≈ 4.61   (wrong, confident — punished hard)
```

---

## MLE

**Maximum Likelihood Estimation (MLE)** is the principle:

> Find the parameters β that make the observed training data most probable.

In practice:
- Write out the likelihood function for all training examples
- Apply log (for numerical stability)
- Negate (to turn maximisation into minimisation)
- Use gradient descent to find β that minimises log-loss

This is what `model.fit()` does internally for Logistic Regression.

---

## Convexity

Log-loss is **convex** — one global minimum, no local minima. Gradient descent is guaranteed to find it.

```
Log-Loss surface:

Loss
  │\            /
  │  \        /
  │    \    /
  │      \/
  │___________
      β values
   Single global minimum ✓
```

---

## Comparison with Linear Regression

| | Linear Regression | Logistic Regression |
|-|-------------------|---------------------|
| Loss | MSE = Σ(y−ŷ)²/n | Log-loss = −mean[y log(p) + (1−y) log(1−p)] |
| Why | Squared error is convex for linear output | MSE is non-convex after sigmoid |
| Optimisation | OLS (closed-form) or gradient descent | Gradient descent only |
| Minimises | Residuals | Log-likelihood (via MLE) |

---

## Binary vs Multiclass Cross-Entropy

Log-loss / binary cross-entropy works for both — with different formulas:

### Binary (2 classes)

```
Log-loss = −(1/n) × Σ [y log(p) + (1−y) log(1−p)]
```

One probability p = P(y=1). The other class is just 1−p.

### Multiclass — Categorical Cross-Entropy

```
Log-loss = −(1/n) × Σᵢ Σₖ yᵢₖ log(pᵢₖ)
```

- i = each sample
- k = each class
- yᵢₖ = 1 if sample i belongs to class k, else 0  (one-hot)
- pᵢₖ = predicted probability for class k

### Example — 3 classes

```
Actual: class 1  →  y = [0, 1, 0]   (one-hot)
Predicted probs:      p = [0.1, 0.7, 0.2]

Loss = −(0×log(0.1) + 1×log(0.7) + 0×log(0.2))
     = −log(0.7)
     = 0.357
```

Only the probability of the **correct class** contributes — zeros cancel everything else out.

| | Binary Cross-Entropy | Categorical Cross-Entropy |
|-|---------------------|--------------------------|
| Classes | 2 | 3+ |
| Formula | −[y log(p) + (1−y) log(1−p)] | −Σₖ yₖ log(pₖ) |
| y format | 0 or 1 | one-hot vector |
| Same idea? | Yes — binary is just a special case of categorical |

---

## sklearn

The API is the **same for binary and multiclass** — sklearn handles it automatically:

```python
from sklearn.metrics import log_loss

# Binary
loss = log_loss(y_true, y_prob)           # y_prob shape: (n, 2)

# Multiclass — identical call
loss = log_loss(y_true, y_prob)           # y_prob shape: (n, k)
```

`log_loss` detects the number of classes from `y_prob` and applies the right formula internally.

```python
# Full example
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss

model = LogisticRegression()
model.fit(X_train, y_train)

y_prob = model.predict_proba(X_test)      # (n, 2) binary or (n, k) multiclass
loss   = log_loss(y_test, y_prob)         # same call either way
```

Log-loss is available in `sklearn.metrics` but not shown by default — `model.score()` and `classification_report` don't include it. You must call `log_loss()` explicitly.

Lower is better. Thumb rules:

```
log-loss = 0      → theoretically perfect, never seen in practice
log-loss < 0.2    → very good
log-loss < 0.5    → decent
log-loss > 1.0    → poor
log-loss = 0.693  → baseline (random model always predicting 0.5 for binary)
```

> Beat 0.693 for binary classification to be better than random guessing.

---

## Full Python Example

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
import numpy as np

# Sample data
X = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])
y = np.array([0, 0, 0, 0, 1, 1, 1, 1])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Fit model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)             # class labels — 0 or 1
y_prob = model.predict_proba(X_test)       # probabilities — shape (n, 2)

# Log-loss
loss = log_loss(y_test, y_prob)
print(f"Log-loss: {loss:.4f}")             # lower is better, beat 0.693

# Manual log-loss to see what sklearn computes
p = y_prob[:, 1]                           # P(y=1) for each sample
manual_loss = -np.mean(y_test * np.log(p) + (1 - y_test) * np.log(1 - p))
print(f"Manual log-loss: {manual_loss:.4f}")   # same as log_loss()
```
