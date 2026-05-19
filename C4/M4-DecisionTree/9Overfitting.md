# Overfitting in Decision Trees

A decision tree can keep splitting until **every training point ends up in its own leaf**. The training accuracy is then 100%. But this almost always means the tree has memorised noise — not learned generalisable patterns.

---

## Why Trees Overfit So Easily

### 1. Unlimited splitting

Without restrictions, the algorithm keeps going until every leaf is pure. A leaf may end up containing just one data point — capturing a quirk of that specific sample, not a real pattern.

### 2. Greedy strategy

Even a tiny reduction in impurity is enough to justify another split. These small gains accumulate, leading to very deep trees.

### 3. Piecewise-constant predictions

Each leaf predicts the same value for all points in its region. The only way to capture fine differences is to create more leaves — pushing the tree deeper and deeper.

---

## Symptoms

```
Training accuracy: 100%      ← memorised training set
Test accuracy:     65%       ← can't generalise

Or for regression:
Train R² = 1.00
Test  R² = 0.40
```

A huge gap between train and test performance is the classic sign of overfitting.

---

## Why Bigger Trees Are Worse

```
Depth:        train acc    test acc
   2          75%          74%        ← underfit (too simple)
   5          88%          86%        ← good balance
   10         95%          82%        ← starting to overfit
   unlimited  100%         70%        ← memorising noise
```

The model gets better and better on training data, but **worse** on unseen data once it goes too deep.

This is the **bias-variance trade-off**:

```
Shallow tree:  high bias,  low variance   (underfit)
Deep tree:     low bias,   high variance  (overfit)
Balanced:      moderate of both           (best generalisation)
```

---

## How to Fix It

Two strategies — both about **controlling tree complexity**:

| Strategy | What it does | When |
|----------|--------------|------|
| **Pre-pruning** | Stop the tree growing before it overfits | While training |
| **Post-pruning** | Grow it fully, then cut back | After training |

Both are covered in the next two files.

---

## Quick Intuition

```
With no controls:
   Tree keeps splitting → leaf with 1 point per region → noise captured

With pre-pruning (max_depth=5):
   Tree stops at depth 5 → leaves still have several points → less noise

With post-pruning:
   Tree grows fully → then weakest branches removed → cleaner tree
```

---

## Summary

```
Decision trees overfit easily because:
   - they can split unlimited times
   - they're greedy
   - they make piecewise-constant predictions

Symptom: huge gap between train and test performance
Fix: control complexity via pre-pruning or post-pruning
```

> Trees are flexible — too flexible by default. **Never use an unrestricted decision tree** in practice.
