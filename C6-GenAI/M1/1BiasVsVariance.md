# Bias vs Variance — The Core Trade-off

Every supervised model makes errors. We can split that error into **three parts**:

```
Total error = Bias²  +  Variance  +  Irreducible noise
                ↑          ↑              ↑
            too simple  too sensitive   can't fix
```

The first two are under our control. The third (noise in the data itself) is not.

---

## What Each Term Means

### Bias — error from wrong assumptions

The model is **too simple** to capture the real pattern. It "underfits".

```
High bias  → model ignores structure in the data
           → wrong on TRAINING set AND test set
           → e.g. fitting a straight line to a curve
```

### Variance — error from over-sensitivity

The model is **too flexible** and chases noise. It "overfits".

```
High variance → model memorises the training data
              → great on TRAINING set, bad on test set
              → predictions swing wildly if data changes a little
```

---

## The Visual Intuition — Dartboard

```
            Low Variance              High Variance

Low      ┌───────────┐            ┌───────────┐
Bias     │     •      │            │  •     •   │
         │   • • •    │            │     •      │
         │    •••     │   ← ideal  │ •      •  •│
         └───────────┘            └───────────┘
          tight + centred          scattered but centred

High     ┌───────────┐            ┌───────────┐
Bias     │           │            │ •          │
         │           │            │       •    │
         │   •••      │ ← off but  │    •    •  │  ← off AND
         │   •••      │   tight    │ •     •    │     scattered
         └───────────┘            └───────────┘
         consistently wrong        wrong + unstable
```

Bullseye = true value. We want **low bias AND low variance** (top-left).

---

## The Trade-off Curve

As model complexity goes up, bias falls but variance rises.

```
Error
  │ \                              /
  │  \  Variance ────────────→   /
  │   \                         /
  │    \                       /  Total error (U-shape)
  │     \____               __/
  │          \____     ____/
  │   Bias ───────\_______/
  │                  ↑
  │              sweet spot
  └─────────────────────────────────→  Model complexity
   simple                          complex
   (underfit)                      (overfit)
```

The goal is the **bottom of the U** — not the simplest model, not the most complex.

---

## How to Diagnose

| Symptom | Train error | Test error | Problem |
|---------|-------------|------------|---------|
| Underfit | High | High | **High bias** |
| Overfit | Low | High | **High variance** |
| Just right | Low | Low (close to train) | Balanced |
| Hopeless | High | Low | (shouldn't happen — check setup) |

> Rule of thumb: a **big gap** between train and test error → variance problem.
> **Both errors high** → bias problem.

---

## How to Fix Each

### Reduce high bias (underfitting)

```
✓ Use a more complex model (add features, higher-degree, deeper tree)
✓ Add more / better features
✓ Reduce regularisation
✓ Train longer
```

### Reduce high variance (overfitting)

```
✓ Get more training data
✓ Simplify the model
✓ Add regularisation (L1 / L2, dropout)
✓ Feature selection — drop noisy features
✓ Ensemble: bagging / Random Forest (averaging cancels variance)
```

---

## Connection to Other Models

```
Single deep decision tree  → low bias,  HIGH variance
Linear regression          → HIGH bias, low variance
Bagging / Random Forest    → keeps low bias, kills variance by averaging
Boosting                   → keeps low variance, kills bias by correction
SVM (with regularisation C)→ C tunes the bias-variance balance directly
```

> See [[project_probability_revision]] for the broader course context.

---

## Memorable One-Liners

```
Bias     = "stubbornly wrong"      (too simple, ignores data)
Variance = "nervously wrong"       (too sensitive, chases noise)

Underfit → can't even learn the training data
Overfit  → learned the training data TOO well, including its noise
```

---

## Summary

```
Bias    ↑  → underfitting → wrong on train AND test
Variance↑  → overfitting  → great on train, bad on test

You can't minimise both to zero — you balance them.
The aim: lowest TOTAL error (bottom of the U), not lowest bias or lowest variance.

More data and ensembles are the two most reliable variance-killers.
A richer model / more features is the cure for bias.
```

> The whole craft of ML model selection is, at heart, managing this one trade-off.
