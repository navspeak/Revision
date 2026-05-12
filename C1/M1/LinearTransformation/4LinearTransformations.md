# Linear Transformations

## What is a Transformation?

A transformation T takes a **vector as input** and returns a **vector as output**.

```
T: Rⁿ → Rᵐ

input vector → T → output vector
```

### Example 1 — Scaling transformation
```
T(x̂) = 3x̂   defined on R²

T(1, 2) = (3, 6)

input: [1, 2]  →  output: [3, 6]
```

### Example 2 — Shift transformation
```
T(x, y) = (x + 1, y + 1)

T(0, 0) = (1, 1)   ← origin moves!
```

**Key difference:**
- Example 1: T(0,0) = (0,0) → origin is **fixed**
- Example 2: T(0,0) = (1,1) → origin is **not fixed**

---

## What Makes a Transformation Linear?

Three geometric conditions must hold:

| Condition | Meaning |
|-----------|---------|
| Lines stay lines | A straight line input → straight line output |
| Origin is fixed | T(0) = 0 always |
| Grid lines stay parallel and equidistant | No bending, no uneven stretching |

### Algebraic conditions (how to test it)

A transformation T is linear if and only if **both** hold for all vectors u, v and scalar c:

```
1. Additivity:       T(u + v) = T(u) + T(v)
2. Homogeneity:      T(cu)    = c·T(u)
```

These two can be combined into one:

```
T(cu + dv) = c·T(u) + d·T(v)
```

### Why these conditions matter

- **Additivity** — transforming a sum = sum of transformations
- **Homogeneity** — scaling input = scaling output
- Together they mean: **T preserves the structure of the vector space**

---

## Test: Is T Linear?

### T(x, y) = (3x, 3y) — scaling ✅
```
T(u + v) = 3(u + v) = 3u + 3v = T(u) + T(v)  ✅
T(cu)    = 3(cu)    = c(3u)   = c·T(u)         ✅
Origin:  T(0,0) = (0,0)                         ✅
→ Linear
```

### T(x, y) = (x + 1, y + 1) — shift ❌
```
T(0, 0) = (1, 1) ≠ (0, 0)
→ Origin not fixed → NOT linear
```

---

## What's Next
Matrices as linear transformations — every linear transformation can be represented as a matrix multiplication.
