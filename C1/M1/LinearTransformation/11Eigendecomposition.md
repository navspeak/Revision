# Eigendecomposition of a Matrix

## What is Eigendecomposition?

Eigendecomposition breaks a matrix into three simpler matrices using its eigenvectors and eigenvalues.

```
A = P @ D @ P⁻¹

P  = matrix of eigenvectors (columns)
D  = diagonal matrix of eigenvalues
P⁻¹= inverse of eigenvector matrix
```

This only works for **square matrices with n linearly independent eigenvectors**.

---

## Why Decompose?

A diagonal matrix is the simplest possible transformation — just scaling.

Eigendecomposition says: **every matrix is just a diagonal matrix in disguise**, viewed from the right basis (eigenvector basis).

```
Step 1: P⁻¹ @ x  → change to eigenvector basis
Step 2: D @ ...   → apply simple scaling (diagonal)
Step 3: P @ ...   → change back to standard basis
```

Same as C⁻¹ @ A @ C from change of basis — same pattern.

---

## Building P and D

Given eigenvalues λ₁, λ₂ and eigenvectors v₁, v₂:

```
P = [v₁ | v₂]        ← eigenvectors as columns

D = [[λ₁,  0],        ← eigenvalues on diagonal
     [ 0,  λ₂]]
```

---

## Full Example

```
A = [[4, 1],
     [2, 3]]
```

From earlier: λ₁=5, v₁=[1,1]  and  λ₂=2, v₂=[1,-2]

**Build P and D:**
```
P = [[1,  1],       D = [[5, 0],
     [1, -2]]            [0, 2]]
```

**Find P⁻¹:**
```
det(P) = 1×(-2) - 1×1 = -3

P⁻¹ = (1/-3) × [[-2, -1],  =  [[ 2/3,  1/3],
                  [-1,  1]]     [ 1/3, -1/3]]
```

**Verify A = P @ D @ P⁻¹:**
```python
import numpy as np

A = np.array([[4, 1], [2, 3]])
P = np.array([[1,  1], [1, -2]])
D = np.diag([5, 2])

print(np.round(P @ D @ np.linalg.inv(P)))
# [[4. 1.]
#  [2. 3.]]  ✅
```

---

## Power of a Matrix using Eigendecomposition

Computing A¹⁰⁰ directly is expensive. With eigendecomposition:

```
A   = P @ D    @ P⁻¹
A²  = P @ D²   @ P⁻¹
A^n = P @ D^n  @ P⁻¹
```

Since D is diagonal, D^n is trivial:
```
D^n = [[λ₁ⁿ,  0  ],
       [0,    λ₂ⁿ]]
```

```python
n = 100
D_n = np.diag([5**n, 2**n])
A_100 = P @ D_n @ np.linalg.inv(P)
```

---

## When Eigendecomposition Fails

- Matrix is **not square**
- Matrix does not have n **linearly independent** eigenvectors (defective matrix)
- For such cases → use **SVD** (Singular Value Decomposition) instead

---

## Connection to PCA

In PCA:
- The data covariance matrix is eigendecomposed
- Eigenvectors = principal components (directions of maximum variance)
- Eigenvalues = how much variance each direction captures
- You keep the top k eigenvectors → dimensionality reduction

```
Covariance matrix C = P @ D @ P⁻¹

Sort eigenvalues largest → smallest
Keep top k eigenvectors → new basis
Project data onto new basis → fewer features, most variance retained
```

---

## NumPy

```python
import numpy as np

A = np.array([[4, 1],
              [2, 3]])

vals, vecs = np.linalg.eig(A)

P   = vecs                        # eigenvectors as columns
D   = np.diag(vals)               # eigenvalues on diagonal
P_inv = np.linalg.inv(P)

# Reconstruct A
A_reconstructed = P @ D @ P_inv
print("Reconstructed A:\n", np.round(A_reconstructed))  # should match A

# Matrix power
A_10 = P @ np.diag(vals**10) @ P_inv
print("\nA^10:\n", np.round(A_10))
```

---

## Summary

| Term | Meaning |
|------|---------|
| P | Matrix of eigenvectors (columns) |
| D | Diagonal matrix of eigenvalues |
| P⁻¹ | Change back to standard basis |
| A = P@D@P⁻¹ | Eigendecomposition |
| A^n = P@D^n@P⁻¹ | Efficient matrix powers |
| Fails when | Not square or not enough eigenvectors |
| Used in | PCA, SVD, Google PageRank, quantum computing |
