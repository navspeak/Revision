# What Is a Tensor? And What Is Autograd?

Two foundational concepts that underpin every modern deep learning framework (PyTorch, TensorFlow, JAX).

```
Tensor    → the data type that neural networks operate on
Autograd  → automatic differentiation — computes gradients for you
```

---

## What Is a Tensor?

A **tensor** is a multi-dimensional array — a generalisation of scalars, vectors, and matrices.

```
0-D tensor → SCALAR     (just a number)        e.g. 3.14
1-D tensor → VECTOR     (a list of numbers)    e.g. [1, 2, 3]
2-D tensor → MATRIX     (rows × columns)       e.g. [[1,2], [3,4]]
3-D tensor → CUBE       (e.g. an image batch)
4-D tensor → and beyond (e.g. video, batched images)
```

The word **tensor** is just the general name — once you go beyond matrix, there's no shorter term.

---

## Examples by Dimension

```
Scalar      (0-D):  loss value, learning rate
                    torch.tensor(0.5) → shape ()

Vector      (1-D):  one sample's features, one neuron's weights, biases
                    torch.tensor([1.0, 2.0, 3.0]) → shape (3,)

Matrix      (2-D):  batch of features (samples × features), weight matrix
                    torch.tensor([[1,2],[3,4]]) → shape (2, 2)

3-D tensor:        RGB image (height × width × channels)
                    one minibatch of vectors (batch × features × something)
                    shape (32, 28, 28) for 32 grayscale 28×28 images

4-D tensor:        batch of colour images (batch × channels × H × W)
                    shape (32, 3, 224, 224)

5-D and beyond:    video (batch × frames × C × H × W)
                    Transformer attention (batch × heads × seq × seq)
```

---

## Why "Tensor" Instead of "Array"?

In math, a tensor is a generalised array with specific transformation properties. In ML, **tensor = multi-dim array with deep-learning superpowers**:

```
NumPy array         → CPU only, no gradients
PyTorch / TF tensor → can live on GPU, supports autograd
```

Functionally similar for math ops, but tensors are designed for **deep learning workflows**.

---

## In PyTorch

```python
import torch

# Different shapes
a = torch.tensor(3.14)                  # scalar    — shape ()
b = torch.tensor([1.0, 2.0, 3.0])       # vector    — shape (3,)
c = torch.tensor([[1, 2], [3, 4]])      # matrix    — shape (2, 2)
d = torch.zeros(4, 28, 28)              # 3-D       — shape (4, 28, 28)
e = torch.randn(32, 3, 224, 224)        # 4-D batch — shape (32, 3, 224, 224)

print(a.shape)    # torch.Size([])
print(c.shape)    # torch.Size([2, 2])

# On a GPU
gpu_tensor = c.to('cuda')               # move to GPU

# Conversions
np_array = c.numpy()                    # tensor → numpy
back = torch.from_numpy(np_array)       # numpy → tensor
```

---

## Everything in a Neural Network Is a Tensor

```
x   (input)             → tensor (batch × features)
W   (weights)           → tensor (output_dim × input_dim)
b   (bias)              → tensor (output_dim,)
z   (pre-activation)    → tensor
a   (activation)        → tensor
ŷ   (prediction)        → tensor
loss                    → tensor (typically scalar)
gradients               → tensors (same shape as their parameters)
```

Forward and backward passes are just **tensor operations**: matrix multiply, element-wise math, reductions, broadcasting.

That's why GPUs accelerate deep learning — they execute massive parallel tensor operations.

---

## What Is Autograd?

**Autograd = Automatic Differentiation**. It's the system that computes gradients for backpropagation **automatically**, without you writing derivative code.

```
Without autograd:
   You manually derive ∂L/∂W for every weight in the network.
   Doable for tiny models. Impossible for billions of parameters.

With autograd:
   You write the forward pass.
   The framework remembers the computation.
   Call .backward() — gets gradients for FREE.
```

This is the **single most important feature** of modern deep learning frameworks.

---

## How Autograd Works (Conceptually)

```
1. As you do operations on tensors, the framework builds a
   COMPUTATIONAL GRAPH that tracks every step.

2. Each node in the graph stores:
   - the operation performed (multiply, add, etc.)
   - references to its inputs

3. When you call .backward() on a final tensor (typically the loss):
   - The graph is traversed in REVERSE.
   - At each node, the LOCAL gradient is computed.
   - Chain rule is applied automatically.
   - Final gradients accumulate in the leaf tensors' .grad attribute.
```

That's the whole magic of backpropagation, abstracted away.

---

## Simple Example

```python
import torch

# Create a tensor that REQUIRES gradients
x = torch.tensor(3.0, requires_grad=True)

# Forward pass
y = x ** 2 + 2 * x + 1     # y = (x+1)² = 16 when x=3

# Compute gradient: dy/dx
y.backward()

print(x.grad)     # tensor(8.)
                  # because dy/dx = 2x + 2 = 2·3 + 2 = 8
```

You wrote no derivative code. Autograd figured it out.

---

## More Complex Example — Neural Network Training

```python
import torch

# Parameters with gradient tracking
W = torch.randn(3, 4, requires_grad=True)
b = torch.randn(3, requires_grad=True)

# Input and target
x = torch.tensor([0.5, 1.0, 0.2, 0.8])
y = torch.tensor([1.0, 0.0, 0.0])    # one-hot target

# Forward pass
z = W @ x + b
y_hat = torch.softmax(z, dim=0)
loss = -(y * torch.log(y_hat)).sum()  # cross-entropy

# Backward pass — autograd computes ALL gradients
loss.backward()

print(W.grad)    # gradient w.r.t. W — shape (3, 4)
print(b.grad)    # gradient w.r.t. b — shape (3,)
```

You didn't compute a single derivative. Autograd traversed the chain of operations and produced exactly the gradients backpropagation needs.

---

## requires_grad — The Toggle

```
torch.tensor([1.0, 2.0])
   → requires_grad=False (default)
   → not tracked, no gradient

torch.tensor([1.0, 2.0], requires_grad=True)
   → tracked
   → can call .backward() and get .grad

For neural networks:
   model parameters (W, b) → requires_grad=True
   inputs (x)              → requires_grad=False
   labels (y)              → requires_grad=False
```

When you wrap parameters in `nn.Parameter` (which PyTorch does automatically for `nn.Module`), they get `requires_grad=True` by default.

---

## The Computational Graph

Every operation builds a node:

```
W ─┐
   ├── @ ──┐
x ─┘       ├── + ──── z ──── softmax ──── y_hat ──── log ──── × ──── −sum ──── loss
b ──────── ┘                                    ↑
                                                y (no grad)

Forward direction:  → → → → → → → → → → → → → → → → → →
Backward direction: ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
                    (autograd traverses here to compute gradients)
```

When you call `.backward()`, autograd walks this graph in reverse, applying the chain rule at each operation.

---

## Why Autograd Matters

```
✓ You only write the FORWARD pass — the math you care about.
✓ Frameworks compute gradients automatically — no manual chain rule.
✓ Works for ANY computation graph: networks, transformers, even physics simulations.
✓ Scales to billions of parameters effortlessly.
✓ Lets researchers iterate rapidly on new architectures.
```

Without autograd, modern deep learning would be **impossibly tedious**.

---

## Manual vs Autograd — Side by Side

```python
# MANUAL (for y = x²):
x = 3.0
y = x ** 2
# d(x²)/dx = 2x
gradient = 2 * x   # = 6.0

# AUTOGRAD:
import torch
x = torch.tensor(3.0, requires_grad=True)
y = x ** 2
y.backward()
print(x.grad)      # tensor(6.) — autograd computed it
```

For x² that's trivial. For a 70-billion-parameter Transformer, autograd is the only practical option.

---

## In Other Frameworks

```
PyTorch       → torch.autograd
TensorFlow    → tf.GradientTape
JAX            → jax.grad
```

All do the same thing — track operations, compute gradients via the chain rule, give you back gradients to feed to your optimizer.

---

## Common Gotchas

```
✗ Forgetting to call optimizer.zero_grad()
   → gradients ACCUMULATE across batches → wrong updates
   → always zero out before each backward pass

✗ Detaching tensors when you shouldn't
   → tensor.detach() removes from computational graph
   → useful for visualisation, but breaks autograd if used wrong

✗ Modifying tensors in place during forward
   → can break the graph if the original is needed for backward

✗ Treating .grad as a fresh value
   → .grad is accumulated — must zero between iterations
```

---

## The Full Training Loop with Autograd

```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = torch.nn.CrossEntropyLoss()

for batch_x, batch_y in dataloader:
    optimizer.zero_grad()           # clear old gradients
    
    pred = model(batch_x)           # forward — builds graph
    loss = criterion(pred, batch_y) # forward — builds more graph
    
    loss.backward()                 # backward — autograd computes gradients
    
    optimizer.step()                # use gradients to update weights
```

5 lines. That's it. The entire complexity of backpropagation lives inside `loss.backward()` — fully automatic.

---

## Summary

```
TENSOR:
   - multi-dimensional array
   - 0-D = scalar, 1-D = vector, 2-D = matrix, 3+D = tensor
   - the universal data type in deep learning
   - lives on CPU or GPU
   - PyTorch / TensorFlow / JAX

AUTOGRAD:
   - automatic differentiation system
   - tracks operations on tensors → builds a computational graph
   - .backward() computes ALL gradients via chain rule
   - eliminates manual derivative code
   - what makes deep learning feasible at scale
```

> Tensors are the **data**. Autograd is the **engine**. Together they're why you can train a 100-billion-parameter model in a few lines of code.
