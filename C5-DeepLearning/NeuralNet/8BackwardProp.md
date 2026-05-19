# Backward Propagation (Backprop)

The algorithm that **computes gradients of the loss with respect to every weight** in the network — using the chain rule of calculus.

```
Forward pass: compute prediction → compute loss
Backward pass: propagate the error BACK through the layers → compute gradients
```

These gradients tell the optimizer **how to update weights** to reduce the loss.

---

## In Simple Terms

```
1. Make a prediction (forward pass)
2. Compute the error (loss)
3. Figure out how much each weight contributed to the error (backprop)
4. Adjust weights to reduce the error (optimizer step)
```

Without backprop, training a deep network would be infeasible. It's what makes deep learning possible.

---

## Purpose

```
Goal: minimise the loss function L by adjusting weights W and biases b.

To do that, we need ∂L/∂W for every weight in the network.

Backprop computes ALL these gradients efficiently in one backward pass.
```

---

## The Key Idea — Chain Rule

If `L` depends on `a`, which depends on `z`, which depends on `W`:

```
If: L = f(a),  a = g(z),  z = h(W)

Then: ∂L/∂W = (∂L/∂a) · (∂a/∂z) · (∂z/∂W)
              ────────   ────────   ────────
              loss        activation   weight
              gradient    gradient     derivative
```

Each piece is **local** — depends only on one operation. Multiply them along the chain to get the total derivative.

In a neural network, this chain extends through every layer:

```
∂L/∂W⁽ˡ⁾ = ∂L/∂a⁽ᴸ⁾ · ∂a⁽ᴸ⁾/∂z⁽ᴸ⁾ · ∂z⁽ᴸ⁾/∂a⁽ᴸ⁻¹⁾ · ... · ∂z⁽ˡ⁾/∂W⁽ˡ⁾
                 │                                              │
                 └── from output                       all the way to layer l
```

Backprop computes this **layer by layer, starting from the output**.

---

## Three Steps in Backpropagation

### Step 1 — Compute output layer gradient

The error at the output:

```
δ⁽ᴸ⁾ = ∂L/∂z⁽ᴸ⁾ = (ŷ − y) · σ'(z⁽ᴸ⁾)
```

For binary cross-entropy + sigmoid, this simplifies nicely to `(ŷ − y)`.

### Step 2 — Backpropagate to earlier layers

For each layer `l` going BACKWARDS:

```
δ⁽ˡ⁾ = (W⁽ˡ⁺¹⁾)ᵀ · δ⁽ˡ⁺¹⁾ · σ'(z⁽ˡ⁾)
```

The error from layer `l+1` is passed back through the transpose of the weights and multiplied by the derivative of the activation.

### Step 3 — Compute gradients of weights and biases

```
∂L/∂W⁽ˡ⁾ = δ⁽ˡ⁾ · (a⁽ˡ⁻¹⁾)ᵀ
∂L/∂b⁽ˡ⁾ = δ⁽ˡ⁾
```

These are the actual gradients used to update parameters.

---

## Weight Update — Gradient Descent

```
W⁽ˡ⁾ ← W⁽ˡ⁾ − η · ∂L/∂W⁽ˡ⁾
b⁽ˡ⁾ ← b⁽ˡ⁾ − η · ∂L/∂b⁽ˡ⁾

η = learning rate
```

Each weight moves a tiny step in the direction that **reduces the loss**.

---

## Intuitive Analogy

Backprop is like learning to play basketball:

```
1. Take a shot (forward pass)
2. See where it went (loss)
3. Figure out: was the angle off? Was the force too much?  (backprop)
4. Adjust your form (weight update)
5. Try again
```

Each "step" you adjust just slightly — over many tries, you learn to shoot accurately.

---

## Worked Example

A tiny network: 1 input → 1 hidden neuron → 1 output. Sigmoid activations.

```
Given:
   x = 0.5    (input)
   y = 1.0    (true output)
   W⁽¹⁾ = 0.4,  b⁽¹⁾ = 0
   W⁽²⁾ = 0.6,  b⁽²⁾ = 0
```

### Forward Pass

```
z⁽¹⁾ = 0.4 · 0.5 + 0 = 0.20
a⁽¹⁾ = σ(0.20) ≈ 0.550

z⁽²⁾ = 0.6 · 0.550 + 0 = 0.330
ŷ = σ(0.330) ≈ 0.582

Loss = (ŷ − y)² = (0.582 − 1.0)² = 0.175
```

### Backward Pass

**Output layer gradient:**

```
∂L/∂z⁽²⁾ = (ŷ − y) · σ'(z⁽²⁾)
        = (0.582 − 1.0) · σ(0.330)·(1 − σ(0.330))
        = (−0.418) · 0.582 · 0.418
        = −0.102

∂L/∂W⁽²⁾ = ∂L/∂z⁽²⁾ · a⁽¹⁾ = −0.102 · 0.550 = −0.056
∂L/∂b⁽²⁾ = ∂L/∂z⁽²⁾ = −0.102
```

**Hidden layer gradient:**

```
∂L/∂z⁽¹⁾ = (W⁽²⁾)ᵀ · ∂L/∂z⁽²⁾ · σ'(z⁽¹⁾)
        = 0.6 · (−0.102) · σ(0.20)·(1 − σ(0.20))
        = −0.0612 · 0.550 · 0.450
        = −0.0152

∂L/∂W⁽¹⁾ = ∂L/∂z⁽¹⁾ · x = −0.0152 · 0.5 = −0.0076
∂L/∂b⁽¹⁾ = ∂L/∂z⁽¹⁾ = −0.0152
```

**Update (η = 0.1):**

```
W⁽²⁾ = 0.6 − 0.1·(−0.056) = 0.6 + 0.0056 = 0.6056
W⁽¹⁾ = 0.4 − 0.1·(−0.0076) = 0.4 + 0.00076 = 0.40076
```

Both weights increased — pushing `ŷ` up toward the target `y = 1.0`.

Repeat over thousands of iterations → network slowly converges to good weights.

---

## The Complete Training Loop

```
For each batch:
   1. FORWARD PASS    → compute ŷ for input x
   2. COMPUTE LOSS    → L = loss(ŷ, y)
   3. BACKWARD PASS   → compute ∂L/∂W, ∂L/∂b for all layers
   4. UPDATE WEIGHTS  → W ← W − η · ∂L/∂W

Repeat for many epochs (passes over data).
```

This loop is the core of how every neural network learns.

---

## Why Backprop Is Essential

| Function | Importance |
|----------|-----------|
| **Learns from mistakes** | Adjusts weights so next prediction improves |
| **Efficient** | Avoids brute-force trial and error |
| **Scalable** | Works for networks with millions/billions of parameters |
| **Automatic** | Modern frameworks compute gradients automatically (autograd) |
| **General** | Works for ANY differentiable model — networks, transformers, even physics simulators |

---

## Common Issues

### Vanishing Gradients

```
Gradients shrink as they propagate back through many layers.
Early layers receive near-zero gradient → don't learn.

Especially bad with sigmoid/tanh (max derivative ~0.25).
Fix: ReLU (max derivative = 1), batch normalization, residual connections.
```

### Exploding Gradients

```
Gradients grow exponentially through layers.
Weight updates become huge → unstable training, NaN losses.

Fix: gradient clipping (cap the gradient magnitude).
```

### Overfitting

```
Network learns training noise instead of patterns.
Backprop minimises training loss, not test loss.

Fix: dropout, weight decay, data augmentation, early stopping.
```

---

## Modern Frameworks

You rarely implement backprop by hand. PyTorch, TensorFlow, JAX provide **automatic differentiation** (autograd):

```python
import torch

x = torch.tensor([0.5], requires_grad=False)
y = torch.tensor([1.0])
W1 = torch.tensor([0.4], requires_grad=True)
W2 = torch.tensor([0.6], requires_grad=True)

# Forward
a1 = torch.sigmoid(W1 * x)
y_hat = torch.sigmoid(W2 * a1)
loss = (y_hat - y) ** 2

# Backward — autograd computes ALL gradients
loss.backward()

print(W1.grad)   # automatically computed
print(W2.grad)
```

This is one of the most powerful features of modern deep learning frameworks.

---

## Summary

```
Backpropagation = compute gradient of loss w.r.t. every weight
                = via the chain rule of calculus
                = layer by layer, working BACKWARDS

Steps:
   1. Output layer gradient
   2. Propagate back to each earlier layer
   3. Use gradients to update weights (gradient descent)

Issues: vanishing/exploding gradients, overfitting
Fixes: ReLU, batch norm, residual connections, dropout

Forward pass: how the network computes
Backward pass: how the network LEARNS
```

> Backpropagation is the **fundamental learning algorithm** of neural networks. Every deep model you've heard of — GPT, BERT, ResNet, Stable Diffusion — trains via backprop.
