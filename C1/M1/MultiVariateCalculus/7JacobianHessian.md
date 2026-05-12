# Vector-Valued Functions, Jacobian and Hessian

---

## Vector-Valued Functions

So far: one output. Now: **multiple outputs**.

```
Scalar function:        f(x) = x²           → single number output
Vector-valued function: f(t) = [t², 2t]     → vector output
```

### Example — Car motion
```
f(t) = [f₁(t), f₂(t)]

f₁(t) = t²     ← displacement
f₂(t) = 2t     ← velocity
```

### Derivative of a vector function
Differentiate **each component separately**:
```
f'(t) = [f₁'(t), f₂'(t)]
       = [2t, 2]

f₁'(t) = 2t   ← rate of change of displacement = velocity
f₂'(t) = 2    ← rate of change of velocity = acceleration
```

### Multivariable vector function
```
f(x, y) = [f₁(x,y), f₂(x,y)]
         = [x² + y,  x - y²]
```

Multiple inputs AND multiple outputs — the most general case.

---

## Jacobian Vector (scalar function)

For a **scalar** multivariable function f(x, y), the Jacobian is a **row vector** of all partial derivatives:

```
J = [∂f/∂x,  ∂f/∂y]
```

Same as the gradient but written as a **row vector** by convention.

### Example
```
f(x, y) = x² + y

J = [∂f/∂x,  ∂f/∂y]
  = [2x,      1    ]
```

At point (1, 2):
```
J(1,2) = [2×1, 1] = [2, 1]
```

Slope = 2 in x-direction, slope = 1 in y-direction.

---

## Jacobian Matrix (vector-valued function)

For a **vector-valued** multivariable function, the Jacobian is a **matrix**.

### Example
```
f(x, y) = [f₁(x,y),  f₂(x,y)]
         = [x² + y,   x - y² ]
```

Jacobian matrix:
```
J = [[∂f₁/∂x,  ∂f₁/∂y],
     [∂f₂/∂x,  ∂f₂/∂y]]

  = [[2x,   1 ],
     [ 1,  -2y]]
```

- Row 1 → derivatives of f₁
- Row 2 → derivatives of f₂

### General form
For f: Rⁿ → Rᵐ (n inputs, m outputs):
```
J is an m×n matrix

J_ij = ∂fᵢ/∂xⱼ
```

### Why Jacobian matters in ML
Deep learning models have thousands of parameters (weights). The Jacobian stores all derivatives of all outputs w.r.t. all parameters — used in backpropagation.

---

## Hessian Matrix

The Hessian is like the Jacobian but for **second-order partial derivatives** — it measures **curvature**.

```
H = [[∂²f/∂x²,    ∂²f/∂x∂y],
     [∂²f/∂y∂x,   ∂²f/∂y²  ]]
```

Always a **square n×n matrix** for f: Rⁿ → R.

### Example
```
f(x, y) = x³ + y³ + x²y
```

**First partial derivatives:**
```
∂f/∂x = 3x² + 2xy
∂f/∂y = 3y² + x²
```

**Second partial derivatives:**
```
∂²f/∂x²   = 6x + 2y
∂²f/∂y²   = 6y
∂²f/∂x∂y  = 2x      (mixed partial)
∂²f/∂y∂x  = 2x      (same as above — always equal for smooth functions)
```

**Hessian:**
```
H = [[6x + 2y,  2x],
     [2x,        6y]]
```

---

## Jacobian vs Hessian

| | Jacobian | Hessian |
|---|---|---|
| Contains | First-order partial derivatives | Second-order partial derivatives |
| Measures | **Slope** in all directions | **Curvature** in all directions |
| Shape | m×n (outputs × inputs) | n×n (always square) |
| Analogy | f'(x) for multivariable | f''(x) for multivariable |
| Used for | Gradient, backpropagation | Optimisation, finding max/min |

---

## Curvature vs Slope

```
Slope (Jacobian):    steepness of the straight line tangent to the surface
Curvature (Hessian): how quickly the slope is changing — how "bendy" the surface is

Flat region   → small Hessian values
Curvy region  → large Hessian values
```

---

## Taylor Series

Any smooth continuous function can be approximated as an infinite sum of its derivatives at a point.

**Taylor series centred at x = a:**
```
f(x) = f(a) + f'(a)(x-a) + f''(a)(x-a)²/2! + f'''(a)(x-a)³/3! + ...

     = Σ  f⁽ⁿ⁾(a) × (x-a)ⁿ / n!
       n=0
```

**Alternate form** — centred at x, step h:
```
f(x+h) = f(x) + f'(x)h + f''(x)h²/2! + f'''(x)h³/3! + ...
```

### Intuition
- **0th term:** f(a) — the value at the point (constant approximation)
- **1st term:** + f'(a)(x-a) — adds slope (linear approximation)
- **2nd term:** + f''(a)(x-a)²/2! — adds curvature (quadratic approximation)
- More terms → better approximation further from a

```
         actual f(x)
         ~~~~
        /    \        quadratic approximation (2 terms)
       / ___  \      --------
      / /   \  \    linear approximation (1 term)
-----/ /     \  \  ___________
```

### Example — eˣ centred at a=0
```
eˣ = 1 + x + x²/2! + x³/3! + x⁴/4! + ...
```

For small x:  eˣ ≈ 1 + x  (linear approximation)

### Why It Matters in ML
- Gradient descent derivations use first-order Taylor approximation
- Newton's method uses second-order (Hessian) approximation
- Many ML proofs and derivations rely on Taylor expansions
- Connects Jacobian (1st order) and Hessian (2nd order) to function approximation

```python
from sympy import symbols, series, exp, cos

x = symbols('x')

# Taylor series of eˣ around x=0, up to 5th order
print(series(exp(x), x, 0, 5))
# 1 + x + x²/2 + x³/6 + x⁴/24 + O(x⁵)

print(series(cos(x), x, 0, 6))
# 1 - x²/2 + x⁴/24 + O(x⁶)
```

---

## Python

```python
from sympy import symbols, diff, Matrix

x, y = symbols('x y')

f1 = x**2 + y
f2 = x - y**2

# Jacobian matrix
J = Matrix([[diff(f1,x), diff(f1,y)],
            [diff(f2,x), diff(f2,y)]])
print("Jacobian:\n", J)
# [[2x, 1], [1, -2y]]

# Hessian of a scalar function
f = x**3 + y**3 + x**2*y
H = Matrix([[diff(f,x,x), diff(f,x,y)],
            [diff(f,y,x), diff(f,y,y)]])
print("Hessian:\n", H)
# [[6x+2y, 2x], [2x, 6y]]
```
