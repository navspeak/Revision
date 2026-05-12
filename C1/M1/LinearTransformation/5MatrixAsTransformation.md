# Matrix as a Linear Transformation

## Key Idea

Every linear transformation can be written as **matrix multiplication**:

```
T(x̂) = A @ x̂
```

The matrix A **is** the transformation. Feed it a vector, get a transformed vector back.

---

## Example in NumPy

```python
import numpy as np

A = np.array([[2, 0],
              [0, 3]])

x = np.array([1, 2])

T_x = A @ x
print(T_x)   # [2, 6]
```

What happened:
```
input  x = [1, 2]
output     [2×1 + 0×2,  0×1 + 3×2]  =  [2, 6]

x-component scaled by 2
y-component scaled by 3
```

---

## More Transformations via A

### Scaling
```python
A = np.array([[3, 0], [0, 3]])
A @ np.array([1, 2])   # [3, 6] — scaled uniformly
```

### Reflection (flip across x-axis)
```python
A = np.array([[1, 0], [0, -1]])
A @ np.array([1, 2])   # [1, -2] — y flipped
```

### Shear
```python
A = np.array([[1, 2], [0, 1]])
A @ np.array([1, 2])   # [5, 2] — x pushed by 2×y
```

### Rotation by 90°
```python
A = np.array([[0, -1], [1, 0]])
A @ np.array([1, 0])   # [0, 1] — rotated 90° anticlockwise
```

---

## Verify Linearity via A

Since T(x̂) = A @ x̂, both conditions are automatically satisfied:

```
Additivity:   A @ (u + v) = A@u + A@v   ✅  (matrix distributive law)
Homogeneity:  A @ (cu)    = c(A@u)       ✅  (scalar pulls out)
```

This is why **every matrix defines a linear transformation** — and why we study them together.

---

## What the Columns of A Tell You

The columns of A show where the **basis vectors land** after transformation:

```
A = [[2, 0],
     [0, 3]]

î = [1,0]  →  A @ [1,0] = [2, 0]   ← first column
ĵ = [0,1]  →  A @ [0,1] = [0, 3]   ← second column
```

Know where î and ĵ go → you know where **everything** goes.
