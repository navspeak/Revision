# Partial Derivatives

## What is a Partial Derivative?

For a multivariable function, a partial derivative measures the **rate of change with respect to one variable, keeping all others constant**.

```
f(x, y)  →  ∂f/∂x  (partial w.r.t. x, treat y as constant)
             ∂f/∂y  (partial w.r.t. y, treat x as constant)
```

The ∂ symbol (pronounced "del") distinguishes partial from ordinary derivatives.

---

## Real-World Intuition

**Electricity bill = f(time, house_size)**

- ∂f/∂time → how bill changes with time, keeping house size fixed
- ∂f/∂size → how bill changes with house size, keeping time fixed

Each partial derivative **isolates the effect of one variable** on the output.

Used in:
- **Sensitivity analysis** — which input affects output most?
- **Gradient-based optimisation** — which direction to move each parameter?

---

## How to Compute

**Rule:** differentiate w.r.t. the target variable, treat all others as constants.

### Example: f(x, y) = x² + 3xy + y²

**∂f/∂x** — treat y as constant:
```
∂f/∂x = 2x + 3y + 0 = 2x + 3y
```

**∂f/∂y** — treat x as constant:
```
∂f/∂y = 0 + 3x + 2y = 3x + 2y
```

---

### Example: f(x, y) = x²y + sin(y)

**∂f/∂x** — treat y as constant:
```
∂f/∂x = 2xy   (y is just a constant multiplier)
```

**∂f/∂y** — treat x as constant:
```
∂f/∂y = x² + cos(y)
```

---

### Example: f(x, y, z) = x²y + yz³ + xz

**∂f/∂x:**
```
∂f/∂x = 2xy + 0 + z = 2xy + z
```

**∂f/∂y:**
```
∂f/∂y = x² + z³ + 0 = x² + z³
```

**∂f/∂z:**
```
∂f/∂z = 0 + 3yz² + x = 3yz² + x
```

---

## Geometric Meaning

For f(x, y) — a 3D surface:

- **∂f/∂x** = slope of the surface in the x-direction (slice the surface with a plane parallel to xz)
- **∂f/∂y** = slope of the surface in the y-direction (slice with a plane parallel to yz)

```
        z
        |    surface f(x,y)
        |   /
        |  /  ← slope in x-direction = ∂f/∂x
        | /
        +----------> x
       /
      y
```

---

## Evaluating at a Point

For f(x,y) = x² + 3xy + y², at point (1, 2):

```
∂f/∂x = 2x + 3y  →  at (1,2): 2(1) + 3(2) = 8
∂f/∂y = 3x + 2y  →  at (1,2): 3(1) + 2(2) = 7
```

---

## Python (SymPy)

```python
from sympy import symbols, diff

x, y, z = symbols('x y z')

f = x**2 + 3*x*y + y**2

df_dx = diff(f, x)    # 2x + 3y
df_dy = diff(f, y)    # 3x + 2y

print("∂f/∂x =", df_dx)
print("∂f/∂y =", df_dy)

# Evaluate at (1, 2)
print("∂f/∂x at (1,2):", df_dx.subs([(x,1),(y,2)]))   # 8
print("∂f/∂y at (1,2):", df_dy.subs([(x,1),(y,2)]))   # 7
```

---

## Practice Question

### f(x, y) = sin(xy) + 3xy — find ∂f/∂x and ∂f/∂y

**∂f/∂x** — treat y as constant:
```
Term 1: sin(xy)
  → chain rule: outer = sin → cos, inner = xy → y (treating y as constant)
  → y·cos(xy)

Term 2: 3xy
  → y is constant, so 3y is just a coefficient
  → 3y

∂f/∂x = y·cos(xy) + 3y
```

**∂f/∂y** — treat x as constant:
```
Term 1: sin(xy)
  → chain rule: outer = sin → cos, inner = xy → x (treating x as constant)
  → x·cos(xy)

Term 2: 3xy
  → x is constant, so 3x is just a coefficient
  → 3x

∂f/∂y = x·cos(xy) + 3x
```

**Notice the symmetry** — same structure, just x and y swapped. This happens because sin(xy) and xy are both symmetric in x and y.

---

### f(x, y) = xy·ln(xy) — find ∂f/∂x and ∂f/∂y

**∂f/∂x** — treat y as constant, apply product rule on xy and ln(xy):
```
u = xy      →  u' = y           (y is constant)
v = ln(xy)  →  v' = 1/(xy) × y = 1/x   (chain rule, inner = xy → y)

∂f/∂x = y·ln(xy) + xy·(1/x)
       = y·ln(xy) + y
       = y(ln(xy) + 1)
```

**∂f/∂y** — treat x as constant:
```
u = xy      →  u' = x           (x is constant)
v = ln(xy)  →  v' = 1/(xy) × x = 1/y   (chain rule, inner = xy → x)

∂f/∂y = x·ln(xy) + xy·(1/y)
       = x·ln(xy) + x
       = x(ln(xy) + 1)
```

**Again symmetric** — x and y swapped. Same pattern as sin(xy) example.

---

## Key Rule Summary

| Situation | What to do |
|-----------|-----------|
| Differentiating w.r.t. x | Treat all other variables as constants |
| Term has only y (no x) | Derivative = 0 w.r.t. x |
| Term has x and y multiplied | y is just a constant coefficient |
| sin(y), eʸ etc. (no x) | Derivative = 0 w.r.t. x |
