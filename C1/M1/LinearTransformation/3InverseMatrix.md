# Inverse, Determinant & Transformations

---

## Determinant — What Does It Represent?

The determinant measures **how much a matrix scales space** — area in 2D, volume in 3D.

Think of the row vectors as sides of a parallelogram:

```
A = [[3, 0],      det(A) = 3×2 - 0×0 = 6
     [0, 2]]
```

The unit square (area=1) becomes a rectangle of area **6** — space stretched by factor 6.

### Key Values
| det value | Meaning |
|-----------|---------|
| = 1       | No scaling — rotation or reflection only |
| > 1       | Space stretched |
| 0 < det < 1 | Space squished |
| < 0       | Space flipped (orientation reversed) + scaled |
| = 0       | Space collapsed to lower dimension → **no inverse** |

### Formula for 2×2
```
A = [[a, b],
     [c, d]]

det(A) = ad - bc
```

---

## Why det = 0 Means No Inverse
A matrix where det = 0 — it collapses space, so no inverse exists.

- The word "singular" means unique/special in a bad way — it breaks the normal rules (can't be inverted).
- Why it happens — always one of these:
  - A row is all zeros
  - One row is a multiple of another (dependent rows)
  - Two rows are identical

### The Collapse Problem
```
A = [[1, 2],
     [2, 4]]

det(A) = 1×4 - 2×2 = 0
```

Multiply any vector [x, y]:
```
A × [x, y] = [x + 2y,
               2x + 4y]
```

Row 2 = 2 × Row 1 always. Every output lands on the line **y = 2x**.

A whole 2D plane got squashed onto a single line — **information is lost**.

### Many inputs → same output
If output is [2, 4], which input produced it?
- [0, 1] → works
- [2, 0] → works
- [1, 0.5] → works

Infinitely many inputs map to the same output. **You can't reverse that.**

### The number analogy
```
5 × 0 = 0
7 × 0 = 0   → can't divide by 0 to get back
```

det = 0 means the matrix behaved like multiplying by zero on space.

---

## When det ≠ 0 — Inverse Exists

```
A = [[2, 0],      det(A) = 6 ≠ 0
     [0, 3]]
```

Every point in the output came from exactly one input — fully reversible.

```
A⁻¹ = [[1/2,   0],
         [0,   1/3]]

A⁻¹ × [2, 3] = [1, 1]  ✅
```

### For a general 2×2:
```
A = [[a, b],
     [c, d]]

A⁻¹ = (1/det(A)) × [[ d, -b],
                      [-c,  a]]
```

### Example
```
A = [[2, 1],
     [3, 7]]

det(A) = 2×7 - 1×3 = 14 - 3 = 11

A⁻¹ = (1/11) × [[ 7, -1],   =  [[ 7/11, -1/11],
                  [-3,  2]]       [-3/11,  2/11]]
```

> Note: For non-diagonal matrices, the transformation mixes x and y together:
> A × [x,y] = [2x+y, 3x+7y] — not a clean axis-by-axis stretch, but det ≠ 0 still guarantees invertibility.

---

## Types of Transformations

### Scaling (Diagonal matrix)
```
[[2, 0],   stretches x by 2, y by 3
 [0, 3]]   det = 6
```

### Shear
Slants space in one direction while keeping the other axis fixed.
```
S = [[1, k],
     [0, 1]]
```

Example k=2: S × [x,y] = [x+2y, y] — y stays fixed, x gets pushed by 2×y

```
Before:          After shear:
(0,1)---(1,1)    (2,1)---(3,1)
  |        |      /        /
(0,0)---(1,0)   (0,0)---(1,0)
```

Like pushing the top of a deck of cards sideways.

- det = 1×1 - k×0 = **1 always**
- Area is always preserved
- Inverse always exists

### Rotation
```
R = [[cos θ, -sin θ],
     [sin θ,  cos θ]]

det(R) = cos²θ + sin²θ = 1
```
- No scaling, no flipping — pure rotation
- det = 1 always

---

## Identifying Transformation Types — Summary

| Matrix form | Type | det |
|-------------|------|-----|
| [[a,0],[0,d]] | Scaling | a×d |
| [[1,k],[0,1]] or [[1,0],[k,1]] | Shear | 1 |
| [[cosθ,-sinθ],[sinθ,cosθ]] | Rotation | 1 |
| det = 0 | Singular / collapse | 0 |

---

## Practice Questions

### P1 — Compute the determinant
```
A = [[4, 3],     B = [[6, 2],     C = [[3, 6],
     [2, 1]]          [3, 1]]          [1, 2]]
```
Which matrices are singular? Which have an inverse?

<details>
<summary>Answer</summary>

```
det(A) = 4×1 - 3×2 = 4 - 6   = -2  → invertible
det(B) = 6×1 - 2×3 = 6 - 6   =  0  → singular, no inverse
det(C) = 3×2 - 6×1 = 6 - 6   =  0  → singular, no inverse
```
</details>

---

### P2 — Find the inverse
```
A = [[3, 1],
     [5, 2]]
```

<details>
<summary>Answer</summary>

```
det(A) = 3×2 - 1×5 = 6 - 5 = 1

A⁻¹ = (1/1) × [[ 2, -1],
                 [-5,  3]]

     = [[ 2, -1],
         [-5,  3]]

Verify: A × A⁻¹ = I ✅
```
</details>

---

### P3 — What type of transformation?
Identify each and state whether area is preserved:
```
A = [[1, 4],    B = [[0, -1],    C = [[5, 0],
     [0, 1]]         [1,  0]]         [0, 2]]
```

<details>
<summary>Answer</summary>

```
A: Shear (k=4) — det = 1, area preserved
B: Rotation by 90° — det = 0×0-(-1×1) = 1, area preserved
C: Scaling (x×5, y×2) — det = 10, area scaled by 10
```
</details>

---

### P4 — Does the inverse exist? If yes, find it.
```
A = [[2, 6],
     [1, 3]]
```

<details>
<summary>Answer</summary>

```
det(A) = 2×3 - 6×1 = 6 - 6 = 0

Singular matrix — no inverse exists.

Geometrically: row 2 = ½ × row 1 — the matrix collapses 2D space onto a line.
```
</details>

---

### P5 — Area scaling
A unit square (area = 1) is transformed by:
```
A = [[3, 1],
     [2, 4]]
```
What is the area of the resulting shape?

<details>
<summary>Answer</summary>

```
det(A) = 3×4 - 1×2 = 12 - 2 = 10

Area of result = |det(A)| × original area = 10 × 1 = 10
```
</details>

### P6 — If det = 1 it can either be shear or rotation. How to tell
<details>
<summary>Answer</summary>


  Rotation — has cos/sin pattern, off-diagonal elements are negatives of each other:
  [[cos θ, -sin θ],
   [sin θ,  cos θ]]
  - Top-left = bottom-right (same value)
  - Top-right = negative of bottom-left
  
  Shear — has 1s on diagonal, zero on one off-diagonal:
  [[1, k],      [[1, 0],
   [0, 1]]       [k, 1]]
  - Diagonal is always 1s
  - Only one off-diagonal is non-zero

  Quick test:
  A = [[0, -1],     diagonal not 1s → check cos/sin
       [1,  0]]     → cos90°=0, sin90°=1 → Rotation ✅

  B = [[1,  3],     diagonal is 1s, one off-diagonal zero → Shear ✅
       [0,  1]]     
   
  Rule of thumb:
  - Diagonal = 1s → Shear
  - Diagonal ≠ 1s but det = 1 → likely Rotationsult = |det(A)| × original area = 10 × 1 = 10

</details>