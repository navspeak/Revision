# Forward Propagation

The process of **computing the network's output** from a given input. Information flows forward, one layer at a time.

```
Input → Layer 1 → Layer 2 → ... → Output
```

Forward propagation is what happens during **inference (prediction)** AND as the first step of every training iteration.

---

## Purpose

```
1. Make a prediction for a new input
2. Compute activations needed to calculate gradients (during training)
3. Compare prediction to ground truth → produces the loss
4. Evaluate model performance on test data
```

It's the **calculate the answer** stage. The backward pass (next file) is the **learn from the error** stage.

---

## How It Works

For each layer:

```
z⁽ˡ⁾ = W⁽ˡ⁾ · a⁽ˡ⁻¹⁾ + b⁽ˡ⁾        ← weighted sum
a⁽ˡ⁾ = σ(z⁽ˡ⁾)                      ← apply activation
```

Where:
- `W⁽ˡ⁾` = weight matrix for layer `l`
- `a⁽ˡ⁻¹⁾` = activation from previous layer (or input `x` if `l = 1`)
- `b⁽ˡ⁾` = bias vector for layer `l`
- `σ` = activation function (ReLU, sigmoid, ...)
- `a⁽ˡ⁾` = activation output of this layer

---

## Computational Flow

```
INPUT x
   │
   ▼
┌──────────────────────────┐
│ Layer 1                  │
│   z⁽¹⁾ = W⁽¹⁾x + b⁽¹⁾   │
│   a⁽¹⁾ = σ(z⁽¹⁾)         │
└──────────────────────────┘
   │
   ▼
┌──────────────────────────┐
│ Layer 2                  │
│   z⁽²⁾ = W⁽²⁾a⁽¹⁾ + b⁽²⁾ │
│   a⁽²⁾ = σ(z⁽²⁾)         │
└──────────────────────────┘
   │
   ▼
   ...
   │
   ▼
┌──────────────────────────┐
│ Output Layer             │
│   z⁽ᴸ⁾ = W⁽ᴸ⁾a⁽ᴸ⁻¹⁾+b⁽ᴸ⁾│
│   ŷ = σ(z⁽ᴸ⁾)            │
└──────────────────────────┘
   │
   ▼
PREDICTION ŷ
```

Every neuron repeats two operations: **weighted sum**, then **activation**.

---

## Worked Example

A 2 → 2 → 1 network (2 inputs, 2 hidden neurons, 1 output) using sigmoid.

```
Input:        x = [0.5, 1.0]
Weights L1:   W⁽¹⁾ = [[0.1, 0.2],
                       [0.3, 0.4]]
Bias L1:      b⁽¹⁾ = [0.1, 0.2]

Weights L2:   W⁽²⁾ = [0.5, 0.6]
Bias L2:      b⁽²⁾ = [0.3]
```

### Layer 1

```
z⁽¹⁾_1 = 0.1·0.5 + 0.2·1.0 + 0.1 = 0.05 + 0.20 + 0.10 = 0.35
z⁽¹⁾_2 = 0.3·0.5 + 0.4·1.0 + 0.2 = 0.15 + 0.40 + 0.20 = 0.75

a⁽¹⁾_1 = σ(0.35) = 0.587
a⁽¹⁾_2 = σ(0.75) = 0.679
```

### Layer 2

```
z⁽²⁾ = 0.5·0.587 + 0.6·0.679 + 0.3
     = 0.294 + 0.408 + 0.300
     = 1.002

ŷ = σ(1.002) ≈ 0.731
```

The network predicts 0.731 → likely "positive" if classifying binary.

---

## Types of Outputs by Task

| Task | Final Activation | Output Interpretation |
|------|------------------|----------------------|
| **Binary classification** | Sigmoid | Probability of class 1 |
| **Multiclass classification** | Softmax | Class probabilities (sum to 1) |
| **Regression** | None (linear) | Continuous numerical value |
| **Multi-label classification** | Sigmoid (per output) | Independent probability per label |

The output activation is **task-specific**. Hidden layers usually use ReLU.

---

## Loss Function

Once forward propagation produces `ŷ`, compare to the true label `y` using a **loss function**.

```
Binary classification:    Binary cross-entropy
Multiclass:                Categorical cross-entropy
Regression:                MSE (mean squared error)
```

Examples:

```
MSE:        L = (1/n) Σ (yᵢ − ŷᵢ)²
Cross-entropy:  L = − Σ yᵢ log(ŷᵢ)
```

The loss is a **single number** measuring how wrong the predictions are.

---

## Why Forward Propagation Matters

| Aspect | Importance |
|--------|-----------|
| **Prediction** | Converts input into output |
| **Learning** | Produces activations needed for gradient computation |
| **Evaluation** | Determines train / test performance |
| **Building block** | Same flow used in CNN, RNN, Transformer |

Forward propagation is **what the network does at inference time**. Backpropagation is only needed during training.

---

## In Code (Conceptually)

```python
def forward(x, weights, biases, activations):
    a = x
    for W, b, sigma in zip(weights, biases, activations):
        z = W @ a + b           # weighted sum
        a = sigma(z)            # activation
    return a                    # final output ŷ
```

Each line is one layer. With NumPy or PyTorch, the same operations happen in parallel on GPUs.

---

## Vectorisation

Forward propagation processes **many examples at once** via matrix operations:

```
Single example:    z = W·x + b       (vector)
Batch of N:        Z = W·X + b       (matrix, X has N columns)
```

GPUs are designed for this — matrix multiplication is their bread and butter. That's why neural networks scale to massive data.

---

## What Each Layer Computes

```
Input  → x = [0.5, 1.0, 0.3, ...]
         ↓ (encode features into a representation)
Hidden 1 → [combinations of input features]
         ↓ (extract higher-level patterns)
Hidden 2 → [combinations of hidden 1 features]
         ↓
Output → predicted probability / value
```

Each layer adds another level of **abstraction**. The output is the final answer; everything in between is the network's internal "thought process".

---

## Summary

```
Forward propagation = compute output by chaining layers

For each layer l:
   z⁽ˡ⁾ = W⁽ˡ⁾ · a⁽ˡ⁻¹⁾ + b⁽ˡ⁾
   a⁽ˡ⁾ = σ(z⁽ˡ⁾)

Final activation depends on task:
   Binary: sigmoid    Multi: softmax    Regression: linear

Loss measures how wrong the predictions are.
Forward pass produces predictions; backward pass uses them to learn.
```

> Forward propagation is just **applying the network**. Same code runs at training time AND inference. The "learning" happens in the backward pass.
