# Matrices — Recap

## Components of a Matrix
- A matrix is a rectangular array of numbers with **m rows** and **n columns** → shape (m × n)
- Each element addressed as **a_ij** (row i, column j)

## Special Matrices
- **Square matrix** — same number of rows and columns (n × n)
- **Identity matrix (I)** — square matrix with 1s on diagonal, 0s elsewhere
  - A × I = A (multiplication has no effect — like multiplying by 1)
- **Zero matrix** — all elements are 0
- **Diagonal matrix** — non-zero values only on the main diagonal
- **Symmetric matrix** — A = Aᵀ (transpose equals itself)

---

## Operations on Matrices

### Addition & Subtraction
- Matrices must be the **same shape**
- Add/subtract element by element

### Scalar Multiplication
- Multiply every element by the scalar

### Matrix Multiplication
- **A (m×n) × B (n×p) = C (m×p)**
- Inner dimensions must match; result takes outer dimensions
- Each element C_ij = dot product of row i of A with column j of B
- **Not commutative** — A×B ≠ B×A in general

### Transpose (Aᵀ)
- Flip rows and columns: element at (i,j) moves to (j,i)
- Shape (m×n) → (n×m)

---

## Inverse of a Matrix (A⁻¹)
- Only exists for **square matrices** where **det(A) ≠ 0**
- A × A⁻¹ = I
- If det(A) = 0 → matrix is **singular** → no inverse

---

## Systems of Linear Equations
Represent as **Ax = b** where:
- **A** = coefficient matrix
- **x** = unknowns vector
- **b** = constants vector

Solve by: **x = A⁻¹ b** (if inverse exists)

### Three possible outcomes:
| Case | Meaning |
|------|---------|
| Unique solution | det(A) ≠ 0 — lines/planes meet at one point |
| Infinite solutions | Equations are dependent — lines/planes overlap |
| No solution | Equations are inconsistent — lines/planes are parallel |

---
```
@ is the matrix multiplication operator in Python (introduced in Python 3.5).
  
  A = np.array([[1, 2], [3, 4]])
  B = np.array([[5, 6], [7, 8]])

  A @ B      # matrix multiplication

  Same as np.matmul(A, B) — just cleaner syntax.

  ---
  Don't confuse with *:

  A * B      # element-wise multiplication (each element × each element)
  A @ B      # matrix multiplication (dot product of rows × columns)

  A = [[1,2],   B = [[5,6],
       [3,4]]        [7,8]]

  A * B = [[1×5, 2×6],   = [[5,  12],    ← element-wise
            [3×7, 4×8]]      [21, 32]]

  A @ B = [[1×5+2×7, 1×6+2×8],  = [[19, 22],  ← matrix multiply
            [3×5+4×7, 3×6+4×8]]    [43, 50]]

Yes — @ does both, depending on the input:
  
  ┌─────────────────────┬────────────────────────────────┐
  │        Input        │          What @ does           │
  ├─────────────────────┼────────────────────────────────┤
  │ 1D array @ 1D array │ Dot product → scalar           │
  ├─────────────────────┼────────────────────────────────┤
  │ 2D array @ 2D array │ Matrix multiplication → matrix │
  ├─────────────────────┼────────────────────────────────┤
  │ 2D array @ 1D array │ Matrix × vector → vector       │
  └─────────────────────┴────────────────────────────────┘

  a = np.array([1, 2, 3])
  b = np.array([4, 5, 6])
  a @ b          # dot product → 32 (scalar)

  A = np.array([[1, 2], [3, 4]])
  B = np.array([[5, 6], [7, 8]])
  A @ B          # matrix multiply → 2x2 matrix

  v = np.array([1, 2])
  A @ v          # matrix × vector → [5, 11]

  Dot product is actually just a special case of matrix multiplication — so @ handles all of them with one operator.
```