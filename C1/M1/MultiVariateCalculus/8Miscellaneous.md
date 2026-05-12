# Miscellaneous — Concepts and Practice

## Steepest Descent using Gradient

**Core idea:**
```
∇f  at point P  →  direction of steepest ASCENT
-∇f at point P  →  direction of steepest DESCENT
```

**Steps:**
1. Compute ∇f = [∂f/∂x, ∂f/∂y]
2. Evaluate at the given point (x₀, y₀)
3. Negate it → -∇f = steepest descent direction

---

**Example: f(x,y) = x² + y²  at point (1, 2)**
```
∂f/∂x = 2x,   ∂f/∂y = 2y

∇f = [2x, 2y]

At (1,2): ∇f = [2, 4]    ← steepest ascent
         -∇f = [-2, -4]   ← steepest descent
```

---

## Practice Problems

### P1 — f(x,y) = x² + 3y²  at (2, 1)
Find steepest descent direction.

<details>
<summary>Answer</summary>

```
∂f/∂x = 2x  →  at (2,1): 4
∂f/∂y = 6y  →  at (2,1): 6

∇f  = [4, 6]
-∇f = [-4, -6]  ← steepest descent
```
</details>

---

### P2 — f(x,y) = xy + x²  at (1, 3)
Find steepest descent direction.

<details>
<summary>Answer</summary>

```
∂f/∂x = y + 2x  →  at (1,3): 3+2 = 5
∂f/∂y = x       →  at (1,3): 1

∇f  = [5, 1]
-∇f = [-5, -1]  ← steepest descent
```
</details>

---

### P3 — f(x,y) = sin(x) + y²  at (π/2, 2)
Find steepest descent direction.

<details>
<summary>Answer</summary>

```
∂f/∂x = cos(x)  →  at (π/2, 2): cos(π/2) = 0
∂f/∂y = 2y      →  at (π/2, 2): 4

∇f  = [0, 4]
-∇f = [0, -4]  ← descent only in y-direction, flat in x
```
</details>

---

### P4 — f(x,y,z) = x² + y² + z²  at (1, 1, 1)
Find steepest descent direction.

<details>
<summary>Answer</summary>

```
∇f  = [2x, 2y, 2z]  →  at (1,1,1): [2, 2, 2]
-∇f = [-2, -2, -2]  ← steepest descent
```
</details>

---

## ML Connection

Gradient descent update at each step:
```
w_new = w_old - α × ∇f(w_old)

moving in -∇f direction by step size α (learning rate)
```
