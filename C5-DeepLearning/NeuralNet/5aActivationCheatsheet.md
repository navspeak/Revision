# Activation Functions — Cheatsheet

Focused deep-dive on the four functions you'll meet 95% of the time:

```
ReLU      → default for hidden layers
Sigmoid   → binary output
Tanh      → older hidden-layer choice
Softmax   → multiclass output
```

For each: formula, shape, derivative, where to use, gotchas.

---

## ReLU — Rectified Linear Unit

```
ReLU(z) = max(0, z)
```

**Shape:**

```
ReLU(z)
  │       ╱
  │      ╱
  │     ╱
  │    ╱
  │___╱___________________ z
  0
```

- If z > 0 → output is z (linear)
- If z ≤ 0 → output is 0 (flat)

**Range:** [0, ∞)

**Derivative:**

```
ReLU'(z) = 1   if z > 0
         = 0   if z ≤ 0
```

Cleanest possible gradient — exactly 1 in the active region, 0 in the dead region.

**Pros:**

```
✓ Computationally cheap (just a max)
✓ No vanishing gradient when active (derivative is 1)
✓ Sparse activations (many neurons output 0 → efficient)
✓ Converges faster than sigmoid/tanh in practice
```

**Cons:**

```
✗ DYING RELU — if z is always negative, gradient is 0 → neuron never learns again
✗ Not zero-centred → can cause zigzag updates
✗ Unbounded above → can produce very large values
```

**When to use:** **default for hidden layers** in CNN, MLP, almost everywhere.

**Variants that fix dying ReLU:**

```
Leaky ReLU:   max(0.01·z, z)        → small negative slope
ELU:          z if z>0 else α(eᶻ−1)  → smooth
GELU:         z · Φ(z)                → used in Transformers
```

---

## Sigmoid

```
σ(z) = 1 / (1 + e^(−z))
```

**Shape:**

```
σ(z)
  1.0 |           _________
      |         /
  0.5 |--------/----
      |       /
  0.0 |______/________________  z
            0
```

S-shape ("sigmoid"). Smoothly maps any real number to (0, 1).

**Range:** (0, 1) — interpretable as probability

**Derivative:**

```
σ'(z) = σ(z) · (1 − σ(z))

Max value of derivative = 0.25 (at z = 0)
Approaches 0 as |z| grows
```

**Pros:**

```
✓ Output is a probability (0 to 1)
✓ Smooth and differentiable everywhere
✓ Easy to interpret
```

**Cons:**

```
✗ Vanishing gradient — derivative is ≤ 0.25, often near 0 at extremes
✗ Not zero-centred → can slow convergence
✗ exp() is computationally expensive
✗ Saturates — neurons stop learning once z is very large or very small
```

**When to use:**

```
Binary classification OUTPUT layer  → P(class = 1)
Multi-label outputs (independent labels per output)
Gates in LSTM / GRU
NOT a good choice for hidden layers in deep networks
```

---

## Signum — The Sign Function

```
signum(z) = +1   if z > 0
          =  0   if z = 0
          = −1   if z < 0
```

**Shape:**

```
signum(z)
    +1 |     _____________________
       |    │
       |    │
     0 |════╪════════════════════ z
       |    │
       |    │
    -1 |____│
              z = 0
```

Hard step at 0 — outputs only −1, 0, or +1.

**Range:** {−1, 0, +1} — discrete, only three values

**Derivative:**

```
signum'(z) = 0   almost everywhere
           = undefined at z = 0
```

**This is why signum is unusable for backprop** — zero gradient means no learning signal.

**Pros:**

```
✓ Mathematically clean — pure sign of input
✓ Bipolar (−1 / +1) — symmetric around zero
✓ Useful for binary / quantized neural networks
✓ Foundation of bipolar perceptrons and Hopfield networks
```

**Cons:**

```
✗ Not differentiable → cannot be used with gradient descent
✗ Outputs only 3 distinct values → loses information
✗ Sharp jump → numerical instability
✗ Modern deep learning doesn't use it for trainable layers
```

**When you'll meet it:**

```
Bipolar perceptrons (classical neural net theory)
Hopfield networks (associative memory)
Binary / quantised neural networks (extreme model compression)
Spiking neural networks
Hand-thresholded outputs
NEVER in standard gradient-trained deep networks
```

**Smooth replacement:** **tanh** is the differentiable cousin of signum.

```
At extremes:    tanh(z) → signum(z)
   tanh(−100) ≈ −1
   tanh(+100) ≈ +1

At z = 0:        tanh(0) = 0    (same as signum)

But tanh is smooth and differentiable → autograd works.
```

Use **tanh** when you want signum-like behaviour with trainable gradients.

**In PyTorch:**

```python
torch.sign(z)   # [-1, 0, +1] — signum function, but rarely used as an activation
```

---

## Tanh — Hyperbolic Tangent

```
tanh(z) = (eᶻ − e⁻ᶻ) / (eᶻ + e⁻ᶻ)

Equivalent to:  tanh(z) = 2·σ(2z) − 1
                          (rescaled sigmoid, range (−1, 1))
```

**Shape:**

```
tanh(z)
   1.0 |           _________
       |         /
   0.0 |--------/----
       |       /
  -1.0 |______/________________ z
              0
```

Same S-shape as sigmoid, but centred at 0.

**Range:** (−1, 1) — zero-centred

**Derivative:**

```
tanh'(z) = 1 − tanh²(z)

Max value = 1 (at z = 0)
Approaches 0 as |z| grows
```

**Pros:**

```
✓ Zero-centred — gradients are balanced positive/negative
✓ Steeper gradient than sigmoid (max 1 vs 0.25)
✓ Smooth and differentiable
```

**Cons:**

```
✗ Still suffers from vanishing gradient at extremes
✗ exp() is computationally expensive
```

**When to use:**

```
Hidden layers in older networks (pre-ReLU era)
Hidden state in RNNs / LSTMs (still common)
When you need outputs in (−1, 1) range
```

**Sigmoid vs Tanh comparison:**

```
              Sigmoid     Tanh
Range         (0, 1)      (−1, 1)
Zero-centred  No          Yes
Max gradient  0.25        1.0
Use case      Binary out  Hidden layers
```

Tanh is essentially "better sigmoid" for hidden layers — but both are eclipsed by ReLU in modern practice.

---

## Softmax

```
softmax(zᵢ) = e^(zᵢ) / Σⱼ e^(zⱼ)
```

**Different from the others** — operates on a **vector**, not a single value. Each output depends on all input values.

**Range:** (0, 1) per element, with all elements summing to 1.

**Worked example — 3 classes:**

```
Input logits:  z = [2.0, 1.0, 0.1]

Step 1: exponentiate
   exp(2.0) = 7.389
   exp(1.0) = 2.718
   exp(0.1) = 1.105

Step 2: sum
   sum = 7.389 + 2.718 + 1.105 = 11.212

Step 3: divide
   softmax₁ = 7.389 / 11.212 = 0.659
   softmax₂ = 2.718 / 11.212 = 0.242
   softmax₃ = 1.105 / 11.212 = 0.099

   Total = 1.000  ✓ (probability distribution)
```

The output is now a **probability distribution** over classes — perfect for multiclass classification.

**Properties:**

```
✓ Outputs sum to exactly 1 → valid probability distribution
✓ Larger inputs → exponentially larger outputs (highlights the winner)
✓ Differentiable everywhere
✓ Generalisation of sigmoid to multiple classes
```

**Cons / gotchas:**

```
✗ Numerical instability — exp() of large numbers overflows
   Fix: subtract the max before exponentiating (mathematically equivalent)
        softmax(z) = exp(z − max(z)) / sum(exp(z − max(z)))

✗ Always normalises to 1 — even for nonsense inputs
✗ One class always "wins" by some amount
```

**When to use:**

```
Output layer for MULTICLASS CLASSIFICATION
Attention mechanisms (Transformers)
Probabilistic outputs across categorical choices
```

---

## All Four Side by Side

| Function | Formula | Range | Where used | Key trait |
|----------|---------|-------|------------|-----------|
| **ReLU** | max(0, z) | [0, ∞) | Hidden layers (default) | Fast, but dying ReLU |
| **Sigmoid** | 1/(1+e⁻ᶻ) | (0, 1) | Binary output | Vanishing gradient |
| **Tanh** | (eᶻ−e⁻ᶻ)/(eᶻ+e⁻ᶻ) | (−1, 1) | Hidden (legacy), RNN cells | Zero-centred but still vanishes |
| **Softmax** | eᶻᵢ / Σ eᶻⱼ | (0,1) sum=1 | Multiclass output | Operates on vectors |

---

## Decision Guide

```
Hidden layer in any modern network:
   → ReLU (default)
   → Leaky ReLU / ELU / GELU if dying ReLU
   → Tanh if specifically using RNNs/LSTMs

Output layer:
   Binary classification         → Sigmoid (one output)
   Multi-label classification    → Sigmoid (one per label, independent)
   Multiclass classification     → Softmax (sum to 1)
   Regression                    → None / Linear / Identity
```

---

## Common Mistakes

```
✗ Using sigmoid in hidden layers of deep networks
   → vanishing gradients, slow training
   → use ReLU instead

✗ Using softmax for multi-label (where each label is independent)
   → softmax forces probabilities to sum to 1
   → use sigmoid per output instead

✗ Forgetting the activation at the output layer
   → for classification, you need sigmoid or softmax
   → otherwise raw logits are not interpretable as probabilities

✗ Using sigmoid output but binary cross-entropy with logits
   → either use sigmoid + BCE_loss
     OR raw logits + BCE_with_logits_loss
     NOT sigmoid + BCE_with_logits_loss (applies sigmoid twice)
```

---

## In PyTorch

```python
import torch
import torch.nn.functional as F

z = torch.tensor([2.0, 1.0, 0.1])

F.relu(z)        # [2.0, 1.0, 0.1]   — all positive, unchanged
torch.sigmoid(z) # [0.88, 0.73, 0.52]
torch.tanh(z)    # [0.96, 0.76, 0.10]
F.softmax(z, dim=0)  # [0.66, 0.24, 0.10] sum=1
```

When building layers:

```python
import torch.nn as nn

# Hidden activation
nn.ReLU()
nn.LeakyReLU(0.01)
nn.Tanh()

# Output
nn.Sigmoid()      # binary
nn.Softmax(dim=1) # multiclass
```

**Note:** In practice, you often DON'T explicitly apply softmax — it's combined inside the loss function (`CrossEntropyLoss` in PyTorch expects raw logits).

---

## Quick Memory Hooks

```
ReLU      → "kill negatives, keep positives"
Sigmoid   → "squish anything to (0,1) — a probability"
Tanh      → "sigmoid but centred at 0, range (−1, 1)"
Softmax   → "vector → probability distribution"
```

---

## Summary

```
Hidden layers       → ReLU (default)
Binary output       → Sigmoid
Multiclass output   → Softmax
Older / RNN hidden  → Tanh

All but ReLU and Softmax suffer from vanishing gradients in deep networks.
That's why ReLU revolutionised deep learning — finally trainable deep nets.
```

> Master these four and you can build 95% of neural networks. The rest are variants of the same ideas.
