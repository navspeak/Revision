# Least Squares Approximation

## When is it used?

When a system of equations **Ax = b has no exact solution** — b lies outside the column space of A.

Used heavily in **linear regression** where A is rarely square and exact solutions don't exist.

---

## The Problem

System of 3 equations, 3 unknowns:
```
2x - y - z  =  1
2x - y + z  =  0
4x - 2y - 3z = -1
```

Matrix form Ax = b:
```
A = [[2, -1, -1],      b = [1,
     [2, -1,  1],           0,
     [4, -2, -3]]          -1]
```

```python
import numpy as np

A = np.array([[2, -1, -1],
              [2, -1,  1],
              [4, -2, -3]])

b = np.array([1, 0, -1])

np.linalg.matrix_rank(A)   # returns 2
```

**rank = 2** → A squishes 3D space onto a 2D plane.

---

## Why No Exact Solution?

```
3D input space  →  A  →  2D plane (column space of A)
```

- Every vector Ax lands on that 2D plane
- Vector b does **not** lie on that plane
- So no x exists such that Ax = b exactly

```
         Column space (2D plane)
              ↗
    * * * * *
    * * * * *       b ← outside the plane
    * * * * *
```

---

## The Least Squares Solution

Instead of Ax = b (impossible), find x̂ that minimises:

```
||Ax - b||²     ← squared distance between Ax and b
```

The closest point on the column space to b — the **projection of b onto the column space**.

**Formula:**
```
x̂ = (AᵀA)⁻¹ Aᵀ b
```

- **Aᵀ** = transpose of A
- **(AᵀA)⁻¹Aᵀ** is called the **pseudo-inverse** of A

---

## Why This Formula?

```
Aᵀ A x̂ = Aᵀ b
```

Multiplying both sides by Aᵀ projects b onto the column space of A.
This is called the **normal equation**.

---

## Geometric Meaning

```
         b (target, unreachable)
         |
         | ← residual (error = b - Ax̂)
         |
    Ax̂  ← closest point on column space
    (projection of b)
```

Least squares finds x̂ such that the **residual is perpendicular to the column space** — that's the minimum error point.

---

## NumPy

```python
import numpy as np

A = np.array([[2, -1, -1],
              [2, -1,  1],
              [4, -2, -3]], dtype=float)

b = np.array([1, 0, -1], dtype=float)

# Manual formula: x̂ = (AᵀA)⁻¹ Aᵀ b
x_hat = np.linalg.inv(A.T @ A) @ A.T @ b
print("Least squares solution:", x_hat)

# NumPy built-in
x_lstsq, residuals, rank, sv = np.linalg.lstsq(A, b, rcond=None)
print("lstsq solution:", x_lstsq)

# How close is Ax̂ to b?
print("Ax̂ =", A @ x_hat)
print("b  =", b)
print("Residual:", b - A @ x_hat)
```

---

## Why it Matters in ML

In **linear regression**: y = Xβ

- X = data matrix (n samples × p features) → almost never square
- β = coefficients to find
- y = target values

Exact solution rarely exists → least squares gives best fit:
```
β̂ = (XᵀX)⁻¹ Xᵀ y
```

This is literally what linear regression computes under the hood.

---

## Summary

| Concept | Meaning |
|---------|---------|
| Ax = b unsolvable | b lies outside column space of A |
| Least squares | Find x̂ that minimises \|\|Ax - b\|\|² |
| Formula | x̂ = (AᵀA)⁻¹ Aᵀb |
| Geometric meaning | Project b onto column space — closest point |
| Residual | b - Ax̂ — the leftover error |
| Used in | Linear regression, curve fitting, overdetermined systems |
