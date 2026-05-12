# Matrix Exercises

---

## Q1 — Special Matrices
Identify the type of each matrix:

```
A = [[1, 0, 0],    B = [[3, 0, 0],    C = [[2, 5],
     [0, 1, 0],         [0, 7, 0],         [5, 2]]
     [0, 0, 1]]         [0, 0, 4]]
```

<details>
<summary>Answer</summary>

- A = Identity matrix (I)
- B = Diagonal matrix
- C = Symmetric matrix (C = Cᵀ)
</details>

---

## Q2 — Addition & Subtraction
Given:
```
A = [[1, 2],    B = [[5, 6],
     [3, 4]]         [7, 8]]
```
Find: A + B and A - B

<details>
<summary>Answer</summary>

```
A + B = [[6,  8],      A - B = [[-4, -4],
          [10, 12]]               [-4, -4]]
```
</details>

---

## Q3 — Scalar Multiplication
Given:
```
A = [[2, 4],
     [6, 8]]
```
Find: 3A and -½A

<details>
<summary>Answer</summary>

```
3A  = [[6,  12],     -½A = [[-1, -2],
        [18, 24]]             [-3, -4]]
```
</details>

---

## Q4 — Matrix Multiplication (can we multiply?)
State whether multiplication is possible and give the shape of the result:

- A (2×3) × B (3×4) → ?
- A (3×2) × B (3×2) → ?
- A (1×4) × B (4×1) → ?

<details>
<summary>Answer</summary>

- (2×3) × (3×4) → ✅ possible → result (2×4)
- (3×2) × (3×2) → ❌ not possible — inner dims 2 ≠ 3
- (1×4) × (4×1) → ✅ possible → result (1×1) — a single number (dot product)
</details>

---

## Q5 — Matrix Multiplication (compute)
Given:
```
A = [[1, 2],    B = [[5, 6],
     [3, 4]]         [7, 8]]
```
Find: A × B

<details>
<summary>Answer</summary>

```
C_11 = 1×5 + 2×7 = 5  + 14 = 19
C_12 = 1×6 + 2×8 = 6  + 16 = 22
C_21 = 3×5 + 4×7 = 15 + 28 = 43
C_22 = 3×6 + 4×8 = 18 + 32 = 50

A × B = [[19, 22],
          [43, 50]]
```
</details>

---

## Q6 — Is A×B = B×A?
Using the same A and B from Q5, find B × A and compare.

<details>
<summary>Answer</summary>

```
B × A:
C_11 = 5×1 + 6×3 = 5  + 18 = 23
C_12 = 5×2 + 6×4 = 10 + 24 = 34
C_21 = 7×1 + 8×3 = 7  + 24 = 31
C_22 = 7×2 + 8×4 = 14 + 32 = 46

B × A = [[23, 34],
          [31, 46]]
```
A×B ≠ B×A → matrix multiplication is NOT commutative
</details>

---

## Q7 — Identity Multiplication
Given:
```
A = [[3, 7],
     [2, 5]]
```
Show that A × I = A

<details>
<summary>Answer</summary>

```
I = [[1, 0],
     [0, 1]]

A × I:
Row 1: [3×1 + 7×0,  3×0 + 7×1] = [3, 7]
Row 2: [2×1 + 5×0,  2×0 + 5×1] = [2, 5]

Result = [[3, 7], [2, 5]] = A ✅
```
</details>

---

## Q8 — Transpose
Find Aᵀ:
```
A = [[1, 2, 3],
     [4, 5, 6]]
```
What is the shape of A and Aᵀ?

<details>
<summary>Answer</summary>

```
Aᵀ = [[1, 4],
       [2, 5],
       [3, 6]]
```
A is (2×3), Aᵀ is (3×2) — rows and columns swapped
</details>

---

## Q9 — Inverse
Given:
```
A = [[4, 7],
     [2, 6]]
```
Find A⁻¹ using the formula for a 2×2 matrix:
```
A⁻¹ = (1/det(A)) × [[d, -b], [-c, a]]
where A = [[a,b],[c,d]]
```

<details>
<summary>Answer</summary>

```
det(A) = 4×6 - 7×2 = 24 - 14 = 10

A⁻¹ = (1/10) × [[ 6, -7],
                  [-2,  4]]

     = [[0.6,  -0.7],
         [-0.2,  0.4]]

Verify: A × A⁻¹ = I ✅
```
</details>

---

## Q10 — System of Linear Equations
Solve using matrix form Ax = b:
```
2x + y = 8
5x + 3y = 21
```

<details>
<summary>Answer</summary>

```
A = [[2, 1],    b = [[8],
     [5, 3]]         [21]]

det(A) = 2×3 - 1×5 = 6 - 5 = 1

A⁻¹ = (1/1) × [[ 3, -1],
                 [-5,  2]]

x = A⁻¹ × b:
x = 3×8  + (-1)×21 = 24 - 21 = 3
y = -5×8 +  2×21   = -40 + 42 = 2

Solution: x = 3, y = 2 ✅
Verify: 2(3) + 2 = 8 ✓  and  5(3) + 3(2) = 21 ✓
```
</details>

---

## Q11 — How many solutions?
Without solving, state how many solutions each system has:

```
System 1:          System 2:          System 3:
x  + y = 4        x + y = 4          x + y = 4
2x + 2y = 8       2x + 2y = 9        x - y = 2
```

<details>
<summary>Answer</summary>

- System 1: **Infinite solutions** — second equation is just 2× the first (dependent)
- System 2: **No solution** — parallel lines (same slope, different intercept)
- System 3: **Unique solution** — x=3, y=1
</details>
