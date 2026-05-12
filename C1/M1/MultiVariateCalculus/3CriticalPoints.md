# Critical Points — Maxima and Minima

## Why This Matters in ML

Almost all ML model training boils down to **minimising a cost function**.
Finding that minimum = finding the critical point. Derivatives are the tool.

---

## What is a Critical Point?

A point x where **f'(x) = 0** (or f is non-differentiable).

Something interesting happens here — the function stops increasing and starts decreasing (or vice versa).

```
f'(x) = 0  →  tangent is horizontal at that point
```

---

## Types of Critical Points

```
        maximum          inflexion         minimum
           ↓                 ↓                ↓
    *               *                          *
  *   *           *   *                      *   *
*       *       *       *                  *       *

f'=0, going        f'=0, doesn't          f'=0, going
+ to -             change sign            - to +
```

| Type | f'(x) | Meaning |
|------|-------|---------|
| Maximum | + → 0 → - | Function peaks |
| Minimum | - → 0 → + | Function valleys |
| Inflexion | + → 0 → + or - → 0 → - | Curvature changes, not a peak/valley |

---

## Method 1 — Check Sign of f'(x) Around the Point

For critical point x₀ where f'(x₀) = 0, check f'(x₀ - ε) and f'(x₀ + ε) where ε is small:

| f'(x₀ - ε) | f'(x₀ + ε) | Conclusion |
|------------|------------|------------|
| \+ | \- | Maximum |
| \- | \+ | Minimum |
| \+ | \+ | Inflexion |
| \- | \- | Inflexion |

---

## Method 2 — Second Derivative Test (faster)

Compute **f''(x)** at the critical point:

| f''(x₀) | Conclusion |
|---------|------------|
| \> 0 (positive) | Minimum — concave up ∪ |
| \< 0 (negative) | Maximum — concave down ∩ |
| = 0 | Inconclusive — use Method 1 or check higher derivatives |

> f''(x)=0 does NOT necessarily mean inflexion. Example: f(x)=x⁴ has f''(0)=0 but x=0 is a minimum.
> To confirm inflexion, check if f'' **changes sign** around the point.

**Memory trick:**
- f'' > 0 → "smiling" shape → minimum at bottom
- f'' < 0 → "frowning" shape → maximum at top
```
Yes — if f'' doesn't change sign, it's either max or min. Use f'' value to tell which:

  + → +  around point  →  minimum  (concave up ∪)
  - → -  around point  →  maximum  (concave down ∩)

  ---

  f'(x) = 0
      ↓
  compute f''(x)
      ↓
  f'' > 0  →  Minimum
  f'' < 0  →  Maximum
  f'' = 0  →  check sign of f'' around point
                  ↓
           sign changes  →  Inflexion
           sign same     →  Min (++) or Max (--)
```            
---

## Local vs Global

```
        global max
            *
           / \     local max
          /   \       *
         /     \     / \
        /       \   /   \
-------/         \ /     \-------
                  *
               local min          global min is at boundary
```

- **Local max/min** — highest/lowest in a neighbourhood
- **Global max/min** — highest/lowest over the entire domain

ML cost functions can have many local minima — gradient descent can get stuck in them.

---

## Worked Example

```
f(x) = x³ - 3x
```

**Step 1 — Find critical points:**
```
f'(x) = 3x² - 3 = 0
3(x² - 1) = 0
x = 1  or  x = -1
```

**Step 2 — Second derivative test:**
```
f''(x) = 6x

f''(1)  =  6 > 0  →  x=1  is a minimum
f''(-1) = -6 < 0  →  x=-1 is a maximum
```

**Values:**
```
f(1)  = 1 - 3  = -2   ← minimum value
f(-1) = -1 + 3 =  2   ← maximum value
```

---

## Python

```python
from sympy import symbols, diff, solve, sin

x = symbols('x')
f = x**3 - 3*x

f1 = diff(f, x)           # first derivative
f2 = diff(f, x, 2)        # second derivative

critical = solve(f1, x)   # solve f'(x) = 0
print("Critical points:", critical)    # [-1, 1]

for pt in critical:
    val = f2.subs(x, pt)
    if val > 0:
        print(f"x={pt} → Minimum")
    elif val < 0:
        print(f"x={pt} → Maximum")
    else:
        print(f"x={pt} → Inflexion")
```

---

## Inflexion Point Example

```
f(x) = x³

f'(x)  = 3x²  →  f'(0) = 0   ← critical point
f''(x) = 6x   →  f''(0) = 0  ← inflexion, not max or min
```

At x=0: f' goes + → 0 → + (doesn't change sign) → inflexion point.
The function changes from concave to convex here.
