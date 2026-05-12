# Change of Basis

## Core Idea

Any basis can be represented as a matrix — columns are the basis vectors.

Multiply that matrix by the **coordinates in that basis** → you get the actual vector.

```
B @ coordinates = vector
```

---

## Example — Standard Basis

Standard basis vectors: î = [1,0], ĵ = [0,1]

Represent as matrix (columns = basis vectors):
```
B = [[1, 0],
     [0, 1]]   ← this is just the Identity matrix
```

Multiply by coordinates [3, 5]:
```
B @ [3, 5] = [[1,0], @ [3,  =  [3,
              [0,1]]    5]       5]
```

Makes sense — in standard basis, coordinates **are** the vector.

---

## Example — Non-Standard Basis

New basis vectors: v₁ = [2, 0], v₂ = [0, 3]

Represent as matrix:
```
B = [[2, 0],
     [0, 3]]
```

If coordinates in this basis are [1, 2]:
```
B @ [1, 2] = [[2,0], @ [1,  =  [2×1 + 0×2,   =  [2,
              [0,3]]    2]       0×1 + 3×2]        6]
```

Meaning: 1 step along v₁ + 2 steps along v₂ = vector [2, 6] in standard coordinates.

---

## Finding Coordinates in a Given Basis

Reverse problem: given a vector, what are its coordinates in basis B?

```
B @ coordinates = vector
→ coordinates = B⁻¹ @ vector
```

**Example:**

Vector v = [4, 6], Basis B = [[2, 0], [0, 3]]

```
coordinates = B⁻¹ @ [4, 6]

B⁻¹ = [[1/2, 0  ],
        [0,   1/3]]

B⁻¹ @ [4, 6] = [1/2×4 + 0×6,    =  [2,
                 0×4 + 1/3×6]        2]
```

So [4, 6] in standard = **[2, 2] in basis B**.

Verify: B @ [2,2] = [2×2, 3×2] = [4, 6] ✅

---

## Non-Orthogonal Basis Example

Basis: v₁ = [1, 1], v₂ = [1, -1]

```
B = [[1,  1],
     [1, -1]]
```

Coordinates [2, 3] in this basis → vector in standard:
```
B @ [2, 3] = [1×2 + 1×3,   =  [5,
              1×2 + (-1)×3]    -1]
```

Meaning: 2 steps along [1,1] + 3 steps along [1,-1] lands at [5,-1].

---

## NumPy

```python
import numpy as np

B = np.array([[2, 0],
              [0, 3]])

coords = np.array([1, 2])

# Basis coordinates → standard vector
vector = B @ coords
print("Vector:", vector)          # [2, 6]

# Standard vector → basis coordinates
v = np.array([4, 6])
coords_in_B = np.linalg.inv(B) @ v
print("Coordinates in B:", coords_in_B)   # [2. 2.]
```

---

## Key Rule

| Operation | Formula | Meaning |
|-----------|---------|---------|
| Basis → Standard | B @ coords | Express in standard coordinates |
| Standard → Basis | B⁻¹ @ vector | Find coordinates in new basis |
