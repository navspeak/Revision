# Logistic Regression

Logistic Regression is a **classification** model despite the name. It outputs a probability between 0 and 1, then applies a threshold to produce a class label.

---

## The Core Problem

Linear regression gives:

```
ŷ = β₀ + β₁x₁ + β₂x₂ + ...
```

This can produce any value (−∞ to +∞). For classification we need a value between 0 and 1. The fix is the **sigmoid function**.

---

## Sigmoid Function

The sigmoid squashes any real number into (0, 1):

```
σ(z) = 1 / (1 + e⁻ᶻ)

where z = β₀ + β₁x₁ + β₂x₂ + ...   ← the linear combination
```

### Shape

```
σ(z)
 1.0 |           ___________
     |         /
 0.5 |--------/-------------- ← threshold
     |      /
 0.0 |_____/
          z = 0
     ←-----|-----→
     z → −∞      z → +∞
     σ → 0        σ → 1
```

| z | σ(z) |
|---|------|
| −∞ | → 0 |
| −2 | 0.12 |
| 0 | 0.50 |
| +2 | 0.88 |
| +∞ | → 1 |

At z = 0: σ = 0.5 exactly — the decision boundary.

---

## σ(z) vs y — Why Not Call It y?

| Symbol | What it is |
|--------|------------|
| `y` | The **actual label** — 0 or 1, from your training data |
| `σ(z)` | The **model's output** — a probability between 0 and 1 |

`y` is not output — **y is what you're trying to predict**. `σ(z)` is the model's best guess at P(y = 1).

```
Training data:  X (features)  and  y (actual label, the truth)
Model produces: σ(z)               ← estimated probability
```

In sklearn terms:

```python
y_prob = model.predict_proba(X_test)  # σ(z) — raw probability, e.g. 0.82
y_pred = model.predict(X_test)        # ŷ — class label after threshold (0 or 1)
# y                                   # actual truth from data
```

- `σ(z)` = continuous probability (0.82)
- `ŷ` = class label after threshold (0.82 ≥ 0.5 → ŷ = 1)
- `y` = actual ground truth

The notation `σ(z)` is used in the formula stage because at that point you haven't applied the threshold yet — it's still a probability, not a class label.

---

## From Linear to Logistic

```
Step 1: compute z = β₀ + β₁x₁ + ...   (linear combination)
Step 2: apply sigmoid → P(y=1 | X) = σ(z)   (probability)
Step 3: apply threshold → class label
```

### Example

```
z = −1.5 + 0.8 × Hours_studied

Student studies 3 hours:
  z = −1.5 + 0.8 × 3 = −1.5 + 2.4 = 0.9
  σ(0.9) = 1 / (1 + e⁻⁰·⁹) = 0.71

  P(Pass | 3 hours) = 71%
  Since 0.71 ≥ 0.5 → predict Pass
```

---

## Decision Threshold

Default threshold is **0.5**:

```
P(y=1) ≥ 0.5  →  predict class 1
P(y=1) < 0.5  →  predict class 0
```

You can adjust the threshold depending on the problem:

| Situation | Threshold | Why |
|-----------|-----------|-----|
| Cancer detection | Lower (0.3) | Missing a case is worse than a false alarm |
| Spam filter | Higher (0.7) | Better to miss spam than block real email |
| Balanced problem | 0.5 | Default |

The threshold does **not** change the model — it only changes where you draw the line on the probability output.

---

## Multiclass: One-vs-Rest

Binary LR handles 2 classes. For 3+ classes use **One-vs-Rest (OvR)**:

```
3 classes: Dog, Cat, Bird

Train 3 binary classifiers:
  Classifier 1: Dog vs (Cat + Bird)
  Classifier 2: Cat vs (Dog + Bird)
  Classifier 3: Bird vs (Dog + Cat)

For a new input:
  P(Dog)  = 0.70
  P(Cat)  = 0.20
  P(Bird) = 0.10
  → predict Dog (highest probability)
```

sklearn uses OvR automatically when you have more than 2 classes.

---

## Multiclass: Softmax

Softmax is the natural multiclass extension — it outputs a valid **probability distribution** over all classes (all probabilities sum to 1):

```
P(class k) = e^(zₖ) / Σⱼ e^(zⱼ)

Example with 3 classes, raw scores z = [2.0, 1.0, 0.1]:
  e^2.0 = 7.39,  e^1.0 = 2.72,  e^0.1 = 1.10
  sum   = 11.21

  P(Dog)  = 7.39 / 11.21 = 0.659
  P(Cat)  = 2.72 / 11.21 = 0.243
  P(Bird) = 1.10 / 11.21 = 0.098
                           -----
                           1.000 ✓
```

| | OvR | Softmax |
|-|-----|---------|
| How | K separate binary classifiers | Single classifier with K outputs |
| Probabilities sum to 1? | Not guaranteed | Always |
| Speed | Parallelisable | Single pass |
| sklearn | `multi_class='ovr'` | `multi_class='multinomial'` |

---

## sklearn API

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred       = model.predict(X_test)          # class labels
y_prob       = model.predict_proba(X_test)    # probabilities for each class
y_prob[:, 1]                                  # P(class 1) for binary
```

### predict_proba is the sigmoid

`predict_proba` internally applies sigmoid to the linear combination z:

```python
# What sklearn does internally:
z    = X_test @ model.coef_.T + model.intercept_
prob = 1 / (1 + np.exp(-z))   # sigmoid = predict_proba
```

For binary classification it returns two columns:

```
y_prob shape: (n_samples, 2)
y_prob[:, 0]  → P(class 0) = 1 − σ(z)
y_prob[:, 1]  → P(class 1) = σ(z)      ← sigmoid output
```

The two columns always sum to 1 for each row.

---

### predict vs predict_proba

```
predict_proba → probability (continuous, 0 to 1)
predict       → class label (discrete, 0 or 1)
```

```python
y_prob = model.predict_proba(X_test)
# [[0.18, 0.82],   ← 18% fail, 82% pass
#  [0.71, 0.29],   ← 71% fail, 29% pass
#  [0.45, 0.55]]   ← 45% fail, 55% pass

y_pred = model.predict(X_test)
# [1,   ← 0.82 ≥ 0.5 → Pass
#  0,   ← 0.29 < 0.5 → Fail
#  1]   ← 0.55 ≥ 0.5 → Pass
```

`predict` is just a shortcut — these two are equivalent:

```python
y_pred = model.predict(X_test)
y_pred = (model.predict_proba(X_test)[:, 1] >= 0.5).astype(int)
```

| | `predict_proba` | `predict` |
|-|-----------------|-----------|
| Output | Float 0–1 | Integer 0 or 1 |
| Shape | (n, 2) | (n,) |
| Use when | Need confidence / adjust threshold | Just need the class label |

**For basic use, `predict` is enough.** Use `predict_proba` only when:
- Adjusting the threshold (e.g. 0.3 for cancer detection)
- You need the confidence score itself
- Computing log_loss (requires probabilities, not labels)

---

## Binary Classification — The Basic Case

The foundation of Logistic Regression is binary classification — y contains only 0 or 1:

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)        # y_train contains 0s and 1s

y_pred = model.predict(X_test)    # returns 0s and 1s
```

The full flow:

```
X_train, y_train (0/1)
        ↓
  model.fit()          ← learns β₀, β₁, β₂ ... that best separate the two classes
        ↓
  model.predict()      ← for each row: z → sigmoid → ≥0.5? → 1 else 0
        ↓
  y_pred (0s and 1s)
```

Same sklearn pattern as Linear Regression — only what happens inside `fit()` changes:

| | Linear Regression | Logistic Regression |
|-|-------------------|---------------------|
| `fit()` | finds β that minimises MSE | finds β that minimises log-loss |
| `predict()` | returns a number | returns 0 or 1 |
| output | continuous | binary |

---

## Multiclass

In multiclass, `y` contains more than 2 values — say 0, 1, 2. The API is **identical** — only `y` changes:

```python
model = LogisticRegression()
model.fit(X_train, y_train)        # y_train contains 0, 1, 2

y_pred = model.predict(X_test)    # returns 0, 1, or 2
```

### What happens inside fit()

sklearn automatically uses One-vs-Rest — trains 3 binary classifiers:

```
Classifier 1: Is it class 0?  →  P(class 0) = σ(z₀)
Classifier 2: Is it class 1?  →  P(class 1) = σ(z₁)
Classifier 3: Is it class 2?  →  P(class 2) = σ(z₂)
```

### What happens inside predict()

Pick the class with the highest probability:

```python
y_prob = model.predict_proba(X_test)
# [[0.10, 0.70, 0.20],   ← predict class 1
#  [0.60, 0.15, 0.25],   ← predict class 0
#  [0.05, 0.20, 0.75]]   ← predict class 2

y_pred = model.predict(X_test)
# [1, 0, 2]
```

`predict_proba` now returns **k columns** — one per class — summing to 1 across each row.

| | Binary | Multiclass |
|-|--------|------------|
| y values | 0, 1 | 0, 1, 2, ... |
| predict output | 0 or 1 | 0, 1, 2, ... |
| predict_proba shape | (n, 2) | (n, k) |
| Code change | — | none — sklearn handles it |

---

## OvR vs Softmax

Two strategies for multiclass — both supported by sklearn:

### OvR (One-vs-Rest) — default
Trains k separate binary classifiers, one per class:

```
3 classes → 3 classifiers, each answers "is it this class or not?"
Each outputs its own probability independently
Probabilities don't have to sum to 1
```

### Softmax (Multinomial)
Trains one single classifier with k outputs:

```
3 classes → 1 classifier, outputs 3 probabilities at once
Probabilities always sum to 1 (proper distribution)
```

```python
model = LogisticRegression(multi_class='ovr')            # OvR (default)
model = LogisticRegression(multi_class='multinomial',
                           solver='lbfgs')               # Softmax
```

| | OvR | Softmax |
|-|-----|---------|
| Classes independent? | Yes — each trained separately | No — all classes compete |
| Probabilities sum to 1? | Not guaranteed | Always |
| Speed | Parallelisable | Single pass |
| Default in sklearn | Yes | No |

For most problems OvR works fine. Softmax is preferred when classes are **mutually exclusive** and you want proper probabilities (e.g. digit recognition — an image is exactly one digit).

---

## Summary

| Step | What happens |
|------|-------------|
| z = β₀ + β₁x | Linear combination (same as linear regression) |
| σ(z) = 1/(1+e⁻ᶻ) | Sigmoid squashes z to (0, 1) |
| P(y=1) = σ(z) | Interpret as probability |
| P ≥ threshold → class 1 | Apply decision boundary |

> The only difference from linear regression is the sigmoid wrapper. Everything else — coefficients, fitting, prediction — follows the same sklearn pattern.
