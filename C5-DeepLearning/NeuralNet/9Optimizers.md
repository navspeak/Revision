# Optimizers

An **optimizer** is an algorithm that updates the network's weights and biases to minimise the loss function.

```
Gradient (from backprop)  →  tells the direction to move
Optimizer                  →  decides HOW MUCH to move and HOW to move
```

The optimizer is what makes the network actually **learn**. The same gradients with different optimizers can give wildly different training outcomes.

---

## Why We Need Optimizers

```
✓ Gradients give DIRECTION only — not step size
✓ Optimizers decide step size (learning rate)
✓ They smooth out noisy gradients
✓ They avoid getting stuck in poor local minima
✓ They speed up convergence
```

Without a good optimizer, training a deep network is painfully slow or doesn't converge at all.

---

## Key Concepts

### 1. Learning Rate (η)

Controls the step size during weight updates:

```
W_new = W_old − η · ∂L/∂W

η too high  →  divergence, loss explodes
η too low   →  very slow training
η just right →  steady convergence
```

The single most important hyperparameter in deep learning.

### 2. Gradient

The slope of the loss function — direction to minimise.

### 3. Momentum

Smooths updates by remembering previous gradients. Like rolling a ball downhill — it builds speed.

### 4. Adaptive Learning Rate

Each parameter gets its own learning rate, adjusted based on gradient history.

---

## Types of Optimizers

### 1. Batch Gradient Descent (BGD)

```
Computes gradient using the ENTIRE dataset
Updates weights ONCE per epoch
```

**Update rule:**

```
W ← W − η · ∇W L
```

**Pros:** stable updates, suitable for convex problems.
**Cons:** very slow for large datasets, needs huge memory.

Rarely used in deep learning because of the compute / memory cost.

---

### 2. Stochastic Gradient Descent (SGD)

```
Updates weights for EACH training example separately
```

**Update rule:**

```
W ← W − η · ∇W L(xᵢ)
```

**Pros:** fast updates, good generalisation, low memory.
**Cons:** very noisy updates, loss fluctuates a lot.

The "stochastic" comes from the randomness of seeing one example at a time.

---

### 3. Mini-Batch Gradient Descent (most common)

```
Uses a small batch of examples (e.g., 32, 64, 128)
Updates weights once per batch
```

**Sweet spot between batch and pure SGD:**

```
✓ Faster than batch GD
✓ Less noisy than pure SGD
✓ Parallelisable on GPUs
✓ Smooth convergence
```

This is what almost all deep learning training uses in practice. When people say "SGD" today, they usually mean **mini-batch SGD**.

---

### 4. Momentum

Adds a fraction of the **previous update** to the current update — like rolling a ball downhill, accumulating velocity.

**Update rule:**

```
v_t = γ · v_{t−1} + η · ∇W L
W ← W − v_t

γ (momentum term) ≈ 0.9
```

**Intuition:**

```
Standard SGD:    each step independent — can zigzag
Momentum:        builds speed in consistent directions, dampens oscillations
```

```
Without momentum:                With momentum:
   ↘
     ↗ ↘                              ↘
       ↗ ↘                              ↘
         ↗   ← oscillating                 ↘   ← smooth, direct
                                            ↘
```

Helps especially with **valleys** in the loss landscape (long narrow ravines).

---

### 5. Nesterov Accelerated Gradient (NAG)

A smarter version of momentum — computes the gradient at the **future position** (where momentum is taking us), not the current position.

```
Standard momentum: gradient at current W → step in direction of momentum + gradient
Nesterov:           jump first with momentum → THEN compute gradient → correct
```

**Advantage:** faster convergence, more stable than vanilla momentum.

Think of it as "looking ahead" before deciding the step.

---

### 6. RMSProp

Uses a **moving average of squared gradients** to adapt the learning rate per parameter.

**Update rule:**

```
E[g²]_t = β · E[g²]_{t−1} + (1 − β) · g_t²
W ← W − (η / √(E[g²]_t + ε)) · g_t

β ≈ 0.9,  ε ≈ 10⁻⁸
```

**Effect:**

```
Parameters with consistently large gradients  → learning rate DECREASES (avoid overshooting)
Parameters with small gradients               → learning rate stays normal (keep learning)
```

**Pros:** works well for non-stationary problems, excellent for RNNs.
**Cons:** no momentum component.

---

### 7. Adam — Adaptive Moment Estimation

The most widely used optimizer in deep learning. **Combines momentum + RMSProp.**

**Update rule (simplified):**

```
m_t = β₁ · m_{t−1} + (1 − β₁) · g_t        ← first moment (momentum)
v_t = β₂ · v_{t−1} + (1 − β₂) · g_t²       ← second moment (RMSProp)
W ← W − η · m_t / (√v_t + ε)
```

**Default parameters (you rarely need to change these):**

```
β₁ = 0.9
β₂ = 0.999
ε  = 10⁻⁸
η  = 0.001 (the default learning rate)
```

**Pros:**

```
✓ Fast convergence
✓ Works well on sparse gradients (NLP, recommendation)
✓ Adapts learning rate per parameter
✓ Robust default for most deep networks
✓ Little hyperparameter tuning needed
```

**Cons:**

```
✗ Slightly worse generalisation than SGD+momentum on some image tasks
✗ Can converge to suboptimal solutions on certain problems
✗ More memory (stores m and v for every parameter)
```

---

## Summary Table

| Optimizer | Step Size | Memory | Best For |
|-----------|-----------|--------|----------|
| **Batch GD** | Same for all parameters | Low | Convex problems, tiny datasets |
| **SGD** | Same for all | Low | Theoretical understanding |
| **Mini-batch SGD** | Same for all | Low | All deep learning baseline |
| **Momentum** | Same, with velocity | Low | Valleys in loss surface |
| **NAG** | Same, look-ahead | Low | When momentum oscillates |
| **RMSProp** | Adaptive per parameter | Medium | RNNs, non-stationary data |
| **Adam** | Adaptive + momentum | High | Default for most problems |

---

## Choosing an Optimizer

```
Default starting point:        Adam (lr=0.001)

Fine-tuning pretrained model:  Adam (lr=2e-5 to 5e-5) — smaller lr
                                AdamW (Adam with weight decay) — for Transformers

Image classification:           SGD + Momentum (often beats Adam on test accuracy)
                                AdamW also works

RNN / LSTM:                     RMSProp or Adam

Reinforcement learning:         Adam usually

Production / very large models: SGD with cosine LR schedule
```

**Rule of thumb:** start with **Adam**. If you need the last few percent of accuracy, try SGD+momentum with careful learning rate scheduling.

---

## Learning Rate Schedules

The learning rate often **decreases over time** for better convergence:

```
Constant:         η stays the same throughout training
Step decay:       η ← η × 0.1 every N epochs
Exponential decay: η = η₀ · e^(−kt)
Cosine schedule:   η follows a cosine curve from initial to 0
Warmup + decay:    η ramps up, then decays (used in Transformers)
```

A good schedule can be the difference between mediocre and state-of-the-art results.

---

## In Code (PyTorch)

```python
import torch.optim as optim

# Simple SGD
optimizer = optim.SGD(model.parameters(), lr=0.01)

# SGD with momentum
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# RMSProp
optimizer = optim.RMSprop(model.parameters(), lr=0.001)

# Adam (most common)
optimizer = optim.Adam(model.parameters(), lr=0.001)

# AdamW — Adam with proper weight decay
optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)
```

Training loop usage:

```python
for batch_x, batch_y in dataloader:
    optimizer.zero_grad()        # clear old gradients
    pred = model(batch_x)        # forward pass
    loss = criterion(pred, batch_y)
    loss.backward()              # backprop
    optimizer.step()             # take an optimization step
```

---

## Visualisation of Optimizer Paths

```
Loss surface (top-down view):

SGD:           ⤳⤳⤳⤳⤳⤳⤳⤳   ← noisy, zigzag
Momentum:      ⤴⤴⤴↘↘↘↘     ← builds velocity
RMSProp:       →→→↓↓↓→      ← adapts per direction
Adam:          ⤴↘→↓→→→      ← combines all benefits — usually shortest path

Target: minimum of the loss
```

Adam typically takes the most direct path to the minimum — that's why it's the default.

---

## Common Issues

```
Loss diverging        → lr too high → decrease lr
Loss not decreasing   → lr too low or vanishing gradient → increase lr or change activations
Loss oscillating      → try momentum or smaller lr
Adam converges to bad minimum → try SGD + momentum + LR schedule
```

---

## Summary

```
Optimizer = algorithm that updates weights using gradients

Hierarchy:
   Batch GD       → uses all data, slow
   SGD            → uses one example, noisy
   Mini-batch SGD → standard practice
   Momentum        → adds velocity
   NAG            → look-ahead momentum
   RMSProp        → adaptive per-parameter learning rate
   Adam           → momentum + RMSProp combined (DEFAULT)

Key hyperparameter: learning rate η
Default choice: Adam (lr=0.001) with mini-batch training
```

> Adam is the workhorse optimizer of modern deep learning. Start with `Adam(lr=1e-3)` for nearly any problem and tune from there.
