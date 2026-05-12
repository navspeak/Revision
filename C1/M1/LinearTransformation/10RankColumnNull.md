# Rank, Column Space and Null Space

## Non-Invertible Matrices (Recap)

A matrix is non-invertible (singular) when det(A) = 0.

**Geometric reason:** The transformation "squishes" space into a lower dimension.
- 2D → line (rank 1)
- 2D → point (rank 0)
- 3D → plane or line

Solving **Ax = b** means: find the vector x that lands on b after transformation A.
If A squishes space, many vectors land on the same point → can't reverse → no unique solution.

---

## Rank

**Rank = dimensionality of the output of the transformation.**

```
A = [[1, 2],
     [2, 4]]
```

Column 2 = 2 × Column 1 — they are **collinear** (same direction).
The transformation squishes 2D → a straight line.

```
rank(A) = 1   (output is 1D — a line)
```

| rank | Meaning |
|------|---------|
| = n  | Full rank — transformation preserves dimensions |
| < n  | Rank deficient — space is squished |
| = 0  | Zero matrix — everything maps to origin |

**Rule:** rank = number of linearly independent columns = number of non-zero rows after row reduction.

```python
import numpy as np
A = np.array([[1, 2], [2, 4]])
print(np.linalg.matrix_rank(A))   # 1
```

---

## Column Space

**Column space = the span of the columns of the matrix.**

It is the set of all vectors you can reach by applying the transformation — all possible outputs.

```
A = [[1, 2],
     [2, 4]]

Column 1: [1, 2]
Column 2: [2, 4] = 2 × [1, 2]   ← same direction, not independent
```

Column space = all multiples of [1, 2] → **a straight line through the origin**.

```
A = [[1, 0],
     [0, 1]]   ← identity

Column space = all of R²   (full rank)
```

> **What is R²?**
> R = real numbers (all numbers -∞ to +∞)
> R² = 2D real coordinate space — every possible (x, y) pair on the plane
> The 2 means 2 dimensions, not squaring.
> R¹ = line, R² = plane, R³ = 3D space, Rⁿ = n-dimensional space

**Key link:**
```
rank(A) = dimension of column space
```

---

## Null Space

**Null space = all vectors that map to the zero vector under transformation A.**

```
A @ v = 0
```

For a full rank matrix, only v = [0,0] satisfies this → null space = {0}

For a singular matrix:

```
A = [[1, 2],
     [2, 4]]

A @ [2, -1] = [1×2 + 2×(-1),  2×2 + 4×(-1)] = [0, 0]  ✅
A @ [4, -2] = [0, 0]  ✅
A @ [6, -3] = [0, 0]  ✅
```

All vectors of the form [2k, -k] map to zero → null space is the **line v₂ = -½v₁**

**Key relationship — Rank-Nullity Theorem:**
```
rank + nullity = n   (number of columns)

nullity = dimension of null space
```

Think of it as a budget — total dimensions = what survives + what collapses:
```
n columns = rank + nullity
total     = what survives + what collapses to zero
```

| Matrix | rank | nullity | n | check |
|--------|------|---------|---|-------|
| Full rank [[1,0],[0,1]] | 2 | 0 | 2 | 2=2+0 ✅ |
| Singular [[1,2],[2,4]] | 1 | 1 | 2 | 2=1+1 ✅ |
| Zero [[0,0],[0,0]]     | 0 | 2 | 2 | 2=0+2 ✅ |

For A (2×2, rank=1): nullity = 2 - 1 = 1 → null space is a line ✅

---

## All Three Together

```
A = [[1, 2],
     [2, 4]]
```

```
┌─────────────┬───────────────────────────────────┐
│ Rank        │ 1  (one independent column)        │
│ Column space│ line spanned by [1,2]              │
│ Null space  │ line spanned by [2,-1]             │
│ det(A)      │ 0  → singular, no inverse          │
└─────────────┴───────────────────────────────────┘
```

```python
import numpy as np

A = np.array([[1, 2], [2, 4]])

print("Rank:", np.linalg.matrix_rank(A))          # 1

# Null space via SVD
U, S, Vt = np.linalg.svd(A)
null_space = Vt[S < 1e-10]
print("Null space vector:", null_space)            # ~ [0.447, -0.894] ∝ [2,-1]
```

---

## Summary

| Concept | Definition | For [[1,2],[2,4]] |
|---------|-----------|-------------------|
| Rank | Dimension of output | 1 |
| Column space | All reachable outputs (span of columns) | Line y=2x |
| Null space | All inputs that map to zero | Line v₂=-½v₁ |
| Singular | det=0, rank < n | Yes |
