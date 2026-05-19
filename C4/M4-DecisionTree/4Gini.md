# Gini Index — Splitting for Classification

The Gini index measures the **probability of misclassifying a randomly chosen point** from a group.

```
Gini = 1 − Σ pᵢ²

where pᵢ = proportion of class i in the node
```

---

## Two-Class Case

For a node with proportion `p` of class "Yes" and `1−p` of class "No":

```
Gini = 1 − p² − (1−p)²
```

### How it behaves

| p (Yes) | 1−p (No) | Gini | Interpretation |
|---------|----------|------|---------------|
| 1.0 | 0.0 | 0.0 | Pure — all Yes |
| 0.9 | 0.1 | 0.18 | Mostly Yes |
| 0.5 | 0.5 | **0.50** | Maximally mixed (worst) |
| 0.1 | 0.9 | 0.18 | Mostly No |
| 0.0 | 1.0 | 0.0 | Pure — all No |

> Pure node → Gini = 0. Maximally mixed → Gini = 0.5 (for 2 classes).

---

## Multi-Class Case

For C classes:

```
Gini = 1 − Σᵢ₌₁ᶜ pᵢ²
```

### Example — 3 classes, 10 points

```
Class A: 3 points  → p = 0.3
Class B: 4 points  → p = 0.4
Class C: 3 points  → p = 0.3

Gini = 1 − 0.09 − 0.16 − 0.09 = 0.66
```

The more classes and the more mixed, the higher the Gini.

---

## Evaluating a Split

Compute Gini for parent, then for each subgroup. Take a **weighted average** by number of points in each subgroup.

### Worked Example

```
Parent: 10 points (7 Yes, 3 No)
   ├── Sub-region 1: 5 points (3 Yes, 2 No)
   └── Sub-region 2: 5 points (4 Yes, 1 No)
```

```
Gini(parent) = 1 − (7/10)² − (3/10)² = 1 − 0.49 − 0.09 = 0.42

Gini(sub-1)  = 1 − (3/5)² − (2/5)² = 1 − 0.36 − 0.16 = 0.48
Gini(sub-2)  = 1 − (4/5)² − (1/5)² = 1 − 0.64 − 0.04 = 0.32

Gini(split) = (5/10) × 0.48 + (5/10) × 0.32
            = 0.24 + 0.16
            = 0.40
```

```
0.40 < 0.42 → split improved purity ✓
```

The tree tries **every possible split** and picks the one with the **lowest weighted Gini**.

---

## Worked Example — Multi-Class with Uneven Split

10 points, 3 classes (A, B, C):

```
Parent (10 points):
   Class A: 4 points → p = 0.4
   Class B: 4 points → p = 0.4
   Class C: 2 points → p = 0.2

Gini(parent) = 1 − 0.4² − 0.4² − 0.2²
             = 1 − 0.16 − 0.16 − 0.04
             = 0.64
```

Try a split that divides into **6:4** sub-regions:

```
Sub-region 1 (6 points):       Sub-region 2 (4 points):
   A: 4 (p = 4/6 ≈ 0.67)         A: 0 (p = 0)
   B: 1 (p = 1/6 ≈ 0.17)         B: 3 (p = 3/4 = 0.75)
   C: 1 (p = 1/6 ≈ 0.17)         C: 1 (p = 1/4 = 0.25)
```

### Compute Gini for each sub-region

```
Gini(sub-1) = 1 − (4/6)² − (1/6)² − (1/6)²
            = 1 − 0.444 − 0.028 − 0.028
            = 0.500

Gini(sub-2) = 1 − 0² − (3/4)² − (1/4)²
            = 1 − 0 − 0.5625 − 0.0625
            = 0.375
```

### Weighted Gini for the split

```
Gini(split) = (6/10) × 0.500 + (4/10) × 0.375
            = 0.300 + 0.150
            = 0.450
```

### Compare to parent

```
Gini(parent) = 0.640
Gini(split)  = 0.450

Reduction = 0.640 − 0.450 = 0.190  ← split improved purity ✓
```

Each sub-region is now dominated by one class (A in region 1, B in region 2). The split moved from "mostly mixed" to "mostly clear".

> Note: weights are by **number of points**, not by Gini score. Even though sub-1 has higher Gini than sub-2, it carries more weight because it has more samples.

---

## The Decision Rule

```
For each candidate split:
   compute Gini(split) = weighted average of child Ginis
Pick the split with the lowest Gini(split)
```

This is what `criterion='gini'` does in sklearn — the **default** for `DecisionTreeClassifier`.

---

## Summary

```
Pure node     → Gini = 0
Mixed node    → Gini > 0 (max = 0.5 for binary, → 1 for many classes)
Better split  → lower weighted Gini
```

> Gini is simple, fast to compute, and the default in scikit-learn.
