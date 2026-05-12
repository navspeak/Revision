# Eigenvectors and Eigenvalues

## The Core Idea

When you apply a matrix transformation to most vectors, the direction changes.

But for special vectors — called **eigenvectors** — the direction stays the same. The vector only gets **scaled**.

```
A @ v = λv

A  = transformation matrix
v  = eigenvector  (direction unchanged)
λ  = eigenvalue   (how much it scaled)
```

---

## Visual Intuition

```
Normal vector:                 Eigenvector:
                                
  A @ u  ↗ (direction changed)    A @ v  ↑  (same direction)
       /                                  |
      /                                   |  scaled by λ
     → u                                  → v
```

Think of it as: most vectors get rotated + scaled. Eigenvectors only get scaled.

---

## Simple Example

```
A = [[2, 0],
     [0, 3]]
```

Try v = [1, 0]:
```
A @ [1, 0] = [2, 0] = 2 × [1, 0]   ✅  eigenvalue λ = 2
```

Try v = [0, 1]:
```
A @ [0, 1] = [0, 3] = 3 × [0, 1]   ✅  eigenvalue λ = 3
```

For a diagonal matrix — the basis vectors **are** the eigenvectors, and diagonal values **are** the eigenvalues.

---

## Finding Eigenvalues

Start from: **A @ v = λv**

Rearrange:
```
A @ v - λv = 0
(A - λI) @ v = 0
```

For a non-zero v to exist, the matrix (A - λI) must be **singular**:
```
det(A - λI) = 0
```

This is called the **characteristic equation**.

### Example
```
A = [[4, 1],
     [2, 3]]

A - λI = [[4-λ,  1  ],
           [2,   3-λ]]

det(A - λI) = (4-λ)(3-λ) - 1×2
            = 12 - 4λ - 3λ + λ² - 2
            = λ² - 7λ + 10
            = (λ - 5)(λ - 2)

λ₁ = 5,  λ₂ = 2
```

---

## Finding Eigenvectors

Once you have λ, substitute back into **(A - λI) @ v = 0** and solve.

### For λ₁ = 5:
```
A - 5I = [[4-5,  1  ],   =  [[-1,  1],
           [2,   3-5]]        [ 2, -2]]

[[-1, 1],  @  [v₁,  =  [0,
 [ 2,-2]]      v₂]      0]

-v₁ + v₂ = 0  →  v₂ = v₁

Eigenvector: v = [1, 1]  (any scalar multiple works)
```

### For λ₂ = 2:
```
A - 2I = [[2,  1],
           [2,  1]]

2v₁ + v₂ = 0  →  v₂ = -2v₁

Eigenvector: v = [1, -2]
```

---

## Verify
```
A @ [1, 1] = [[4,1],[2,3]] @ [1,1] = [5, 5] = 5 × [1,1]  ✅  λ=5
A @ [1,-2] = [[4,1],[2,3]] @ [1,-2] = [2,-4] = 2 × [1,-2] ✅  λ=2
```

---

## Shortcut — Triangular Matrices

For **upper or lower triangular matrices**, eigenvalues = diagonal elements directly. No calculation needed.

```
A = [[3, -8,  4],
     [0, -5, -1],    → λ₁=3, λ₂=-5, λ₃=6
     [0,  0,  6]]
```

**Why?** Characteristic equation factors cleanly:
```
det(A - λI) = (3-λ)(-5-λ)(6-λ) = 0
```

Off-diagonal elements vanish in the determinant expansion.

Applies to:
- Upper triangular (zeros below diagonal)
- Lower triangular (zeros above diagonal)
- Diagonal matrices

---

## Key Properties

| Property | Meaning |
|----------|---------|
| λ = 0 | Matrix is singular — eigenvector gets squashed to zero |
| λ = 1 | Eigenvector unchanged by transformation |
| λ < 0 | Eigenvector flipped and scaled |
| λ > 1 | Eigenvector stretched |
| 0 < λ < 1 | Eigenvector shrunk |

- An n×n matrix has **n eigenvalues** (can be repeated)
- Eigenvectors are **not unique** — any scalar multiple is also an eigenvector
- Eigenvectors for **different** eigenvalues are linearly independent

---

## NumPy

```python
import numpy as np

A = np.array([[4, 1],
              [2, 3]])

eigenvalues, eigenvectors = np.linalg.eig(A)

print("Eigenvalues: ", eigenvalues)       # [5. 2.]
print("Eigenvectors:\n", eigenvectors)    # columns are eigenvectors
```

> Note: `np.linalg.eig` returns eigenvectors as **columns**, not rows.

---

## Practice Questions

### P1 — Read off eigenvalues directly
State the eigenvalues and eigenvectors without any calculation:

```
A = [[7, 0],     B = [[1, 0],     C = [[1, 0],
     [0, 2]]          [0, 1]]          [0, 1]]
```

<details>
<summary>Answer</summary>

```
A: λ₁=7, v₁=[1,0]   λ₂=2, v₂=[0,1]   (diagonal matrix)
B: λ₁=1, v₁=[1,0]   λ₂=1, v₂=[0,1]   (identity — every vector is eigenvector)
C: same as B
```
</details>

---

### P2 — Characteristic equation
Find the eigenvalues:

```
A = [[3, 1],
     [1, 3]]
```

<details>
<summary>Answer</summary>

```
det(A - λI) = 0

A - λI = [[3-λ,  1  ],
           [1,   3-λ]]

det = (3-λ)(3-λ) - 1×1
    = (3-λ)² - 1
    = 9 - 6λ + λ² - 1
    = λ² - 6λ + 8
    = (λ-4)(λ-2)

λ₁ = 4,  λ₂ = 2
```
</details>

---

### P3 — Find eigenvectors
Using A from P2, find the eigenvectors for λ₁=4 and λ₂=2.

<details>
<summary>Answer</summary>

```
For λ₁ = 4:
A - 4I = [[-1, 1],
           [ 1,-1]]

-v₁ + v₂ = 0  →  v₂ = v₁
Eigenvector: [1, 1]

For λ₂ = 2:
A - 2I = [[1, 1],
           [1, 1]]

v₁ + v₂ = 0  →  v₂ = -v₁
Eigenvector: [1, -1]

Verify:
A @ [1,1]  = [3+1, 1+3] = [4,4]  = 4×[1,1]   ✅
A @ [1,-1] = [3-1, 1-3] = [2,-2] = 2×[1,-1]  ✅
```
</details>

---

### P4 — Full problem
Find eigenvalues and eigenvectors:

```
A = [[2, 3],
     [0, 4]]
```

<details>
<summary>Answer</summary>

```
det(A - λI) = (2-λ)(4-λ) - 3×0
            = (2-λ)(4-λ)

λ₁ = 2,  λ₂ = 4

For λ₁ = 2:
A - 2I = [[0, 3],
           [0, 2]]

0×v₁ + 3×v₂ = 0  →  v₂ = 0,  v₁ = free
Eigenvector: [1, 0]

For λ₂ = 4:
A - 4I = [[-2, 3],
           [ 0, 0]]

-2v₁ + 3v₂ = 0  →  v₁ = 3/2 × v₂
Eigenvector: [3, 2]

Verify:
A @ [1,0] = [2,0]  = 2×[1,0]   ✅
A @ [3,2] = [12,8] = 4×[3,2]   ✅
```
</details>

---

### P5 — True or False
```
1. A 3×3 matrix always has exactly 3 distinct eigenvalues.
2. If λ = 0, the matrix is singular.
3. Any scalar multiple of an eigenvector is also an eigenvector.
4. The identity matrix has eigenvalue 0.
5. Eigenvectors for different eigenvalues are linearly independent.
```

<details>
<summary>Answer</summary>

```
1. False  — eigenvalues can repeat (e.g. identity has λ=1 three times)
2. True   — det(A) = 0, so no inverse
3. True   — A@(cv) = c(Av) = c(λv) = λ(cv)
4. False  — identity has eigenvalue 1 (all vectors unchanged)
5. True   — always
```
</details>

---

### P6 — Conceptual (MCQ)
Matrix A has eigenvector v with eigenvalue λ=3. Which is necessarily true?

```
1. Applying A to v changes its length
2. Applying A to v changes its direction
3. None of the above
```

<details>
<summary>Answer</summary>

```
Answer: 3 — None of the above

Statement 1 — "length changes":
A @ v = 3v → length scales by 3, so length does change HERE.
But not necessarily true always — if λ=1, length stays the same.
So cannot say it is ALWAYS true.

Statement 2 — "direction changes":
ALWAYS false for eigenvectors — direction is always preserved by definition.
A @ v = λv means same direction, only scaled.

The only things NECESSARILY true for any eigenvector:
- Direction is always preserved
- Length changes only if |λ| ≠ 1
```
</details>

---

### P7 — NumPy
Find eigenvalues and eigenvectors of A from P4 using numpy and verify.

```python
import numpy as np

A = np.array([[2, 3],
              [0, 4]])

vals, vecs = np.linalg.eig(A)
print("Eigenvalues:", vals)
print("Eigenvectors (columns):\n", vecs)

# Verify: A @ v = λ @ v for each
for i in range(len(vals)):
    v = vecs[:, i]          # i-th column
    lhs = A @ v
    rhs = vals[i] * v
    print(f"\nλ={vals[i]}: A@v={lhs}, λv={rhs}, match={np.allclose(lhs, rhs)}")
```
