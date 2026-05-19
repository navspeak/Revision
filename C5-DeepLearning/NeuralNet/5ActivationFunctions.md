# Activation Functions

The **non-linearity** in each neuron. Without activation functions, neural networks reduce to **plain linear models** — no matter how many layers.

```
Linear layer alone:                  Linear layer + activation:
   z = Wx + b                            z = Wx + b
                                          a = σ(z)   ← introduces non-linearity
```

Activation functions are what let neural networks model **complex, non-linear** relationships.

---

## Why We Need Activation Functions

| Reason | Explanation |
|--------|-------------|
| **Learning complex patterns** | Without non-linearity, network is just a stack of linear transformations = one big linear transformation |
| **Information flow control** | Activation acts like a gate — decides whether and how strongly a signal passes |
| **Universal approximation** | A network with non-linear activations can approximate **any** continuous function |
| **Biological inspiration** | Mimics the all-or-nothing firing behaviour of real neurons |

---

## The Math Context

Each neuron computes:

```
z = w₁x₁ + w₂x₂ + ... + b      (linear combination)
a = σ(z)                         (apply activation)
```

The `σ` introduces non-linearity. Without it:

```
Layer 1: a⁽¹⁾ = W⁽¹⁾x + b⁽¹⁾
Layer 2: a⁽²⁾ = W⁽²⁾a⁽¹⁾ + b⁽²⁾
        = W⁽²⁾(W⁽¹⁾x + b⁽¹⁾) + b⁽²⁾
        = (W⁽²⁾W⁽¹⁾)x + (W⁽²⁾b⁽¹⁾ + b⁽²⁾)
        = W'x + b'           ← reduces to a single linear function
```

Doesn't matter how many layers — without activations, you're stuck with linear regression.

---

## Common Activation Functions

### Sigmoid

```
σ(z) = 1 / (1 + e^(-z))

Range: (0, 1)
```

```
        σ(z)
         1.0 |     _____
             |   /
         0.5 |--/----
             |/
         0.0 |________________  z
            -∞      0      +∞
```

**Use:** binary classification output (gives probability).
**Remarks:** suffers from **vanishing gradients** — when z is very large or very small, gradient is near 0 → layers stop learning.

---

### Tanh (Hyperbolic Tangent)

```
tanh(z) = (e^z - e^(-z)) / (e^z + e^(-z))

Range: (-1, 1)
```

Zero-centred unlike sigmoid. Better for hidden layers historically.

```
         1.0 |     ____
             |   /
         0.0 |--/----
             | /
        -1.0 |/________________  z
            -∞      0      +∞
```

**Use:** historically used in hidden layers of MLPs.
**Remarks:** still has vanishing gradient problem at extremes.

---

### ReLU (Rectified Linear Unit)

```
ReLU(z) = max(0, z)

Range: [0, ∞)
```

```
        ReLU(z)
            |        /
            |      /
            |    /
            |  /
         ___|/____________________ z
            0
```

**The default activation for hidden layers in modern deep learning.**

**Pros:**
- Computationally cheap (just a max)
- No vanishing gradient for positive inputs
- Sparse activations (many neurons output 0 → efficient)

**Cons:**
- **Dying ReLU** — neurons can get stuck at 0 forever if z is always negative

---

### Leaky ReLU

Fixes the "dying ReLU" issue:

```
Leaky ReLU(z) = max(0.01·z, z)

Allows a small negative slope instead of zero.
```

Range: (−∞, ∞), small negative values for z < 0.

**Pros:** Solves dying ReLU.
**Use:** when you observe many dead neurons with regular ReLU.

---

### ELU (Exponential Linear Unit)

```
ELU(z) = z              if z > 0
       = α(e^z - 1)     if z ≤ 0

α is typically 1.0
```

Smooth alternative to ReLU with negative outputs.

**Pros:** Avoids dying ReLU, smoother gradients.
**Cons:** More compute than ReLU.

---

### Softmax

```
softmax(z_i) = e^(z_i) / Σ e^(z_j)

Range: (0, 1), and all outputs sum to 1
```

**Converts a vector of logits into a probability distribution.**

**Use:** output layer for **multiclass classification**.

```
Input logits:    [2.0, 1.0, 0.1]
exp:             [7.39, 2.72, 1.10]
sum:             11.21
softmax:         [0.66, 0.24, 0.10]   ← probabilities, sum to 1
```

---

## Summary Table

| Function | Formula | Range | Use Case | Issue |
|----------|---------|-------|----------|-------|
| **Sigmoid** | 1/(1+e⁻ᶻ) | (0, 1) | Binary output | Vanishing gradient |
| **Tanh** | (eᶻ−e⁻ᶻ)/(eᶻ+e⁻ᶻ) | (-1, 1) | Hidden (historical) | Vanishing gradient |
| **ReLU** | max(0, z) | [0, ∞) | Hidden (default) | Dying ReLU |
| **Leaky ReLU** | max(0.01z, z) | (-∞, ∞) | Hidden (fixes ReLU) | Mostly OK |
| **ELU** | z or α(eᶻ−1) | (-α, ∞) | Hidden (smooth) | More compute |
| **Softmax** | eᶻ_i / Σ eᶻ_j | (0,1) sum=1 | Multiclass output | Numerical stability |

---

## Activation by Layer Type

| Layer | Common Activation | Reason |
|-------|------------------|--------|
| **Hidden layers** | ReLU, Leaky ReLU, ELU, Tanh | Efficient, propagate gradients well |
| **Binary classification output** | Sigmoid | Outputs probability |
| **Multiclass classification output** | Softmax | Outputs probability distribution |
| **Regression output** | None (linear) | Need unbounded continuous output |

---

## The Vanishing Gradient Problem

```
Sigmoid / tanh have derivatives that are TINY when z is large in magnitude.

During backpropagation, gradients are MULTIPLIED through layers.
If each layer's gradient is ~0.1, then after 10 layers:
   0.1¹⁰ = 10⁻¹⁰

→ early layers receive essentially zero gradient → they don't learn
```

This is why **ReLU is preferred** for hidden layers — its gradient is exactly 1 for positive inputs (no shrinkage).

---

## Non-Linearity in Action

Suppose we want to learn the XOR function:

```
Input  | XOR
[0, 0] |  0
[0, 1] |  1
[1, 0] |  1
[1, 1] |  0
```

**Linear regression cannot solve this** — XOR is not linearly separable.

But a small neural network with **one hidden layer of 2 neurons** and ReLU activation **can** — because the hidden layer's non-linear transformation makes the data linearly separable in the hidden representation.

This is the simplest example of why non-linearity matters.

---

## Universal Approximation Theorem

A network with at least one hidden layer and a non-linear activation function can approximate **any continuous function** on a compact domain — given enough neurons.

```
1 hidden layer + non-linear activation + enough neurons = universal approximator
```

That's the formal guarantee. In practice, **depth** is more efficient than width — a deep network needs fewer total neurons than a wide-shallow one to learn the same function.

---

## Choosing Activations — Modern Recommendations

```
Default for hidden layers:        ReLU
If you see dying ReLU:             Leaky ReLU or ELU
Need smooth gradient:              ELU, GELU (used in Transformers)
Binary output:                      Sigmoid
Multiclass output:                  Softmax
Regression output:                  None (linear / identity)
```

GELU (Gaussian Error Linear Unit) is the standard in modern Transformers — a smoother version of ReLU.

---

## Summary

```
Activation functions = non-linear gates between layers

Without them, the network reduces to linear regression.
With them, networks can approximate any continuous function.

Common functions:
   ReLU      → default for hidden layers
   Sigmoid   → binary output
   Softmax   → multiclass output
   Tanh      → older hidden layer choice
   Leaky/ELU → improvements over ReLU

ReLU is the workhorse of modern deep learning.
```

> Activation functions are what turn a stack of linear matrix multiplications into a powerful function approximator. Without them, there's no "deep" in deep learning.
