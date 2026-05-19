# Worked Matrix Example — 4 → 3 → 3 → 2 Network

A complete forward pass through a small feedforward network with **real numbers**. Same architecture as the diagram in `3Architecture.md`.

```
Input (4) → Hidden 1 (3) → Hidden 2 (3) → Output (2)
```

ReLU in hidden layers, softmax at output (multiclass classification).

---

## Step 0 — Inputs

```
x = [0.5,  1.0,  0.2,  0.8]      ← 4 input features (vector of length 4)
```

---

## Step 1 — Hidden Layer 1 (4 → 3)

**Weights** `W⁽¹⁾` — shape `(3 × 4)`: 3 neurons, each with 4 weights:

```
          x₁    x₂    x₃    x₄
W⁽¹⁾ = [[ 0.1,  0.2,  0.3,  0.4],   ← weights for neuron 1
        [ 0.5,  0.0,  0.1,  0.2],   ← weights for neuron 2
        [ 0.3,  0.4,  0.2,  0.1]]   ← weights for neuron 3
```

**Biases** `b⁽¹⁾`:

```
b⁽¹⁾ = [0.1,  0.2,  0.0]
```

**Compute z⁽¹⁾ = W⁽¹⁾ · x + b⁽¹⁾:**

```
z₁ = 0.1·0.5 + 0.2·1.0 + 0.3·0.2 + 0.4·0.8 + 0.1
   = 0.05 + 0.20 + 0.06 + 0.32 + 0.10
   = 0.73

z₂ = 0.5·0.5 + 0.0·1.0 + 0.1·0.2 + 0.2·0.8 + 0.2
   = 0.25 + 0.00 + 0.02 + 0.16 + 0.20
   = 0.63

z₃ = 0.3·0.5 + 0.4·1.0 + 0.2·0.2 + 0.1·0.8 + 0.0
   = 0.15 + 0.40 + 0.04 + 0.08 + 0.00
   = 0.67

z⁽¹⁾ = [0.73, 0.63, 0.67]
```

**Apply ReLU** — all positive, so unchanged:

```
a⁽¹⁾ = ReLU(z⁽¹⁾) = [0.73, 0.63, 0.67]
```

---

## Step 2 — Hidden Layer 2 (3 → 3)

**Weights** `W⁽²⁾` — shape `(3 × 3)`:

```
         a₁    a₂    a₃
W⁽²⁾ = [[ 0.2,  0.5,  0.3],
        [ 0.4,  0.1,  0.6],
        [ 0.1,  0.7,  0.2]]
```

**Biases:**

```
b⁽²⁾ = [0.1,  0.0,  0.2]
```

**Compute z⁽²⁾ = W⁽²⁾ · a⁽¹⁾ + b⁽²⁾:**

```
z₁ = 0.2·0.73 + 0.5·0.63 + 0.3·0.67 + 0.1
   = 0.146 + 0.315 + 0.201 + 0.100
   = 0.762

z₂ = 0.4·0.73 + 0.1·0.63 + 0.6·0.67 + 0.0
   = 0.292 + 0.063 + 0.402 + 0.000
   = 0.757

z₃ = 0.1·0.73 + 0.7·0.63 + 0.2·0.67 + 0.2
   = 0.073 + 0.441 + 0.134 + 0.200
   = 0.848

z⁽²⁾ = [0.762, 0.757, 0.848]
```

**Apply ReLU:**

```
a⁽²⁾ = [0.762, 0.757, 0.848]
```

---

## Step 3 — Output Layer (3 → 2)

**Weights** `W⁽³⁾` — shape `(2 × 3)`:

```
         a₁    a₂    a₃
W⁽³⁾ = [[ 0.3,  0.4,  0.5],
        [ 0.6,  0.2,  0.1]]
```

**Biases:**

```
b⁽³⁾ = [0.0,  0.1]
```

**Compute z⁽³⁾ = W⁽³⁾ · a⁽²⁾ + b⁽³⁾:**

```
z₁ = 0.3·0.762 + 0.4·0.757 + 0.5·0.848 + 0.0
   = 0.229 + 0.303 + 0.424 + 0.000
   = 0.955

z₂ = 0.6·0.762 + 0.2·0.757 + 0.1·0.848 + 0.1
   = 0.457 + 0.151 + 0.085 + 0.100
   = 0.793

z⁽³⁾ = [0.955, 0.793]
```

**Apply softmax** (multiclass classification):

```
exp(0.955) = 2.598
exp(0.793) = 2.210
sum        = 4.808

ŷ₁ = 2.598 / 4.808 = 0.540
ŷ₂ = 2.210 / 4.808 = 0.460

ŷ = [0.540, 0.460]
```

**Prediction:** class 0 with 54% probability.

---

## Shape Summary

```
Input    x      shape (4,)            → 4 features
Hidden 1 a⁽¹⁾   shape (3,)            → 3 activations
Hidden 2 a⁽²⁾   shape (3,)            → 3 activations
Output   ŷ      shape (2,)            → 2 class probabilities

Weights:
   W⁽¹⁾  (3, 4)   = 12 weights + 3 biases  = 15 parameters
   W⁽²⁾  (3, 3)   = 9 weights  + 3 biases  = 12 parameters
   W⁽³⁾  (2, 3)   = 6 weights  + 2 biases  = 8 parameters
   Total = 35 parameters
```

Notice the matrix shape rule:

```
W⁽ˡ⁾ shape = (neurons_in_layer_l, neurons_in_layer_l-1)
```

`W⁽¹⁾` is `(3, 4)` — 3 neurons in layer 1, 4 inputs from previous layer.

---

## In NumPy

```python
import numpy as np

x = np.array([0.5, 1.0, 0.2, 0.8])

# Layer 1
W1 = np.array([[0.1, 0.2, 0.3, 0.4],
               [0.5, 0.0, 0.1, 0.2],
               [0.3, 0.4, 0.2, 0.1]])
b1 = np.array([0.1, 0.2, 0.0])

z1 = W1 @ x + b1
a1 = np.maximum(0, z1)        # ReLU
print(a1)  # [0.73 0.63 0.67]

# Layer 2
W2 = np.array([[0.2, 0.5, 0.3],
               [0.4, 0.1, 0.6],
               [0.1, 0.7, 0.2]])
b2 = np.array([0.1, 0.0, 0.2])

z2 = W2 @ a1 + b2
a2 = np.maximum(0, z2)
print(a2)  # [0.762 0.757 0.848]

# Output layer
W3 = np.array([[0.3, 0.4, 0.5],
               [0.6, 0.2, 0.1]])
b3 = np.array([0.0, 0.1])

z3 = W3 @ a2 + b3

# Softmax
exp = np.exp(z3)
y_hat = exp / exp.sum()
print(y_hat)  # [0.540 0.460]
```

Three lines per layer — `W @ a + b` then activation. The whole network is just a chain of these.

---

## Full Flow Visualisation

```
x       [0.5, 1.0, 0.2, 0.8]
   ↓  W⁽¹⁾·x + b⁽¹⁾, ReLU
a⁽¹⁾    [0.73, 0.63, 0.67]
   ↓  W⁽²⁾·a⁽¹⁾ + b⁽²⁾, ReLU
a⁽²⁾    [0.762, 0.757, 0.848]
   ↓  W⁽³⁾·a⁽²⁾ + b⁽³⁾, softmax
ŷ       [0.540, 0.460]   → predict class 0
```

35 parameters total, all the math is just matrix multiplication + activation.

---

## Vectorisation — Multiple Inputs at Once

In practice you don't process one example at a time. You batch them:

```
X shape: (4, n_samples)        ← 4 features × N samples in a batch
Z⁽¹⁾ = W⁽¹⁾ · X + b⁽¹⁾         ← still works! shape (3, n_samples)
A⁽¹⁾ = ReLU(Z⁽¹⁾)               ← same activation, applied element-wise
```

Each column of `X` is one sample. The same `W` and `b` apply to all — that's why GPUs are so good at neural networks. **Matrix multiplication scales beautifully**.

---

## Summary

```
Forward pass = chain of (linear + activation) operations

For each layer:
   z = W · a_prev + b
   a = activation(z)

In this 4 → 3 → 3 → 2 network:
   - 3 weight matrices (W⁽¹⁾, W⁽²⁾, W⁽³⁾)
   - 3 bias vectors (b⁽¹⁾, b⁽²⁾, b⁽³⁾)
   - 35 total parameters
   - Output is a probability distribution via softmax
```

> Once you can do this by hand, the whole neural network forward pass becomes demystified. **It's just matrix multiplication + activations, repeated.**
