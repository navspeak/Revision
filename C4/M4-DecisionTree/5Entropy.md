# Entropy and Information Gain

The **second main impurity measure** for classification splits. Borrowed from information theory.

> **Entropy** = amount of uncertainty in a group.

- All points in same class → no uncertainty → entropy = 0
- Classes evenly split → maximum uncertainty → entropy = 1

---

## Formula

For 2 classes with proportions p and 1−p:

```
Entropy = −p × log₂(p) − (1−p) × log₂(1−p)
```

For C classes:

```
E = −Σᵢ₌₁ᶜ pᵢ × log₂(pᵢ)
```

> Convention: 0 × log(0) = 0.

---

## How It Behaves

| p (Yes) | 1−p | Entropy | |
|---------|-----|---------|---|
| 1.0 | 0.0 | 0.0 | Pure |
| 0.9 | 0.1 | 0.47 | Mostly Yes |
| 0.5 | 0.5 | **1.0** | Maximally mixed |
| 0.1 | 0.9 | 0.47 | Mostly No |
| 0.0 | 1.0 | 0.0 | Pure |

> Pure node → entropy = 0. Maximally mixed binary → entropy = 1.

---

## Information Gain

The **reduction in entropy** from a split:

```
Information Gain = E(parent) − E(children)

where E(children) = weighted average of child entropies
```

The split with the **highest information gain** is chosen.

### "Information Gain" with Gini?

Yes — the term "information gain" strictly refers to entropy-based gain, but the **same idea** applies to Gini:

```
Information Gain (entropy):  E(parent) − E(weighted children)
Gini Gain (Gini):            Gini(parent) − Gini(weighted children)
Variance Reduction (reg.):   Var(parent) − Var(weighted children)
```

All three are the **same concept** — impurity reduction. Only the impurity measure changes.

```
Strict definition:
   "Information gain" = entropy-based (from information theory)

Loose usage:
   "Information gain" is often used generically for any impurity reduction
```

In sklearn you don't pass "information gain" explicitly — you pick the `criterion`:

```python
DecisionTreeClassifier(criterion='gini')      # Gini gain (default)
DecisionTreeClassifier(criterion='entropy')   # Information gain (strict)
```

Either way, sklearn picks the split that maximises the gain — just measured with whichever criterion you chose.

---

## Worked Example

```
Parent: 10 points (7 Yes, 3 No)
   ├── Sub-region 1: 5 points (2 Yes, 3 No)
   └── Sub-region 2: 5 points (5 Yes, 0 No)
```

### Parent entropy

```
E(parent) = −(7/10)·log₂(7/10) − (3/10)·log₂(3/10)
          = −0.7 × (−0.515) − 0.3 × (−1.737)
          = 0.360 + 0.521
          = 0.88
```

### Children entropies

```
E(sub-1) = −(2/5)·log₂(2/5) − (3/5)·log₂(3/5)
         = 0.529 + 0.442
         = 0.97

E(sub-2) = −(5/5)·log₂(5/5) − 0
         = 0 + 0
         = 0          ← pure node
```

### Weighted average

```
E(children) = (5/10) × 0.97 + (5/10) × 0
            = 0.485
```

### Information Gain

```
Gain = 0.88 − 0.485 = 0.395
```

Positive → split improved purity ✓

---

## Gini vs Entropy — Full Comparison

Both measure node impurity, both go to 0 for pure nodes. They almost always pick the same splits.

### Side by side for binary

| p (Yes) | Gini | Entropy |
|---------|------|---------|
| 1.0 | 0.00 | 0.00 |
| 0.9 | 0.18 | 0.47 |
| 0.7 | 0.42 | 0.88 |
| 0.5 | **0.50** | **1.00** |
| 0.3 | 0.42 | 0.88 |
| 0.1 | 0.18 | 0.47 |
| 0.0 | 0.00 | 0.00 |

Both peak at p=0.5, both hit 0 at the pure ends — same shape, different scale.

```
Gini:    0 to 0.5  for binary
Entropy: 0 to 1.0  for binary
```

### Shape

```
Entropy reacts more strongly to imbalance (sharper near peak)
Gini is flatter

       ____peak____
      ╱            ╲
     ╱              ╲       ← Entropy (sharper)
    ╱                ╲
   ╱   __________     ╲
  ╱  ╱            ╲    ╲    ← Gini (flatter)
 ╱  ╱              ╲    ╲
══╧════════════════════╧══
  0        0.5         1
```

### Numerical relationship

```
Entropy ≈ 2 × Gini   (rough approximation for small impurity)
```

That's why they pick the same splits in practice — studies show they agree **>95% of the time** on real data.

### Trade-offs

| | Gini | Entropy |
|-|------|---------|
| Formula | 1 − Σpᵢ² | −Σpᵢ log₂(pᵢ) |
| Binary range | 0 to 0.5 | 0 to 1.0 |
| Compute speed | Faster (no log) | Slightly slower |
| Shape | Flatter | Steeper |
| Used by | CART | ID3, C4.5 |
| sklearn | `criterion='gini'` (default) | `criterion='entropy'` |

### Practical recommendation

```
Default to Gini  → faster, almost always same result
Try Entropy      → only if you suspect Gini is too flat for your problem
```

In 95%+ of cases the choice doesn't matter. Pick Gini and focus on more impactful decisions (max_depth, ccp_alpha, feature engineering).

---

## Summary

```
Entropy: measures uncertainty in a group
Information Gain: how much uncertainty drops after a split
Best split: highest information gain
```

> Gini and Entropy almost always agree on the best split. Pick Gini for speed, Entropy if you prefer the information-theory framing.
