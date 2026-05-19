# Normalization

A technique that makes features (or activations) have **similar ranges and distributions** so the network can train stably and efficiently.

```
Without normalization:
   feature 1: values 100 - 200
   feature 2: values 10,000 - 20,000
   feature 3: values 0 - 1

   → matrix multiplications produce wildly different magnitudes
   → gradients explode or vanish
   → training becomes unstable

With normalization:
   All features have similar scales (e.g., mean 0, variance 1)
   → stable training, faster convergence
```

---

## Why We Need Normalization

Consider an image's feature vector:

```
[colour intensity, width in pixels, height in pixels, aspect ratio, ...]
   ↑                ↑                ↑                ↑
   0 - 255          200 - 4000       100 - 3000       0.5 - 2.0
```

Each feature has a completely different scale. During training:

```
1. Matrix multiplications mix these features
2. Large-range features DOMINATE the dot products
3. Small-range features contribute almost nothing
4. Gradients become unbalanced
5. Some weights barely update; others overshoot
6. Result: EXPLODING / VANISHING GRADIENTS → unstable training
```

Normalization fixes this by bringing all features to the **same scale**.

---

## Min-Max Normalization

```
x_norm = (x − x_min) / (x_max − x_min)
```

Scales all values to the range **[0, 1]**.

### Example

```
Feature values:    [50, 100, 150, 200, 250]
x_min = 50
x_max = 250

Normalized:
   (50 − 50)  / 200 = 0.00
   (100 − 50) / 200 = 0.25
   (150 − 50) / 200 = 0.50
   (200 − 50) / 200 = 0.75
   (250 − 50) / 200 = 1.00
```

Now all values lie in [0, 1].

**Pros:**
- Bounded range
- Easy to interpret

**Cons:**
- Very sensitive to outliers (one extreme value distorts min/max)
- Not suitable if data is unbounded or has outliers

---

## Standardization (Z-Score Normalization)

```
x_std = (x − μ) / σ

μ = mean of the feature
σ = standard deviation
```

Transforms values so the feature has **mean 0 and standard deviation 1**.

### Example

```
Feature values:    [50, 100, 150, 200, 250]
μ = 150
σ ≈ 79

Standardized:
   (50  − 150) / 79 = −1.27
   (100 − 150) / 79 = −0.63
   (150 − 150) / 79 =  0.00
   (200 − 150) / 79 = +0.63
   (250 − 150) / 79 = +1.27
```

Now the feature is **zero-centred** with unit variance.

**Pros:**
- Robust to outliers (compared to Min-Max)
- Standard for deep learning
- Plays well with gradient-based optimization

**Cons:**
- Not bounded to a fixed range

This is the **default** in deep learning. When people say "normalization" without qualification, they usually mean **standardization**.

---

## Min-Max vs Standardization

| | Min-Max | Standardization |
|-|---------|-----------------|
| **Formula** | (x − min) / (max − min) | (x − μ) / σ |
| **Output range** | [0, 1] | unbounded, mean=0, std=1 |
| **Sensitive to outliers?** | Very | Less |
| **Best for** | Bounded features (images, percentages) | Most deep learning tasks |

For deep neural networks → **standardization** by default.

---

## Two Types of Normalization in Networks

Beyond input normalization (just normalising features before training), modern networks also normalise **activations inside the network**:

```
Layer Normalization  → normalise each SAMPLE separately
Batch Normalization  → normalise across the BATCH
```

These help training stability through deep networks.

---

## Layer Normalization

```
For each SAMPLE individually:
   Compute mean and variance ACROSS its features
   Normalize that sample's feature vector
```

### How It Works

```
For sample i:
   compute mean(features of sample i)
   compute variance(features of sample i)
   normalize each feature using these stats
```

**No interaction between samples.** Each sample is normalised on its own.

### Example

```
Batch of 3 samples, each with 4 features:

Sample 1: [10, 12, 8, 14]    → mean = 11, std = 2.24
                                normalised: [-0.45, 0.45, -1.34, 1.34]

Sample 2: [5, 7, 6, 9]       → mean = 6.75, std = 1.48
                                normalised: [-1.18, 0.17, -0.51, 1.52]

Sample 3: [20, 22, 18, 24]   → mean = 21, std = 2.24
                                normalised: [-0.45, 0.45, -1.34, 1.34]
```

Each row normalised against its own stats.

### When to Use

```
✓ RNNs / LSTMs (where batch sizes are variable)
✓ Transformers (the dominant choice)
✓ When batch size is small or 1
✓ When samples are very different from each other
```

**Layer norm is the standard in Transformers (BERT, GPT, etc.).**

---

## Batch Normalization

```
For each FEATURE DIMENSION:
   Compute mean and variance ACROSS THE BATCH
   Normalize that dimension across all samples
```

### How It Works

```
For each feature dimension j:
   collect feature j across all samples in the batch
   compute mean and variance of those values
   normalize feature j of each sample using these stats
```

**Interaction across samples.** All samples in the batch contribute to the stats.

### Example

```
Batch of 3 samples, each with 4 features:

           f1   f2   f3   f4
Sample 1: [10,  12,  8,  14]
Sample 2: [5,   7,   6,  9]
Sample 3: [20,  22,  18, 24]

For f1: values across batch = [10, 5, 20]
   mean = 11.67, std = 6.24
   → normalise sample 1's f1 = (10 - 11.67) / 6.24 = -0.27
   → normalise sample 2's f1 = (5 - 11.67) / 6.24 = -1.07
   → normalise sample 3's f1 = (20 - 11.67) / 6.24 = +1.34

For f2: values across batch = [12, 7, 22]
   ... and so on
```

Each column normalised against the batch's statistics.

### When to Use

```
✓ CNNs (the original use case)
✓ Large batch sizes (typically ≥ 32)
✓ When samples in the batch are similar
✓ Image classification tasks
```

**Batch norm is the standard in CNN architectures (ResNet, VGG, etc.).**

---

## Layer Norm vs Batch Norm — Side by Side

| | Layer Normalization | Batch Normalization |
|-|---------------------|--------------------|
| **Normalises across** | Features within one sample | One feature across the batch |
| **Depends on batch size?** | No | Yes — needs large batches |
| **Works at test time** | Same as training | Uses stored running stats |
| **Common in** | Transformers, RNNs | CNNs |
| **Failure mode** | Less affected by small batches | Bad with batch size = 1 |

### Visual

```
Imagine a batch represented as a table (samples × features):

         f1  f2  f3  f4  f5
sample1  [             ]   ←——— Layer Norm: normalises EACH ROW
sample2  [             ]         (per-sample stats)
sample3  [             ]
sample4  [             ]
           ↑   ↑   ↑   ↑   ↑
           Batch Norm: normalises EACH COLUMN
           (per-feature stats across the batch)
```

Layer norm goes **across rows**. Batch norm goes **down columns**.

---

## Why Normalize Activations (Not Just Inputs)?

Even if you normalise inputs at the start, the activations **inside** deep networks can become unbalanced:

```
Input layer:    normalised (mean=0, std=1)
After layer 1:  activations might have mean=2, std=5
After layer 2:  mean=8, std=20
After layer 3:  mean=30, std=100
...
Late layers:    huge values → unstable gradients
```

This is called **internal covariate shift**. Layer/batch normalization keeps activations well-behaved **throughout** the network.

```
With normalization layers:
   Layer 1: mean=0, std=1
   Layer 2: mean=0, std=1
   Layer 3: mean=0, std=1
   ...
   → stable gradients, fast training
```

---

## In PyTorch

```python
import torch.nn as nn

# Batch Normalization for fully connected layers
model = nn.Sequential(
    nn.Linear(784, 128),
    nn.BatchNorm1d(128),     # normalise across batch dimension
    nn.ReLU(),
    nn.Linear(128, 10)
)

# Layer Normalization
model = nn.Sequential(
    nn.Linear(784, 128),
    nn.LayerNorm(128),        # normalise per-sample
    nn.ReLU(),
    nn.Linear(128, 10)
)

# For CNNs
model = nn.Sequential(
    nn.Conv2d(3, 64, 3),
    nn.BatchNorm2d(64),       # 2D batch norm for image features
    nn.ReLU(),
    ...
)
```

**Rule of thumb:** put batch norm or layer norm **after the linear layer, before the activation**.

---

## Benefits of Internal Normalization

```
✓ Allows higher learning rates → faster training
✓ Reduces sensitivity to weight initialization
✓ Acts as MILD regularization (adds noise via batch statistics)
✓ Reduces vanishing/exploding gradient issues
✓ Often improves final accuracy
✓ Less dependence on careful hyperparameter tuning
```

Batch norm was a major breakthrough — it made training **very deep networks** (50+ layers) practical.

---

## Common Gotchas

```
✗ Batch norm with small batches (1-4)
   → unreliable statistics → training breaks
   → use Layer Norm or Group Norm instead

✗ Forgetting model.eval() during inference with batch norm
   → uses batch statistics instead of stored running averages
   → wrong predictions

✗ Applying batch norm AFTER the activation
   → conventionally goes BEFORE the activation
   → some recent papers experiment with after, but stick with before by default

✗ Using batch norm with dropout
   → can cause interference
   → often choose one or the other, not both in same place
```

---

## When to Use Which Normalization

```
Input data preprocessing       → Standardization (mean=0, std=1)
CNN architectures (vision)     → Batch Normalization
Transformers / RNN / NLP       → Layer Normalization
Small batch / single sample    → Layer Normalization or Group Normalization
Reinforcement learning         → Layer Normalization (varying batch sizes)
```

---

## Summary

```
Normalization = scaling features to similar ranges
   → prevents exploding/vanishing gradients
   → speeds up training
   → improves accuracy

Input normalization:
   Min-Max:           [0, 1] range
   Standardization:   mean=0, std=1   ← default

Internal normalization:
   Batch Norm:    normalise across BATCH (per feature)
                   → CNNs, large batches
   Layer Norm:    normalise within each SAMPLE
                   → Transformers, RNNs, small batches

Both stabilise activations throughout deep networks.
```

> Normalization is one of the most impactful techniques in modern deep learning. It made deep networks **trainable at scale** — without it, models like ResNet, BERT, and GPT wouldn't be possible.
