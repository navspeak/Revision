# Gradients

## What is a Gradient?

The gradient of f(x, y, z) is a **vector of all its partial derivatives**:

```
∇f = [∂f/∂x,  ∂f/∂y,  ∂f/∂z]
```

∇ is called "nabla" or "del". It collects all partial derivatives into one vector.

---

## Example

```
f(x, y) = x² + y²

∂f/∂x = 2x
∂f/∂y = 2y

∇f = [2x, 2y]
```

At point (1, 2):
```
∇f(1,2) = [2×1, 2×2] = [2, 4]
```

This vector points in the direction of **steepest ascent** at (1,2).

---

## Geometric Meaning

```
        y
        ↑
    ↗ ↗ ↑ ↗ ↗
    ↗ ↗ ↑ ↗ ↗     ← gradient vectors at each point
    ↗ ↗ * ↗ ↗        point toward steepest ascent
    ↗ ↗ ↑ ↗ ↗
        +----------> x
```

- **∇f at a point** → direction of steepest **ascent** (going up fastest)
- **-∇f at a point** → direction of steepest **descent** (going down fastest)

For f(x,y) = x² + y² (bowl shape):
- Gradient always points away from the centre (outward)
- Negative gradient always points toward the minimum at (0,0)

---

## Why Gradient Matters in ML — Gradient Descent

Training a model = minimising a loss function L(w₁, w₂, ..., wₙ)

```
∇L = [∂L/∂w₁,  ∂L/∂w₂,  ...,  ∂L/∂wₙ]
```

**Gradient descent update rule:**
```
w_new = w_old - α × ∇L

α = learning rate (how big a step to take)
```

Step in the **opposite direction of gradient** → move toward minimum.

```
Loss surface:
         *          ← start here
        / \
       /   \
      *     \       ← step in direction of -∇L
       \     \
        *     *     ← minimum
```

---

## Three Variable Example

```
f(x, y, z) = x²y + yz³ + xz

∂f/∂x = 2xy + z
∂f/∂y = x² + z³
∂f/∂z = 3yz² + x

∇f = [2xy + z,  x² + z³,  3yz² + x]
```

At point (1, 1, 1):
```
∇f(1,1,1) = [2+1,  1+1,  3+1] = [3, 2, 4]
```

---

## Gradient vs Derivative

| | Univariate f(x) | Multivariable f(x,y,...) |
|---|---|---|
| Rate of change | f'(x) — scalar | ∇f — vector |
| Direction info | sign of f' (+/-) | direction of ∇f vector |
| Steepest ascent | move in +f' direction | move in ∇f direction |
| Steepest descent | move in -f' direction | move in -∇f direction |

---

## Python

```python
from sympy import symbols, diff, Matrix

x, y = symbols('x y')

f = x**2 + y**2

grad = Matrix([diff(f, x), diff(f, y)])
print("∇f =", grad)            # [2x, 2y]

# Evaluate at (1, 2)
grad_at_point = grad.subs([(x,1),(y,2)])
print("∇f(1,2) =", grad_at_point)   # [2, 4]
```

---

## Key Takeaways

- Gradient = vector of all partial derivatives
- Points in direction of **steepest ascent**
- Negative gradient = direction of **steepest descent**
- **Gradient descent** moves opposite to gradient to find minimum
- Foundation of all optimisation in ML
