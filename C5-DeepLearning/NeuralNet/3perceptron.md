# Perceptron — The Original Neuron

**Perceptron** = the simplest neural network — a **single artificial neuron** that makes binary decisions.

Invented by Frank Rosenblatt in 1958. It's the historical and conceptual ancestor of every neural network today.

---

## What It Does

```
Inputs (x₁, x₂, ...) → Weighted sum + bias → Activation (step function) → Output (0 or 1)
```

A perceptron computes:

```
z = w₁·x₁ + w₂·x₂ + ... + w_n·x_n + b

output = 1 if z ≥ 0
       = 0 if z < 0
```

The activation is a **step function** — abrupt switch from 0 to 1. (Modern neurons use smooth functions like sigmoid or ReLU.)

---

## Visual

```
x₁ ─w₁─┐
x₂ ─w₂─┤
        ├── Σ ──► z ──► step ──► 0 or 1
x₃ ─w₃─┤
...     │
b ──────┘
```

One neuron, one binary output. That's it.

---

## Concrete Example — AND Gate

Goal: output 1 only if BOTH x₁ AND x₂ are 1.

```
Weights:  w₁ = 1,  w₂ = 1
Bias:     b = -1.5

Truth table:
   x₁  x₂  →  z = w₁x₁ + w₂x₂ + b  →  step(z)
   0   0       1·0 + 1·0 + (-1.5) = -1.5     →  0 ✓
   0   1       1·0 + 1·1 + (-1.5) = -0.5     →  0 ✓
   1   0       1·1 + 1·0 + (-1.5) = -0.5     →  0 ✓
   1   1       1·1 + 1·1 + (-1.5) =  0.5     →  1 ✓
```

The perceptron correctly learned the AND function.

---

## How a Perceptron Learns

Rosenblatt's original training algorithm:

```
For each training example (xᵢ, yᵢ):
   1. Compute prediction: ŷ = step(W·xᵢ + b)
   2. Compute error:      e = yᵢ - ŷ
   3. Update weights:     W ← W + η · e · xᵢ
                          b ← b + η · e

Repeat until no errors (or max iterations).
```

If the prediction is correct → no update.
If wrong → adjust weights in the direction that would have made it correct.

---

## What Perceptron Can Do

```
✓ Solves LINEARLY SEPARABLE problems:
   AND, OR, NOT
   Binary classification with a straight-line decision boundary
```

Geometrically, it draws a **line (or hyperplane)** separating two classes:

```
For 2D inputs:
        x₂
         │     ⬤ ⬤
         │   ⬤   ⬤
         │  ─────────  ← decision boundary
         │  ✕    ✕
         │    ✕  ✕
         └──────────── x₁
```

If the data can be separated by a line → perceptron works.

---

## What Perceptron CANNOT Do — The XOR Problem

```
XOR truth table:
   x₁  x₂  →  XOR
   0   0       0
   0   1       1
   1   0       1
   1   1       0

         x₂
         │   ⬤ (0,1)    ✕ (1,1)
         │
         │   ✕ (0,0)    ⬤ (1,0)
         └─────────────── x₁

No single straight line can separate the two classes!
```

This was famously pointed out by Minsky & Papert in 1969 — and it caused the **first AI winter**. The field stalled until people realised:

```
Single perceptron     → can only learn linear boundaries
MULTI-LAYER perceptron (MLP) → can learn ANY function
                              (via hidden layers + non-linearity)
```

---

## Perceptron vs Modern Neuron

| Aspect | Perceptron (1958) | Modern Artificial Neuron |
|--------|------------------|--------------------------|
| Activation | Step function (0 or 1) | Sigmoid, ReLU, tanh (smooth) |
| Output | Binary | Continuous |
| Trainable | Yes (perceptron rule) | Yes (backpropagation) |
| Differentiable | No (step gives zero gradient almost everywhere) | Yes (needed for backprop) |
| Decision boundary | Linear only | Linear (single) → still linear; multiple stacked → non-linear |

The shift from step → smooth activation is what enabled **gradient-based learning** and ultimately deep networks.

---

## Perceptron → Multi-Layer Perceptron (MLP)

```
1 perceptron:      linear binary classifier (limited)

Multi-layer perceptron (MLP):
   Input → Hidden Layer → Output
   Each layer = many perceptron-like neurons in parallel
   Non-linear activation between layers
   
   → can learn ANY continuous function (Universal Approximation)
   → can solve XOR, image classification, anything
```

The MLP is what we've been calling "neural network" throughout this module. The perceptron is its ancestor.

---

## Historical Significance

```
1958  Rosenblatt invents the perceptron
1969  Minsky & Papert publish "Perceptrons" → first AI winter
1986  Rumelhart, Hinton, Williams: backprop for MLPs → revival
1990s Neural nets gain traction (digit recognition, etc.)
2012  AlexNet wins ImageNet → deep learning era begins
2017+ Transformers dominate
```

The perceptron started it all — even though we don't use it directly anymore.

---

## In Code

```python
import numpy as np

class Perceptron:
    def __init__(self, n_inputs, lr=0.1):
        self.W = np.zeros(n_inputs)
        self.b = 0
        self.lr = lr
    
    def predict(self, x):
        z = np.dot(self.W, x) + self.b
        return 1 if z >= 0 else 0
    
    def train(self, X, y, epochs=10):
        for _ in range(epochs):
            for xi, yi in zip(X, y):
                pred = self.predict(xi)
                error = yi - pred
                self.W += self.lr * error * xi
                self.b += self.lr * error

# Learn AND
X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([0, 0, 0, 1])

p = Perceptron(2)
p.train(X, y)

for xi in X:
    print(xi, '→', p.predict(xi))
# [0 0] → 0
# [0 1] → 0
# [1 0] → 0
# [1 1] → 1
```

Try it on XOR — the perceptron will fail to converge.

---

## Why Perceptron Still Matters

```
✓ Foundation of all neural networks
✓ Conceptual starting point for understanding more complex models
✓ Mathematically simple — easy to analyse
✓ Demonstrates the linear-separability limitation
   → motivates why we need hidden layers
   → motivates why we need non-linear activations
✓ Still used as a baseline in classification tasks
```

Modern sklearn even has `Perceptron` as a classifier:

```python
from sklearn.linear_model import Perceptron
model = Perceptron()
model.fit(X_train, y_train)
```

It's essentially logistic regression with a hard threshold — useful for linear problems.

---

## Summary

```
Perceptron =
   - simplest neural network
   - one neuron, weighted sum + step activation
   - learns binary linear classifiers
   - cannot solve XOR (non-linear problem)

Solution to its limitations:
   - Multi-Layer Perceptron (MLP) — stack many perceptrons + non-linear activation
   - Train with backpropagation

Modern neural networks = MLPs with smooth activations + many layers + backprop
```

> The perceptron is to deep learning what the lightbulb is to modern electronics — primitive by today's standards, but the foundation of everything that came after.
