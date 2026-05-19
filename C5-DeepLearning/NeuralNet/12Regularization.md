# Underfitting, Overfitting, and Regularization

Before learning regularization techniques, you need to understand **what they fight against** — overfitting.

```
Underfitting  → model too simple, can't even fit training data
Overfitting   → model too complex, memorises training data noise
Just right    → model captures real patterns, generalises to new data
```

Regularization is the toolbox we use to **prevent overfitting**.

---

## Underfitting

```
Model has NOT learned a function that captures the data's patterns.
   → Misses important relationships even on the training set.
   → Poor performance during training AND testing.
```

### Visual

```
y
│         ⬤ ⬤ ⬤
│       ⬤  ⬤   ⬤
│   ⬤ ⬤    ⬤     ⬤
│ ─────────────────  ← model fits a STRAIGHT LINE
│                      misses the curve in the data
└──────────────── x
```

The data is curved, but the model fits a straight line. **Too simple**.

### Causes

```
- Model has too few parameters (too few layers / neurons)
- Training stopped too early
- Wrong feature representation
- Too much regularization
```

### Signs

```
Train error: HIGH
Test error:  HIGH

Both are bad → model hasn't learned even the training data.
```

### Fix

```
✓ Make the model larger (more layers, more neurons)
✓ Train longer
✓ Reduce regularization strength
✓ Add more / better features
```

---

## Overfitting

```
Model has learned an EXTREMELY complex pattern.
   → Fits the training data PERFECTLY, including noise.
   → Memorises outliers instead of generalising.
   → Performs great on training, FAILS on testing.
```

### Visual

```
y
│         ⬤    ⬤
│       ⬤   ⬢  ⬤
│   ⬤    ⬢    ⬤
│ ⬢⬢⬢⬢⬢⬢⬢⬢⬢⬢⬢⬢⬢  ← model wiggles through EVERY point
│                      including noisy outliers
└──────────────── x
```

The curve bends in extreme ways to hit every training point — including the noise.

### Causes

```
- Model has too many parameters
- Too few training examples
- Trained too long
- No regularization
- Noisy training data
```

### Signs

```
Train error: VERY LOW (often near zero)
Test error:  HIGH

Huge gap → classic overfitting symptom.
```

### Fix

```
✓ REGULARIZATION (L1, L2, dropout, early stopping)
✓ More training data
✓ Data augmentation
✓ Smaller model
✓ Train less (early stopping)
```

---

## The Right Curve

```
y
│         ⬤
│       ⬤   ⬤
│   ⬤      ⬤
│  ╱─────────╲    ← smooth curve that captures
│ ╱           ╲     the underlying pattern
│                   but NOT the individual noise
└──────────────── x
```

A smooth function that captures the **underlying distribution** without memorising specific samples. This **generalises** to unseen data.

```
Train error: LOW
Test error:  LOW (close to training error)
```

This is what we want.

---

## What Regularization Does

```
Regularization = techniques that prevent overfitting.

Goal: make the model SIMPLER to discourage memorising noise.
        Even at the cost of slightly higher training error.
```

In deep learning, "simpler" usually means:

- **Smaller weight values** (less extreme decision boundaries)
- **Sparser networks** (some weights set to 0)
- **Fewer effective neurons** (some randomly dropped during training)

All these add **constraints** that prevent the model from becoming too flexible.

---

## L1 Regularization (Lasso)

```
Add a penalty to the loss based on the SUM OF ABSOLUTE VALUES of all weights.

L1_loss = original_loss + λ · Σ |wᵢ|
                          ↑       ↑
                       hyperparameter   sum over ALL weights
```

### What L1 Does

```
✓ Pushes SOME weights all the way to 0 (sparsity)
✓ Effectively performs FEATURE SELECTION
   - Useless features get weight = 0 → dropped from the model
✓ Leads to interpretable models
```

### Effect on Weights

```
Without L1:  all weights have some non-zero value
With L1:     many weights become EXACTLY zero
             → only the important features survive
```

### When to Use

```
✓ When you suspect many input features are irrelevant
✓ When you want a sparse, interpretable model
✓ For high-dimensional data with few important features
```

---

## L2 Regularization (Ridge / Weight Decay)

```
Add a penalty based on the SUM OF SQUARED VALUES of all weights.

L2_loss = original_loss + λ · Σ wᵢ²
```

### What L2 Does

```
✓ Pushes ALL weights towards 0 (but not exactly to 0)
✓ Discourages large weight values → smoother decision boundaries
✓ Doesn't perform feature selection — just shrinks magnitudes
```

### Effect on Weights

```
Without L2:  weights can grow very large
With L2:     all weights stay small, balanced
             → smoother, more general predictions
```

### When to Use

```
✓ DEFAULT regularization choice in deep learning
✓ When you want smooth, stable predictions
✓ For most neural network training (often called "weight decay")
```

In modern frameworks, L2 is enabled via `weight_decay` parameter in the optimizer:

```python
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
```

---

## L1 vs L2 — Side by Side

| | L1 (Lasso) | L2 (Ridge / Weight Decay) |
|-|------------|--------------------------|
| **Penalty** | Σ \|wᵢ\| | Σ wᵢ² |
| **Effect on weights** | Some weights → exactly 0 | All weights shrink, stay non-zero |
| **Result** | Sparse model | Dense, smooth model |
| **Feature selection** | Yes | No |
| **Use when** | Many irrelevant features | Default deep learning |
| **Common name** | Lasso | Weight decay |

You can also combine them — **Elastic Net** = L1 + L2.

---

## The λ Hyperparameter

```
loss = original_loss + λ · regularization_term
                       ↑
              controls strength
```

```
λ very LARGE  →  model focuses heavily on minimising weights
                 → ignores the actual prediction task
                 → underfitting

λ very SMALL  →  almost no regularization effect
                 → model can still overfit

λ just right  →  balances fitting the data with simplicity
                 → best generalisation
```

**Tune λ via cross-validation.** Typical values: 1e-5 to 1e-2.

---

## Dropout — A Different Kind of Regularization

```
At each training step, RANDOMLY drop (set to 0) some neurons in a layer.
   → Each iteration uses a different "thinned" network
   → Network can't rely on any single neuron
   → Forces redundancy and robust representations
```

### Visual

```
Full network (normal):              With dropout (50%):

  ⬢ ─── ⬢ ─── ⬢                       ⬢ ─── ✗ ─── ⬢
  │     │     │                         │     │     │
  ⬢ ─── ⬢ ─── ⬢                       ✗ ─── ⬢ ─── ✗
  │     │     │                         │     │     │
  ⬢ ─── ⬢ ─── ⬢                       ⬢ ─── ⬢ ─── ⬢

All neurons active                    Half are randomly dropped
                                      (different ones each iteration)
```

### How It Works

```
1. During training:
   For each neuron, with probability p (e.g. 0.5):
      "drop" it — set its output to 0 for this iteration
   Each batch sees a DIFFERENT random subset of neurons

2. During inference (testing):
   Use ALL neurons — but scale their outputs to compensate
   (or apply "inverted dropout" so scaling happens during training)
```

### Why It Works

```
✓ Prevents over-reliance on any specific neuron
✓ Acts like training many different smaller networks
   → at test time, predictions are an "average" of these → ensemble effect
✓ Forces redundancy — each feature has backups
✓ Reduces co-adaptation of neurons
```

### Typical Values

```
Input layer dropout:    0.0 - 0.2  (low — preserves input info)
Hidden layer dropout:   0.2 - 0.5  (common range)
Just before output:     0.0        (don't drop class predictions)
```

**Used heavily in early deep learning.** Less common in modern Transformers (which use batch norm / layer norm instead, plus L2 weight decay).

**PyTorch:**

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(784, 128),
    nn.ReLU(),
    nn.Dropout(0.5),       # drop 50% of neurons during training
    nn.Linear(128, 10)
)
```

---

## Early Stopping

```
Monitor validation loss during training.
When validation loss STOPS IMPROVING, stop training.
```

### Why It Works

```
At first, both training and validation losses decrease.
At some point, training loss keeps falling but validation loss starts rising.
   → Model is starting to overfit.
   → Stop here to keep the "best" weights.
```

### Visual

```
Loss
  │\
  │ \                          
  │  \___                      Training loss (keeps dropping)
  │      \___                  
  │          \___              
  │              \___          
  │
  │      ______________
  │   /                \___    Validation loss
  │  /                      \___
  │ /                            
  │/                              
  └────────────────────────────── epochs
                ↑
              best epoch
              → stop here (early stopping)
              → past this, you OVERFIT
```

Simple but **extremely effective** — often as good as other regularization techniques.

---

## Data Augmentation

```
Generate more training data by transforming existing samples.

Images:    random crops, rotations, flips, colour jitter
Text:      synonym replacement, back-translation
Audio:     pitch shift, noise addition
```

More data → harder to overfit. Especially powerful for vision tasks.

---

## Other Modern Regularization Techniques

| Technique | What it does |
|-----------|-------------|
| **Batch Normalization** | Normalises activations across the batch → smoother training, mild regularization |
| **Layer Normalization** | Same idea but normalises within each sample (used in Transformers) |
| **Weight initialization** | Good initial weights → smoother convergence |
| **Label smoothing** | Replace one-hot with soft labels (e.g., 0.9/0.1 instead of 1.0/0.0) |
| **Mixup / CutMix** | Blend multiple training samples for richer regularization |
| **Stochastic Depth** | Randomly drop entire layers during training |

---

## Why Layer Inputs Need Normalisation

When activations from one layer vary wildly in scale, gradients explode or vanish. Even with regularization, this can destabilise training.

```
Solution: BATCH NORMALIZATION
   Normalises activations so each layer's inputs are well-behaved.
   Has a mild regularization effect on top of preventing instability.
```

Batch norm and layer norm are covered in their own files — they're the answer to "how do we ensure the data flowing through each layer is balanced and smooth".

---

## When to Use Which Regularization

```
1. Start with L2 (weight_decay=1e-4) — almost always helps
2. Add Dropout (0.2-0.5) if still overfitting
3. Use Early Stopping with a validation set
4. Augment data if you have a small dataset
5. Add Batch Norm for stable training of deep networks
6. Try Label Smoothing for very confident outputs (classification)
```

These can ALL be combined — modern deep networks often use multiple regularization techniques together.

---

## Summary

```
Underfitting:  model too simple → high train + high test error
Overfitting:   model too complex → low train, HIGH test error
Just right:    captures pattern → low train + low test error

Regularization combats overfitting:

   L1 (Lasso)       → push weights to 0 → sparse features
   L2 (Ridge)       → shrink weights → smooth predictions  ← DEFAULT
   Dropout          → randomly drop neurons → robust ensemble
   Early Stopping   → stop training when validation starts rising
   Data Augmentation → more variety → less memorisation
   Batch Norm       → stable activations + mild regularization

The lambda (λ) hyperparameter balances:
   Fitting the data ←→ Keeping the model simple
```

> Regularization is the difference between a model that **memorises** and one that **generalises**. Default to L2 + Dropout + Early Stopping for most deep learning problems.
