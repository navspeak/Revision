# Backpropagation in CNNs

CNNs learn the same way as any other neural network — through **backpropagation**. The only difference: gradients flow through **convolutional layers** instead of fully-connected ones.

```
Forward pass:  Image → conv → pool → ... → prediction
Loss:           how wrong was the prediction?
Backward pass:  gradient flows back through every layer
Update:          weights adjusted to reduce loss
```

The whole training loop is unchanged from MLPs — same `loss.backward()` call, same optimizer. But conceptually, what's happening inside the conv layers is worth understanding.

---

## The Standard Training Loop (Same as MLP)

```python
for epoch in range(num_epochs):
    for batch_x, batch_y in dataloader:
        optimizer.zero_grad()
        pred = cnn_model(batch_x)        # forward pass through conv layers
        loss = criterion(pred, batch_y)
        loss.backward()                   # backprop through conv layers
        optimizer.step()                   # update conv filter weights
```

PyTorch autograd handles the conv-specific gradient math automatically. You write standard code.

---

## What's Different in CNN Backprop

Three things that aren't in MLP backprop:

### 1. Gradients Flow Through Convolutions

A conv layer's forward pass:

```
output = Conv(input, filter_weights)
```

Backprop computes:

```
∂L/∂filter_weights   ← how should filter weights change?
∂L/∂input             ← gradient to pass to previous layer
```

The math is more complex than matrix multiplication, but autograd takes care of it. **You don't write it by hand.**

### 2. Weight Sharing → Gradients Accumulate

The same filter slides across the entire image. During backprop, the gradient for that filter is the **sum** of contributions from **every position** it was applied:

```
Filter applied at positions (1,1), (1,2), (1,3), ...
Each position contributes a partial gradient.

Final gradient for the filter = SUM of all those contributions
```

This is why a tiny filter (e.g., 3×3, only 9 weights) gets a strong gradient signal — it accumulates information from every position in the image.

### 3. Backprop Through Pooling

Pooling layers don't have weights, but gradients still pass through them:

```
Max pooling:
   Forward: takes max of a region
   Backward: gradient flows ONLY to the position that was the max
             other positions get gradient = 0

Average pooling:
   Forward: averages a region
   Backward: gradient distributed EQUALLY across all positions in the region
```

Pooling layers route gradients but don't have parameters to update.

---

## What Each Layer Learns

After many epochs of backprop:

```
Layer 1 filters: end up looking like edge detectors (Gabor-like)
Layer 2 filters: detect textures and simple shapes
Layer 3 filters: detect object parts
Layer 4 filters: detect whole objects
```

The network **discovers** these features through backprop — nobody tells it to learn edges first. The hierarchy emerges naturally because:
- Early layers receive simple gradient signals from many positions
- Late layers receive abstract gradient signals from the loss

---

## Why CNN Backprop Works So Well

```
✓ Weight sharing → each filter gets gradient from many positions
                  → strong learning signal even with few parameters

✓ Local connectivity → gradients respect spatial structure
                       → conv filters learn local patterns

✓ Hierarchical features → gradient signal naturally varies in abstraction
                          → low-level features at low layers, high-level at top

✓ Same machinery as MLPs → autograd handles everything
```

---

## Common Issues

### Vanishing Gradients in Deep CNNs

```
Stack 50 conv layers → gradients shrink through chain rule
   → early layers get tiny gradient → barely learn
   
Fix:
   ✓ ReLU activations (no shrinkage for positive z)
   ✓ Batch normalization
   ✓ Residual connections (ResNet's key idea)
```

### Computational Cost

```
Backprop through conv layers is expensive:
   - Many positions × many filters × many channels
   - GPU acceleration essential

Modern frameworks optimise this heavily.
```

---

## In Code — Behind the Scenes

When you call `loss.backward()` on a CNN:

```python
loss.backward()  # autograd does ALL of this:
                 # 1. Traverse computational graph
                 # 2. Compute gradient at each operation
                 # 3. Accumulate gradients into .grad of each parameter
                 # 4. For conv layers, sum gradients across all positions
                 # 5. For pooling, route gradients to correct positions
```

You don't write any of this manually — but understanding it helps debug training issues.

---

## Summary

```
CNN backprop = same algorithm as MLP backprop
   + gradient flows through CONVOLUTIONS (handled by autograd)
   + weight sharing → gradients accumulate across positions
   + pooling routes gradients without having weights

End result: filters learn task-relevant features automatically.

The conv backbone learns "what to look for" via backprop.
The dense head learns "how to combine those features into a prediction".
Both happen via the same gradient flow.
```

> Backprop in CNNs is conceptually identical to MLP backprop — the difference is in **how** gradients flow through convolutions and pooling. Autograd hides the complexity; the result is automatic feature learning.
