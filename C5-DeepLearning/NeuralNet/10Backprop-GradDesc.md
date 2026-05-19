# Backprop vs Gradient Descent — They're Different Things

A focused clarification — these two are often confused because they always run together, but they play **different roles**.

```
Backpropagation  = how you COMPUTE the gradients
Gradient descent = how you USE those gradients to update weights
```

Both involve gradients. Both happen in every training step. But conceptually they're **distinct algorithms**.

---

## The Two Steps

```
Step 1 — BACKPROPAGATION
   Given a loss, work out how much each weight contributed.
   Output: ∂L/∂W for every weight in the network.
   
   "Here's the gradient for each weight."

Step 2 — GRADIENT DESCENT (or any optimizer)
   Use those gradients to update the weights.
   W_new = W_old - η · ∂L/∂W
   
   "Take a step in the direction that reduces loss."
```

Backprop **computes** the gradient. Gradient descent **uses** the gradient.

---

## Why They Get Conflated

In every training step they happen **back-to-back**:

```
Training loop:
   forward pass     → predictions
   compute loss     → how wrong
   BACKPROP         → ∂L/∂W for every W       ← computes gradients
   GRADIENT DESCENT → W ← W − η · ∂L/∂W       ← uses gradients
```

People often say "backprop" colloquially to mean both. Strictly, they're separate.

---

## Cooking Analogy

```
BACKPROP                                GRADIENT DESCENT
─────────────────                       ─────────────────────
"If I add 1g more salt,                "OK, salt makes it worse,
 the soup gets 0.3 saltiness            so reduce salt by 0.1g
 units saltier."                        for next batch."

It tells you the EFFECT.                It DECIDES what to change.
Doesn't change the recipe.              Actually changes it.
```

You can't choose recipe adjustments without first knowing each ingredient's effect — which is what backprop tells you.

---

## Same Gradients, Different Optimizers

You can compute gradients via backprop and feed them to **any optimizer**:

```
Gradients from backprop  ──→  Plain gradient descent:
                                  W ← W − η · ∂L/∂W

                          ──→  SGD with momentum:
                                  v = γ·v + η · ∂L/∂W
                                  W ← W − v

                          ──→  Adam:
                                  uses gradient + running averages

                          ──→  Any other optimizer
```

The gradients (from backprop) stay the same. Only the **update rule** changes. That's how we know they're separate concepts.

---

## Side by Side

| | Backpropagation | Gradient Descent |
|-|-----------------|------------------|
| **Role** | Computes gradients | Updates parameters |
| **Output** | ∂L/∂W for each W | New W values |
| **Algorithm** | Chain rule applied through the network | W ← W − η · gradient |
| **Type** | Method for computing derivatives | Optimization algorithm |
| **Variants** | Always works the same way | SGD, Momentum, RMSProp, Adam, ... |
| **Frequency in training** | Once per batch | Once per batch |
| **Replaceable?** | Could use numerical differentiation (slow) | Yes — any optimizer |

---

## Can You Have One Without the Other?

```
Backprop without gradient descent:
   ✓ Useful for understanding sensitivities (explainability)
   ✓ Can use gradients without updating weights
   ✓ Saliency maps, gradient-based feature attribution

Gradient descent without backprop:
   ✗ Only if you compute gradients another way
   ✗ Numerical differentiation (slow, imprecise)
   ✗ Manual derivatives (impossible for large networks)
   ✗ Finite differences (inefficient)

In modern deep learning: ALWAYS backprop + an optimizer.
```

---

## In Code — They're Separate Function Calls

```python
# PyTorch training step

optimizer.zero_grad()        # clear old gradients

predictions = model(x)        # forward pass
loss = criterion(predictions, y)

loss.backward()              # ← BACKPROP: compute ∂L/∂W for all weights
                             #   autograd traverses computational graph
                             #   applies chain rule

optimizer.step()             # ← GRADIENT DESCENT (or other optimizer):
                             #   actually update weights using gradients
                             #   W ← W − η · W.grad
```

Two distinct lines:
- `loss.backward()` → **backpropagation**
- `optimizer.step()` → **gradient descent** (or whatever optimizer)

You could swap `Adam` for `SGD` and only `optimizer.step()` would behave differently. Backprop is unchanged.

---

## Why They Look Similar

Both use **gradients**:

```
Backprop's gradient    →  ∂L/∂W  (computed via chain rule)
Gradient descent's use  →  W ← W − η · ∂L/∂W  (used in update)
```

But they're **doing different jobs** with that same gradient:

```
Backprop:        FIND ∂L/∂W
Gradient descent: USE ∂L/∂W to change W
```

Like a thermometer and a thermostat — both deal with temperature, but one measures, the other acts.

---

## The Full Picture

```
                                    Loss
                                     │
                                     │ loss.backward()
                                     ▼
                              ┌──────────────┐
                              │ BACKPROP     │   ← computes gradients
                              │ (chain rule) │     via autograd
                              └──────┬───────┘
                                     │
                            ∂L/∂W for every W
                                     │
                                     │ optimizer.step()
                                     ▼
                              ┌──────────────┐
                              │ OPTIMIZER    │   ← updates weights
                              │ (SGD, Adam)  │     using gradients
                              └──────┬───────┘
                                     │
                                     ▼
                              Updated weights
                                     │
                                     ▼
                              Next forward pass
```

Every training step: forward → loss → backprop → optimizer step → repeat.

---

## Where to Read More

```
For backprop details                → see 8BackwardProp.md
For optimizer variants              → see 9Optimizers.md
For tensors + autograd context      → see 5WhatIsTensor.md
```

This file is purely about **what's the difference** between the two.

---

## Summary

```
BACKPROPAGATION
   → algorithm that COMPUTES gradients
   → applies chain rule from output back through every layer
   → produces ∂L/∂W for every weight
   → answers: "how much does this weight contribute to the error?"

GRADIENT DESCENT (and its variants)
   → algorithm that UPDATES weights using gradients
   → simplest: W ← W − η · ∂L/∂W
   → variants: SGD, Momentum, Adam, RMSProp, ...
   → answers: "what's the new value for this weight?"

They're partners. Backprop gives the gradient.
Gradient descent (or any optimizer) takes the step.
Always together. Always distinct.
```

> Backprop **computes the slope**. Gradient descent **walks down it**. Same gradient, two different jobs.
