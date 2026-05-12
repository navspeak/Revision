# Transformations in a Different Basis

## The Problem

In standard basis, reflection matrix is:
```
A = [[1,  0],
     [0, -1]]   ← reflects about x-axis
```

If your vector is expressed in a **different basis**, you cannot directly apply A.
The reflection matrix A only works in standard basis — applying it to non-standard coordinates gives the wrong answer.

---

## The Solution — 3 Steps

```
Step 1: Convert vector from basis B → standard basis      multiply by C
Step 2: Apply transformation in standard basis            multiply by A
Step 3: Convert result back from standard → basis B       multiply by C⁻¹
```

In one formula:
```
T_B = C⁻¹ @ A @ C
```

Where:
- **C** = change of basis matrix (columns = basis vectors)
- **A** = transformation matrix in standard basis
- **C⁻¹** = converts back to original basis

---

## Why This Works

```
vector in B  →  ×C  →  vector in standard  →  ×A  →  transformed in standard  →  ×C⁻¹  →  transformed in B
```

You are borrowing the standard basis, doing the transformation there, then coming back.

---

## Example — Reflection in a Non-Standard Basis

Basis: v₁ = [1, 1], v₂ = [1, -1]
```
C = [[1,  1],
     [1, -1]]
```

Reflection about x-axis in standard basis:
```
A = [[1,  0],
     [0, -1]]
```

Transformation matrix in basis B:
```
T_B = C⁻¹ @ A @ C
```

---

## NumPy

```python
import numpy as np

C = np.array([[1,  1],
              [1, -1]])           # basis matrix

A = np.array([[1,  0],
              [0, -1]])           # reflection in standard basis

# Transformation matrix in basis B
T_B = np.linalg.inv(C) @ A @ C
print("T_B =\n", T_B)

# Vector in basis B
v_B = np.array([2, 3])

# Apply transformation in basis B directly
result_B = T_B @ v_B
print("Transformed in B:", result_B)

# Verify step by step
v_std     = C @ v_B              # Step 1: B → standard
v_std_t   = A @ v_std            # Step 2: transform in standard
v_back    = np.linalg.inv(C) @ v_std_t   # Step 3: standard → B
print("Step-by-step result:", v_back)    # should match result_B
```

---

## Key Formula

```
T_B = C⁻¹ @ A @ C
```

| Symbol | Meaning |
|--------|---------|
| C      | Basis matrix — columns are basis vectors |
| A      | Transformation in standard basis |
| C⁻¹   | Convert back to original basis |
| T_B    | Equivalent transformation in basis B |

This pattern — **C⁻¹ A C** — appears everywhere in linear algebra, including eigendecomposition.

---

## Exercises

### P1 — Step by step
Basis: v₁ = [1, 0], v₂ = [1, 1]
Vector in basis B: [2, 3]
Transformation: scaling by 2 in standard basis → A = [[2,0],[0,2]]

Find the transformed vector in basis B using T_B = C⁻¹ @ A @ C

<details>
<summary>Answer</summary>

```
C = [[1, 1],
     [0, 1]]

T_B = C⁻¹ @ A @ C

Step 1 — v in standard:  C @ [2,3] = [1×2+1×3, 0×2+1×3] = [5, 3]
Step 2 — transform:      A @ [5,3] = [10, 6]
Step 3 — back to B:      C⁻¹ @ [10,6]

C⁻¹ = [[1,-1],[0,1]]
C⁻¹ @ [10,6] = [10-6, 6] = [4, 6]

Transformed vector in B = [4, 6]
```
</details>

---

### P2 — Which formula?
You have a vector expressed in basis B and want to apply a rotation.
Fill in the blanks:

```
T_B  =  ___ @ A @ ___
```

And the 3 steps are:
1. ___
2. ___
3. ___

<details>
<summary>Answer</summary>

```
T_B = C⁻¹ @ A @ C

1. Multiply by C     → convert B → standard
2. Multiply by A     → apply rotation in standard
3. Multiply by C⁻¹  → convert standard → B
```
</details>

---

### P3 — Shear in a non-standard basis
Basis: v₁ = [2, 0], v₂ = [0, 1] → C = [[2,0],[0,1]]
Shear in standard: A = [[1,1],[0,1]]
Vector in B: [1, 2]

Find the transformed vector in B.

<details>
<summary>Answer</summary>

```
Step 1 — v in standard:  C @ [1,2] = [2, 2]
Step 2 — shear:          A @ [2,2] = [2+2, 2] = [4, 2]
Step 3 — back to B:      C⁻¹ @ [4,2]

C⁻¹ = [[0.5, 0],[0, 1]]
C⁻¹ @ [4,2] = [2, 2]

Transformed vector in B = [2, 2]
```
</details>

---

### P4 — Find the transformation MATRIX in a new basis
Basis: C = [[1, 2], [0, 1]]
Transformation: reflection about x-axis → A = [[1,0],[0,-1]]

Find T_B — the reflection matrix that works natively in basis B.

<details>
<summary>Answer</summary>

```
det(C) = 1×1 - 2×0 = 1

C⁻¹ = [[ 1, -2],
        [ 0,  1]]

Step 1 — A @ C:
[[1, 0],  @  [[1, 2],  =  [1×1+0×0,  1×2+0×1]  =  [[ 1,  2],
 [0,-1]]      [0, 1]]     [0×1-1×0,  0×2-1×1]       [ 0, -1]]

Step 2 — C⁻¹ @ (A @ C):
[[ 1,-2],  @  [[ 1,  2],  =  [1×1+(-2)×0,  1×2+(-2)×(-1)]  =  [[ 1,  4],
 [ 0, 1]]      [ 0, -1]]     [0×1+  1×0,   0×2+  1×(-1) ]      [ 0, -1]]

T_B = [[ 1,  4],
        [ 0, -1]]

This matrix performs reflection about x-axis natively in basis B.
```
</details>

---

### P5 — Rotation 90° anticlockwise in basis C = [[0,1],[1,1]]
(The example we worked through together)

Find T_B.

<details>
<summary>Answer</summary>

```
C = [[0, 1],      A = [[ 0, -1],
     [1, 1]]           [ 1,  0]]

det(C) = 0×1 - 1×1 = -1

C⁻¹ = (1/-1) × [[ 1, -1],  =  [[-1,  1],
                  [-1,  0]]      [ 1,  0]]

Step 1 — A @ C:
[[ 0,-1],  @  [[0,1],  =  [0×0+(-1)×1,  0×1+(-1)×1]  =  [[-1,-1],
 [ 1, 0]]      [1,1]]     [1×0+  0×1,   1×1+  0×1 ]       [ 0, 1]]

Step 2 — C⁻¹ @ (A @ C):
[[-1, 1],  @  [[-1,-1],  =  [(-1)(-1)+1×0,  (-1)(-1)+1×1]  =  [[ 1,  2],
 [ 1, 0]]      [ 0, 1]]     [ 1×(-1)+0×0,    1×(-1)+0×1 ]      [-1, -1]]

T_B = [[ 1,  2],
        [-1, -1]]
```
</details>

---

### P6 — Verify P5 in NumPy
Verify T_B from P5 using numpy.

```python
import numpy as np

C = np.array([[0, 1], [1, 1]])
A = np.array([[0, -1], [1, 0]])

T_B = np.linalg.inv(C) @ A @ C
print("T_B =\n", np.round(T_B))   # [[ 1,  2], [-1, -1]]
```

---

### P7 — Verify in NumPy (vector problem)
Using P3 values, verify that T_B @ v_B gives the same answer as the step-by-step approach.

```python
import numpy as np

C = np.array([[2, 0], [0, 1]])
A = np.array([[1, 1], [0, 1]])
v_B = np.array([1, 2])

T_B = np.linalg.inv(C) @ A @ C

result_direct    = T_B @ v_B
v_std            = C @ v_B
v_std_transformed = A @ v_std
result_stepwise  = np.linalg.inv(C) @ v_std_transformed

print("Direct:   ", result_direct)     # [2. 2.]
print("Stepwise: ", result_stepwise)   # [2. 2.]  ✅
```
