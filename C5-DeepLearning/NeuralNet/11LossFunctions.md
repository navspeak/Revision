# Loss Functions in Neural Networks

The **loss function** measures how wrong the network's predictions are. It's the objective that backprop and the optimizer try to minimise.

```
Loss = quantitative answer to "how bad is this prediction?"

Lower loss → better predictions → better model
```

The choice of loss depends on the **task** — regression vs classification — and on the **output activation** of the network.

---

## Loss Function ↔ Output Activation ↔ Task

The three are tied together. Pick them as a **bundle**, not independently:

| Task | Output activation | Loss function |
|------|-------------------|---------------|
| **Regression** | Linear (none) | MSE / MAE / Huber |
| **Binary classification** | Sigmoid | Binary Cross-Entropy |
| **Multiclass classification** (1 label) | Softmax | Categorical Cross-Entropy |
| **Multi-label classification** (many labels) | Sigmoid (per output) | Binary Cross-Entropy per output |

Get the bundle right → everything works. Mix them wrong → silent bugs that hurt accuracy.

---

## Regression Losses

### Mean Squared Error (MSE) — Default for Regression

```
MSE = (1/n) Σ (yᵢ − ŷᵢ)²
```

Squared difference between prediction and truth, averaged.

**Use for:** standard regression tasks (predict a number).

**Pros:**

```
✓ Smooth, differentiable everywhere
✓ Penalises large errors heavily (squared)
✓ Gradient is proportional to error → fast learning
✓ Mathematical convenience (equivalent to assuming Gaussian noise)
```

**Cons:**

```
✗ Very sensitive to outliers (squaring amplifies them)
✗ Single big outlier can dominate the loss
```

**PyTorch:**

```python
criterion = nn.MSELoss()
```

### Mean Absolute Error (MAE) — Robust to Outliers

```
MAE = (1/n) Σ |yᵢ − ŷᵢ|
```

**Use for:** regression with outliers, when you don't want them to dominate.

**Pros:**

```
✓ Robust to outliers (linear penalty)
✓ Direct interpretation: "average error"
```

**Cons:**

```
✗ Not differentiable at 0 (small numerical issues)
✗ Less smooth gradient than MSE
```

**PyTorch:**

```python
criterion = nn.L1Loss()
```

### Huber Loss — Best of Both

```
Huber(z) = 0.5 · z²           if |z| ≤ δ
         = δ · (|z| − 0.5·δ)  if |z| > δ
where z = y − ŷ
```

Behaves like MSE for small errors, like MAE for large ones.

**Use for:** regression when you want MSE's smoothness AND MAE's outlier robustness.

**PyTorch:**

```python
criterion = nn.HuberLoss(delta=1.0)
```

---

## Classification Losses

### Binary Cross-Entropy (BCE) — Binary Classification

For two-class problems (yes/no, 0/1, positive/negative).

```
BCE = −(1/n) Σ [yᵢ · log(p̂ᵢ) + (1 − yᵢ) · log(1 − p̂ᵢ)]

where p̂ᵢ = predicted probability of class 1 (output of SIGMOID)
```

**Output activation:** **Sigmoid** (gives one probability between 0 and 1)

**Output shape:** one number per sample.

**Why it works:**

```
If y = 1 (true label is positive):
   loss = −log(p̂)  →  wants p̂ close to 1

If y = 0 (true label is negative):
   loss = −log(1 − p̂)  →  wants p̂ close to 0

Confidently wrong → HUGE penalty (log of small number)
Confidently right → tiny penalty
```

**PyTorch:**

```python
# Option 1: explicit sigmoid + BCE
criterion = nn.BCELoss()
output = torch.sigmoid(model(x))     # outputs in (0, 1)
loss = criterion(output, y)

# Option 2 (PREFERRED): combine sigmoid + BCE in one call (numerically stable)
criterion = nn.BCEWithLogitsLoss()
output = model(x)                    # raw logits
loss = criterion(output, y)
```

> **Use `BCEWithLogitsLoss`** — applies sigmoid internally with better numerical stability. Don't apply sigmoid separately AND then BCE — that's the "double sigmoid" bug.

---

### Categorical Cross-Entropy — Multiclass Classification

For multi-class problems where each sample has **exactly one** correct class (digit 0–9, language detection, image labels).

```
CE = −(1/n) Σᵢ Σₖ yᵢₖ · log(p̂ᵢₖ)

where:
   k iterates over CLASSES
   yᵢₖ = 1 if sample i's true class is k, else 0  (one-hot)
   p̂ᵢₖ = softmax probability for class k
```

**Output activation:** **Softmax** (probability distribution over all classes, sums to 1)

**Output shape:** K numbers per sample (one per class).

**Why it works:**

```
For each sample, only the correct class's log-probability contributes
(the rest are multiplied by 0 in the one-hot vector).

Loss = −log(probability assigned to the TRUE class)

Confidently wrong → huge penalty
Confidently right → tiny penalty
```

**Worked example — 3 classes:**

```
True class: 1 (one-hot = [0, 1, 0])
Softmax output:    [0.1, 0.7, 0.2]

Loss = −(0·log(0.1) + 1·log(0.7) + 0·log(0.2))
     = −log(0.7)
     = 0.357

If model had been confidently wrong (p̂ = [0.7, 0.1, 0.2]):
Loss = −log(0.1) = 2.30  ← much bigger
```

**PyTorch:**

```python
# CrossEntropyLoss does softmax + NLL internally — pass RAW LOGITS
criterion = nn.CrossEntropyLoss()
logits = model(x)              # raw scores, NO softmax applied
loss = criterion(logits, y)    # y = integer class index (not one-hot!)
```

> **Important PyTorch gotchas:**
> - `CrossEntropyLoss` expects **raw logits**, not softmax outputs (it applies softmax internally)
> - Target `y` should be **integer class indices** (0, 1, 2, ...), not one-hot vectors
> - Don't apply softmax manually before this loss — you'd be applying it twice

---

### Multi-Label Classification

When each sample can have **multiple labels** independently (an image with both "cat" and "dog", a news article tagged "politics" + "economy").

```
Each output is independent → use sigmoid per output → BCE per output
```

**Output activation:** **Sigmoid** (one per label, NOT softmax)

**Loss:** **Binary Cross-Entropy** applied per output, summed/averaged.

**Why NOT softmax:** softmax forces probabilities to sum to 1 — but labels are independent, so multiple can be "true" simultaneously.

**PyTorch:**

```python
criterion = nn.BCEWithLogitsLoss()   # same as binary case
output = model(x)                    # shape (batch, n_labels) — raw logits
loss = criterion(output, y)          # y has 1s where labels are positive
```

---

## Why Not MSE for Classification?

People sometimes try MSE on classification. It "works" but is suboptimal:

```
MSE on classification:
   ✓ It's a valid loss — gradients exist
   ✗ Gradient is small when prediction is far off → slow learning
   ✗ Doesn't reflect probabilistic interpretation
   ✗ Empirically converges slower

Cross-entropy on classification:
   ✓ Gradient is LARGE when prediction is confidently wrong
   ✓ Faster convergence
   ✓ Probabilistic interpretation matches softmax / sigmoid
   ✓ The "right" choice mathematically (maximum likelihood for categorical data)
```

For classification → **always use cross-entropy** (BCE or categorical CE).

---

## Quick Decision Tree

```
What kind of output does my task need?

Continuous number?           → REGRESSION
   Outliers in data?
      Yes → Huber Loss or MAE
      No  → MSE  ✓ DEFAULT

Single class label per sample?  → BINARY or MULTICLASS

   2 classes?              → BINARY CLASSIFICATION
      Output: sigmoid (1 number per sample)
      Loss:   BCEWithLogitsLoss

   3+ classes (exactly one true)? → MULTICLASS
      Output: softmax (K numbers, sum to 1)
      Loss:   CrossEntropyLoss

Multiple independent labels?    → MULTI-LABEL
   Output: sigmoid per label (independent probabilities)
   Loss:   BCEWithLogitsLoss
```

---

## Summary Table

| Task | Output activation | Loss | PyTorch loss class |
|------|-------------------|------|--------------------|
| Regression (default) | Linear (none) | MSE | `nn.MSELoss()` |
| Regression (outliers) | Linear | MAE | `nn.L1Loss()` |
| Regression (smooth + robust) | Linear | Huber | `nn.HuberLoss()` |
| Binary classification | Sigmoid | Binary CE | `nn.BCEWithLogitsLoss()` |
| Multiclass (one label) | Softmax | Categorical CE | `nn.CrossEntropyLoss()` |
| Multi-label (independent) | Sigmoid per output | Binary CE per output | `nn.BCEWithLogitsLoss()` |

---

## Common Pitfalls

```
✗ Applying softmax/sigmoid before CrossEntropyLoss/BCEWithLogitsLoss
   → they apply it internally — you'd be doing it twice
   → fix: pass RAW LOGITS to these losses

✗ Using CrossEntropyLoss with one-hot targets
   → it expects integer class indices
   → fix: y = torch.tensor([0, 2, 1, ...]) not torch.tensor([[1,0,0], [0,0,1], ...])

✗ Using softmax for multi-label classification
   → forces probabilities to sum to 1 (wrong assumption)
   → fix: use sigmoid per label + BCE

✗ Using MSE for classification
   → works but slow
   → fix: use cross-entropy

✗ Forgetting to scale regression targets
   → MSE with targets in millions → huge loss values
   → fix: normalise targets, or use MAE / Huber
```

---

## In Code — End to End

### Binary classification

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(input_dim, 64),
    nn.ReLU(),
    nn.Linear(64, 1)              # raw logit, no sigmoid here
)

criterion = nn.BCEWithLogitsLoss()
# y is a tensor of 0s and 1s, shape (batch,)
loss = criterion(model(x).squeeze(), y.float())
```

### Multiclass classification

```python
model = nn.Sequential(
    nn.Linear(input_dim, 64),
    nn.ReLU(),
    nn.Linear(64, num_classes)    # raw logits, no softmax here
)

criterion = nn.CrossEntropyLoss()
# y is a tensor of class indices, shape (batch,)
loss = criterion(model(x), y)
```

### Regression

```python
model = nn.Sequential(
    nn.Linear(input_dim, 64),
    nn.ReLU(),
    nn.Linear(64, 1)              # linear output, no activation
)

criterion = nn.MSELoss()
loss = criterion(model(x).squeeze(), y)
```

---

## Summary

```
Choose loss based on TASK:

   Regression:
      Default       → MSE
      Robust        → MAE, Huber

   Classification:
      Binary        → BCE (sigmoid output)
      Multiclass    → Categorical CE (softmax output)
      Multi-label   → BCE per output (sigmoid per output)

The loss function and the output activation are PARTNERS.
Pick them together.
```

> Loss function tells the network what "good" means. Get it wrong, and the network optimises for the wrong objective — no matter how well it trains.
