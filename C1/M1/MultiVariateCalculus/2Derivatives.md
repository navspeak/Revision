# Functions and Derivatives

## What is a Derivative?

The derivative measures the **rate of change** of a function at a point — how much the output changes for a tiny change in input.

```
f'(x) = df/dx = lim(h→0) [f(x+h) - f(x)] / h
```

**Geometrically:** slope of the tangent line at point x.

---

## First Principles (tedious but foundational)

Example: f(x) = x²
```
f'(x) = lim(h→0) [(x+h)² - x²] / h
       = lim(h→0) [x² + 2xh + h² - x²] / h
       = lim(h→0) [2xh + h²] / h
       = lim(h→0) 2x + h
       = 2x
```

In practice — use the rules below instead.

---

## Derivatives of Common Functions

### Powers
```
f(x) = xʳ  →  f'(x) = r·xʳ⁻¹

f(x) = x³  →  f'(x) = 3x²
f(x) = x   →  f'(x) = 1
f(x) = x⁰  →  f'(x) = 0   (constant)
```

### Exponential and Logarithmic
```
f(x) = eˣ      →  f'(x) = eˣ
f(x) = aˣ      →  f'(x) = aˣ · ln(a)
f(x) = ln(x)   →  f'(x) = 1/x
f(x) = log_a(x) → f'(x) = 1/(x · ln(a))
```

### Trigonometric
```
f(x) = sin(x)  →  f'(x) = cos(x)
f(x) = cos(x)  →  f'(x) = -sin(x)
f(x) = tan(x)  →  f'(x) = sec²(x) = 1/cos²(x)
```

---

## Rules for Combined Functions

### Constant Rule
```
f(x) = c  →  f'(x) = 0

f(x) = 5  →  f'(x) = 0
```

### Sum Rule
```
d/dx [αf(x) + βg(x)] = α·f'(x) + β·g'(x)

d/dx [3x² + 5x] = 6x + 5
```

### Product Rule
```
d/dx [f(x)·g(x)] = f'(x)·g(x) + f(x)·g'(x)

d/dx [x²·sin(x)] = 2x·sin(x) + x²·cos(x)
```

### Quotient Rule
```
d/dx [f(x)/g(x)] = [f'(x)·g(x) - f(x)·g'(x)] / g(x)²

d/dx [sin(x)/x] = [cos(x)·x - sin(x)·1] / x²
                = [x·cos(x) - sin(x)] / x²
```

### Chain Rule
```
If y = f(g(x)),  then  dy/dx = f'(g(x)) · g'(x)

outer derivative × inner derivative
```

Example: y = sin(x²)
```
outer: sin(u)  →  cos(u)
inner: x²      →  2x

dy/dx = cos(x²) · 2x
```

---

## Worked Example

```
f(x) = x³·eˣ + ln(x)
```

Using product rule on x³·eˣ, and sum rule:
```
d/dx [x³·eˣ] = 3x²·eˣ + x³·eˣ   (product rule)

d/dx [ln(x)] = 1/x

f'(x) = 3x²·eˣ + x³·eˣ + 1/x
       = eˣ(3x² + x³) + 1/x
       = x²·eˣ(3 + x) + 1/x
```

---

## Quick Reference Table

| f(x) | f'(x) |
|------|-------|
| c (constant) | 0 |
| xʳ | r·xʳ⁻¹ |
| eˣ | eˣ |
| aˣ | aˣ·ln(a) |
| ln(x) | 1/x |
| sin(x) | cos(x) |
| cos(x) | -sin(x) |
| tan(x) | sec²(x) |

---

## Practice Questions

### P1 — Basic derivatives
```
a) f(x) = x⁵
b) f(x) = 3x² + 2x + 1
c) f(x) = eˣ + ln(x)
d) f(x) = sin(x) + cos(x)
```

<details>
<summary>Answer</summary>

```
a) 5x⁴
b) 6x + 2
c) eˣ + 1/x
d) cos(x) - sin(x)
```
</details>

---

### P2 — Chain rule
```
a) f(x) = sin(cx)
b) f(x) = sin(x²)
c) f(x) = e^(3x)
d) f(x) = ln(x²)
```

<details>
<summary>Answer</summary>

```
a) c·cos(cx)        outer=sin→cos, inner=cx→c
b) 2x·cos(x²)       outer=sin→cos, inner=x²→2x
c) 3e^(3x)          outer=eᵘ→eᵘ,  inner=3x→3
d) 2x·(1/x²) = 2/x  outer=ln→1/u, inner=x²→2x

Common mistake on (a): writing cos(cx) without multiplying by c
```
</details>

---

### P3 — Product rule
```
a) f(x) = x²·sin(x)
b) f(x) = eˣ·ln(x)
```

<details>
<summary>Answer</summary>

```
a) 2x·sin(x) + x²·cos(x)
b) eˣ·ln(x) + eˣ·(1/x) = eˣ(ln(x) + 1/x)
```
</details>

---

### P4 — Quotient rule
```
f(x) = sin(x) / x
```

<details>
<summary>Answer</summary>

```
f'(x) = [cos(x)·x - sin(x)·1] / x²
       = [x·cos(x) - sin(x)] / x²
```
</details>

---

## In Python (SymPy)

```python
from sympy import symbols, diff, sin, exp, ln

x = symbols('x')

f = x**3 * exp(x) + ln(x)
print(diff(f, x))    # x**3*exp(x) + 3*x**2*exp(x) + 1/x

g = sin(x**2)
print(diff(g, x))    # 2*x*cos(x**2)  ← chain rule applied automatically
```
