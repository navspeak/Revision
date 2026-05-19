# BPTT — Backpropagation Through Time

**Backpropagation Through Time** = the algorithm used to train RNNs. It's **standard backpropagation**, just applied to the **unrolled** RNN.

```
BPTT = backprop applied to an RNN by "unrolling" it across time steps,
       treating each time step as a layer in a (very) deep network.
```

The math is the same chain rule we use for MLPs and CNNs. The difference is that gradients flow **backwards through time**, not just through layers.

---

## The Setup — Unrolling an RNN

A recurrent network looks compact when drawn with a loop:

```
        ┌──────┐
   x ──►│ RNN  │──► y
        │ cell │
        │  h   │
        └──┬───┘
           │
           │  (h_t feeds back as h_{t-1})
           └─────────────┐
                         │
                         ▼
                  (next time step)
```

But during training, we **unroll** it — show each time step explicitly:

```
   x_1       x_2       x_3        x_4
    │          │          │          │
    ▼          ▼          ▼          ▼
  ┌─────┐ ──► ┌─────┐ ──► ┌─────┐ ──► ┌─────┐
  │ h_1 │     │ h_2 │     │ h_3 │     │ h_4 │
  └─────┘     └─────┘     └─────┘     └─────┘
    │          │          │          │
    ▼          ▼          ▼          ▼
   y_1       y_2       y_3        y_4
                                   │
                                   ▼
                                  loss
```

Now it looks like a **deep feedforward network** with shared weights at every level.

---

## Forward Pass

```
h_t = activation(W_x · x_t + W_h · h_{t-1} + b_h)
y_t = W_y · h_t + b_y

Same W_x, W_h, W_y at EVERY time step (weight sharing in time).

For a sequence of length 4:
   h_1 = f(W_x · x_1 + W_h · h_0)
   h_2 = f(W_x · x_2 + W_h · h_1)
   h_3 = f(W_x · x_3 + W_h · h_2)
   h_4 = f(W_x · x_4 + W_h · h_3)

   y_4 = W_y · h_4
   loss = compare(y_4, target)
```

Same as forward through any other network — just with the temporal recurrence.

---

## Backward Pass — The "Through Time" Part

Now we apply the **chain rule** to compute gradients. Since the loss depends on `h_4`, which depends on `h_3`, which depends on `h_2`, etc., the gradient has to flow **all the way back through time**.

```
∂loss / ∂W_h = sum over ALL time steps of:
                   (gradient through h_4 path)
                 + (gradient through h_3 path)
                 + (gradient through h_2 path)
                 + (gradient through h_1 path)
```

Because the **same** `W_h` is used at every step, gradients from every step **accumulate**:

```
The chain extends through every step of the sequence:

loss → y_4 → h_4 → h_3 → h_2 → h_1
                                ↑
                          gradient travels here

Same W_h appears 4 times in the chain.
   → its gradient is the SUM of contributions from all 4 steps.
```

---

## Concrete Step-by-Step

Suppose sequence length = 3 and loss is computed only at the last step.

```
Forward:
   h_1 = f(W_x x_1 + W_h h_0)
   h_2 = f(W_x x_2 + W_h h_1)
   h_3 = f(W_x x_3 + W_h h_2)
   y_3 = W_y h_3
   L   = loss(y_3, target)
```

```
Backward — gradient of L w.r.t. W_h:

∂L/∂W_h = ∂L/∂y_3 · ∂y_3/∂h_3 · ∂h_3/∂W_h                                  (direct path through h_3)
       + ∂L/∂y_3 · ∂y_3/∂h_3 · ∂h_3/∂h_2 · ∂h_2/∂W_h                       (through h_2)
       + ∂L/∂y_3 · ∂y_3/∂h_3 · ∂h_3/∂h_2 · ∂h_2/∂h_1 · ∂h_1/∂W_h            (through h_1)
```

Three contributions to `∂L/∂W_h`, one from each time step. **All summed together.**

---

## Why It's Called "Through Time"

```
In a CNN or MLP:
   gradient flows back through LAYERS (spatial depth)

In an RNN:
   gradient flows back through TIME STEPS (temporal depth)

Same chain rule, different axis of flow.
```

So "through time" emphasises that backprop traverses the time dimension of the unrolled network.

---

## The Vanishing / Exploding Gradient Problem

Here's where BPTT gets tricky.

The gradient through many time steps involves repeated multiplication:

```
∂h_t / ∂h_{t-k}  involves multiplying:
   ∂h_t / ∂h_{t-1}  ×  ∂h_{t-1} / ∂h_{t-2}  ×  ...  ×  ∂h_{t-k+1} / ∂h_{t-k}

k multiplications.

If each ≈ 0.5 → gradient ≈ 0.5^k → VANISHES rapidly (k=20 → 10⁻⁶)
If each ≈ 2.0 → gradient ≈ 2^k → EXPLODES rapidly (k=20 → 10⁶)
```

```
Vanishing:  early time steps receive ~zero gradient → can't learn long-range patterns
Exploding:  gradients become huge → weights overflow → NaN losses
```

This is why **vanilla RNNs struggle with sequences longer than ~20 steps**.

### Solutions

```
Exploding gradients:
   ✓ Gradient clipping (cap the gradient magnitude)
   
Vanishing gradients:
   ✓ Better cell types: LSTM, GRU (gates preserve gradient flow)
   ✓ Residual / skip connections
   ✓ Attention mechanisms (Transformers)
```

LSTMs were specifically designed to fix this — their internal "cell state" can carry gradients across many time steps.

---

## Truncated BPTT — A Practical Variant

Computing BPTT for very long sequences is expensive (whole sequence in memory + many backprop steps).

**Truncated BPTT** = backprop only through the last K time steps:

```
Sequence:  [x_1, x_2, ..., x_100]

Full BPTT:  unroll 100 steps, backprop through all 100
Truncated:  process in chunks of 20 → backprop only 20 steps at a time
            forward pass still uses the full hidden state

→ much faster, less memory
→ but can't learn dependencies longer than the truncation window
```

Standard in real-world RNN training. PyTorch's `loss.backward()` plus careful state handling implements this.

---

## BPTT vs Standard Backprop

| | Standard backprop (MLP/CNN) | BPTT (RNN) |
|-|------------------------------|------------|
| Direction | Through layers (depth) | Through time steps |
| Weight sharing | Per-layer separate | Same weight at every time step |
| Gradient accumulation | One contribution per weight | Sum of contributions from every time step |
| Vanishing/exploding | Yes (for very deep networks) | **Much worse** (sequence length can be 100s) |
| Memory cost | Depth × params | Sequence length × hidden size |

The "shape" of the gradient flow is different — through TIME, not just through LAYERS.

---

## Pseudocode for BPTT

```python
# Forward pass — unroll across time
h = h_0
losses = []
for t in range(T):
    h = activation(W_x @ x[t] + W_h @ h + b_h)
    y = W_y @ h
    losses.append(loss_fn(y, target[t]))
total_loss = sum(losses)

# Backward pass — BPTT
total_loss.backward()
# Autograd unrolls the computation graph through time
# Computes ∂L/∂W_x, ∂L/∂W_h, ∂L/∂W_y by summing across time steps

# Update
optimizer.step()
```

In PyTorch, **autograd handles BPTT automatically** when you call `loss.backward()`. You don't write the time-unrolled chain rule yourself.

---

## Why You Should Understand BPTT

```
✓ Explains why vanilla RNNs fail on long sequences (vanishing gradients)
✓ Motivates LSTM / GRU (specifically designed to fix BPTT issues)
✓ Foundation for understanding Transformers (which avoid recurrence entirely)
✓ Common interview topic for ML engineering roles
```

---

## Connection to RNNs

See `26RNNIntro.md` for the broader context — how RNNs work, why they exist, and how they sit alongside MLPs and CNNs.

---

## Summary

```
BPTT = Backpropagation Through Time
     = standard backprop applied to an RNN unrolled across time
     = chain rule traverses TIME instead of just LAYERS

Process:
   1. Forward pass: compute h_1, h_2, ..., h_T
   2. Compute loss at output
   3. Backward pass: gradient flows backward through all time steps
   4. Same weights get gradient from EVERY time step (sum)
   5. Optimiser updates weights

Problems:
   - Vanishing gradients (long sequences)
   - Exploding gradients (gradient clipping fixes)
   - Memory cost grows with sequence length
   - Truncated BPTT trades memory for completeness

Fixes:
   - LSTM / GRU (gates preserve gradient flow)
   - Attention / Transformers (avoid recurrence entirely)
```

> BPTT is the bridge between the **basic backprop you know** and the **temporal nature of RNNs**. Same math, applied across time. Once you see it as "backprop through an unrolled sequence", it becomes natural.
