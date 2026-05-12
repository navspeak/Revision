# Total Derivatives

## What is a Total Derivative?

When f(x, y) and both x and y depend on another variable t, the **total derivative** measures the overall rate of change of f with respect to t.

```
df/dt = (∂f/∂x)(dx/dt) + (∂f/∂y)(dy/dt)
```

It's the **chain rule extended to multivariable functions** — each variable contributes to the total change.

---

## Intuition

Think of f as a room temperature that depends on position (x, y), and you're moving through the room over time t.

- ∂f/∂x × dx/dt → how much temperature changes because x is changing
- ∂f/∂y × dy/dt → how much temperature changes because y is changing
- df/dt → total rate of temperature change as you move

---

## Formula

For f(x, y) where x = x(t) and y = y(t):

```
df/dt = (∂f/∂x)(dx/dt) + (∂f/∂y)(dy/dt)
```

For f(x, y, z) where all depend on t:

```
df/dt = (∂f/∂x)(dx/dt) + (∂f/∂y)(dy/dt) + (∂f/∂z)(dz/dt)
```

---

## Worked Example

```
f(x, y) = π²x²y
x(t) = t² + 1
y(t) = t² - 1
```

**Step 1 — Partial derivatives of f:**
```
∂f/∂x = 2π²xy
∂f/∂y = π²x²
```

**Step 2 — Derivatives of x(t) and y(t):**
```
dx/dt = 2t
dy/dt = 2t
```

**Step 3 — Apply total derivative formula:**
```
df/dt = (∂f/∂x)(dx/dt) + (∂f/∂y)(dy/dt)
      = 2π²xy · 2t  +  π²x² · 2t
      = 4π²xyt + 2π²x²t
      = 2π²xt(2y + x)
```

**Step 4 — Substitute x = t²+1, y = t²-1:**
```
2y + x = 2(t²-1) + (t²+1) = 2t²-2 + t²+1 = 3t²-1

df/dt = 2π²(t²+1) · t · (3t²-1)
      = 2π²t(t²+1)(3t²-1)
```

---

## Partial vs Total Derivative

| | Partial ∂f/∂x | Total df/dt |
|---|---|---|
| Treats other vars as | Constants | Also changing (via t) |
| Used when | x, y independent | x, y both depend on t |
| Result | Rate of change in one direction | Overall rate of change |

---

## Python

```python
from sympy import symbols, diff, pi

t = symbols('t')
x = t**2 + 1
y = t**2 - 1

f = pi**2 * x**2 * y

df_dt = diff(f, t)
print("df/dt =", df_dt)
print("Simplified =", df_dt.factor())
# 2*pi**2*t*(t**2 + 1)*(3*t**2 - 1)
```

---

## Practice

### P1
```
f(x, y) = x² + y²
x(t) = sin(t)
y(t) = cos(t)

Find df/dt
```

<details>
<summary>Answer</summary>

```
∂f/∂x = 2x,   dx/dt = cos(t)
∂f/∂y = 2y,   dy/dt = -sin(t)

df/dt = 2x·cos(t) + 2y·(-sin(t))
      = 2sin(t)cos(t) - 2cos(t)sin(t)
      = 0

Makes sense! x²+y² = sin²t + cos²t = 1 (constant) → derivative = 0 ✅
```
</details>
