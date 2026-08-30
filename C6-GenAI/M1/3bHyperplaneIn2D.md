# Concept of a Hyperplane in 2D

Before SVMs, you need the idea of a **hyperplane**:

```
A hyperplane is the BOUNDARY that separates the data into its classes.
(for spam: it separates spam emails from ham emails)
```

It can be:

```
1D feature space → a point
2D feature space → a LINE          ← this note
3D feature space → a plane
nD feature space → an (n−1)-dim "hyperplane"  (beyond our imagination)
```

> A **line** used to separate one class from another **is** a hyperplane (in 2D).
> In fact, that line **is the model you are building**. See [[3aLinearClassificationNumericFeatures]].

---

## The Picture — Spam vs Ham in 2D

Take two numeric features, e.g. `word_freq_money` and `word_freq_technology`.
Each email is a point. A line splits the plane into two sides.

```
   x2 = word_freq_money
   │
   │   •  •            ← spam side (positive value)
   │  •  • •      ╱
   │ •  •      ╱
   │        ╱   ←  hyperplane:  W1·x1 + W2·x2 + c = 0
   │     ╱   ╳  ╳
   │  ╱    ╳  ╳  ╳     ← ham side (negative value)
   │╱     ╳  ╳
   └────────────────────  x1 = word_freq_technology
```

---

## The Equation of the Line

The standard equation of a line:

```
a·x + b·y + c = 0
```

Generalised for our features (rename a→W1, b→W2, x→x1, y→x2):

```
W1·x1 + W2·x2 + c = 0
```

```
x1, x2  = the features   (e.g. word_freq_technology, word_freq_money)
W1, W2  = the coefficients (the "weights" the model learns)
c       = the intercept / bias
```

The **W coefficients define the line**. Learning the model = finding good W1, W2, c.

---

## How the Line Classifies — the Sign Decides

For any email, plug its feature values into the left-hand side. You get a number.
**The sign of that number is the prediction:**

```
f(x) = W1·x1 + W2·x2 + c

   f(x) > 0   →  one class   (blue points)   ← e.g. ham
   f(x) < 0   →  other class (red points)    ← e.g. spam
   f(x) = 0   →  point lies ON the line (the hyperplane itself)
```

```
              f(x) > 0
                 ▲   •  •
                 │  •  •      (positive side)
   ──────────────┼──────────────  f(x) = 0   ← the hyperplane
                 │  ╳  ╳
                 ▼   ╳  ╳      (negative side)
              f(x) < 0
```

Any point sitting exactly on the line satisfies `W1·x1 + W2·x2 + c = 0` — that's the
definition of being on the boundary.

---

## Worked Mini-Example

Say the model learned `W1 = 2`, `W2 = 3`, `c = −6`, so:

```
f(x) = 2·x1 + 3·x2 − 6
```

| Email | x1 (technology) | x2 (money) | f(x) = 2x1+3x2−6 | Sign | Class |
|-------|-----------------|------------|------------------|------|-------|
| A | 0.0 | 3.0 | 0 + 9 − 6 = **+3** | + | blue / ham |
| B | 3.0 | 0.0 | 6 + 0 − 6 = **0**  | 0 | on the line |
| C | 0.0 | 0.5 | 0 + 1.5 − 6 = **−4.5** | − | red / spam |

Same line, three emails, decided purely by the **sign** of `f(x)`.

---

## Vector / Compact Form (you'll see this next)

The same equation written with vectors:

```
W · x + c = 0          where  W = [W1, W2],  x = [x1, x2]

prediction = sign(W · x + c)
```

This generalises instantly to n features — just a longer W and x. That's the whole
reason the boundary is called a *hyperplane*: the formula never changes, only the
dimension does.

---

## Summary

```
Hyperplane = the boundary separating classes.
  2D → a line:   W1·x1 + W2·x2 + c = 0

Classify by the SIGN of f(x) = W1·x1 + W2·x2 + c:
   f(x) > 0 → class A (blue)
   f(x) < 0 → class B (red)
   f(x) = 0 → on the line

The W coefficients ARE the model — learning = finding the best W1, W2, c.
Same equation in n-D = an (n−1)-dim hyperplane (next: 3D).
```

> **Next lecture:** what a hyperplane looks like in **3 dimensions** (a plane), and
> then the SVM question — *which* separating hyperplane is best? (the maximum-margin
> one). See the companion notebook `3b_Hyperplane2D.ipynb`.
