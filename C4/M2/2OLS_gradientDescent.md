# OLS Closed-Form: β = (XᵀX)⁻¹ Xᵀy

---

## Why matrices?

Each observation is a row, each feature is a column. For `n` observations and `p` features, the whole dataset is one matrix multiplication away from a solution — no loops, no gradient steps.

---

## Setup: 3 data points, fit y = β₀ + β₁x

| x | y |
|---|---|
| 1 | 2 |
| 2 | 4 |
| 3 | 5 |

**Design matrix X** — prepend a column of 1s for the intercept β₀:

```
    [1  x]
X = [1  1]  ← row 1: (1, y=2)
    [1  2]  ← row 2: (2, y=4)
    [1  3]  ← row 3: (3, y=5)

y = [2]
    [4]
    [5]

β = [β₀]   ← what we're solving for
    [β₁]
```

The model is: **Xβ = ŷ** (predicted values)

---

## Step 1 — Compute XᵀX (2×2 matrix)

```
Xᵀ = [1  1  1]    X = [1  1]
     [1  2  3]        [1  2]
                       [1  3]

XᵀX = [1·1+1·1+1·1   1·1+1·2+1·3]  =  [3   6]
      [1·1+2·1+3·1   1·1+2·2+3·3]     [6  14]
```

Always a square (p×p) matrix. Diagonal = sum of squares, off-diagonal = cross products between features.

---

## Step 2 — Compute Xᵀy (2×1 vector)

```
Xᵀy = [1·2 + 1·4 + 1·5]  =  [11]
      [1·2 + 2·4 + 3·5]     [25]
```

Captures how each feature relates to the target.

---

## Step 3 — Invert XᵀX

For a 2×2 matrix `[[a,b],[c,d]]`, inverse = `(1/det) × [[d,-b],[-c,a]]`

```
det(XᵀX) = 3×14 - 6×6 = 42 - 36 = 6

(XᵀX)⁻¹ = (1/6) × [14  -6]  =  [ 7/3   -1 ]
                    [-6   3]     [ -1   1/2 ]
```

---

## Step 4 — Multiply: β = (XᵀX)⁻¹ Xᵀy

```
β = [ 7/3   -1 ] × [11]
    [ -1   1/2 ]   [25]

β₀ = (7/3)×11 + (-1)×25  =  77/3 - 25  =  2/3  ≈  0.667
β₁ = (-1)×11  + (1/2)×25  = -11 + 12.5  =  1.5
```

**Model: ŷ = 0.667 + 1.5x**

---

## Verification

| x | Actual y | Predicted ŷ | Residual |
|---|----------|-------------|----------|
| 1 | 2 | 2.167 | −0.167 |
| 2 | 4 | 3.667 | +0.333 |
| 3 | 5 | 5.167 | −0.167 |

Residuals sum to ≈ 0 — a property of OLS. No other line through this data produces a smaller sum of squared residuals.

---

## Where does the formula come from?

### SSE — In Simple Terms

```
SSE = Σ (yᵢ − ŷᵢ)²
```

| Symbol | Meaning |
|--------|---------|
| Σ | sum over all rows |
| yᵢ | actual value (what really happened) |
| ŷᵢ | predicted value (what the model guessed) |
| (yᵢ − ŷᵢ) | residual — how wrong the model was for that row |
| (yᵢ − ŷᵢ)² | squared so negatives don't cancel positives |

For our 3 points after iteration 1 (β₀=0, β₁=0.5):

| x | y | ŷ | residual | residual² |
|---|---|---|----------|-----------|
| 1 | 2 | 0.5 | 1.5 | 2.25 |
| 2 | 4 | 1.0 | 3.0 | 9.00 |
| 3 | 5 | 1.5 | 3.5 | 12.25 |
| | | | **SSE** | **23.5** |

The goal of both OLS and Gradient Descent is to find β₀ and β₁ that make this number as small as possible.

OLS minimises SSE = Σ(y − ŷ)² = (y − Xβ)ᵀ(y − Xβ)

Take the derivative with respect to β and set to zero:

```
d(SSE)/dβ = 0
⟹  -2Xᵀ(y - Xβ) = 0
⟹  Xᵀy = XᵀXβ          ← "normal equations"
⟹  β = (XᵀX)⁻¹ Xᵀy     ← multiply both sides by (XᵀX)⁻¹
```

The name "normal equations" comes from the fact that at the solution, the residuals are **orthogonal (normal)** to the column space of X — the model has extracted everything it can from the features.

---

## The Column of 1s — Intercept Trick

The first column of X is always all 1s. This is intentional.

The intercept β₀ is a constant added to every prediction:

```
ŷ = β₀ + β₁x
```

To write this as a single matrix multiplication **Xβ = ŷ**, β₀ needs a "feature" to multiply against. A column of 1s does exactly that — multiplying any value by 1 leaves it unchanged:

```
X = [1  x₁]     β = [β₀]
    [1  x₂]         [β₁]
    [1  x₃]

Xβ = [1·β₀ + x₁·β₁]   =   [β₀ + β₁x₁]   ✓
     [1·β₀ + x₂·β₁]       [β₀ + β₁x₂]
     [1·β₀ + x₃·β₁]       [β₀ + β₁x₃]
```

Without it you'd have to handle β₀ separately — this way the entire model, including the intercept, lives inside one clean formula: **β = (XᵀX)⁻¹ Xᵀy**.

### What if you skip it?

The regression line is forced through the origin (β₀ = 0). Sometimes valid (physics laws, unit conversions), but almost always wrong for real data.

```python
# sklearn adds the 1s column automatically (fit_intercept=True by default)
# If building X manually in numpy, add it yourself:
import numpy as np
X = np.column_stack([np.ones(len(x)), x])
```

---

## Why "no iteration needed"? — Gradient Descent vs OLS

Gradient descent iteratively nudges β toward the minimum. OLS jumps straight to it via matrix inversion. For small/medium data this is exact and fast. The catch: inverting XᵀX is O(p³) — for thousands of features, iterative methods (gradient descent) become cheaper.

### The loss surface

SSE = Σ(y − ŷ)² forms a bowl shape in β-space. Every point on the bowl is a candidate line; the bottom of the bowl is the best line.

```
Loss
  │     *
  │   *   *
  │  *     *
  │ *       *
  │*         *
  └────────────── β₁
         ↑
       minimum = OLS solution
```

### How one gradient descent step works

The gradient tells you which direction is "uphill". Move in the opposite direction (downhill) by a small step:

```
β_new = β_old − α × ∂(SSE)/∂β

∂(SSE)/∂β₁ = -2 Σ xᵢ(yᵢ − ŷᵢ)   ← slope of loss w.r.t. β₁
∂(SSE)/∂β₀ = -2 Σ (yᵢ − ŷᵢ)      ← slope of loss w.r.t. β₀
```

`α` is the **learning rate** — how big each step is.

### What is α (learning rate)?

`α` is a small number you choose before training that controls how big each step down the hill is.

**Why 0.01 specifically?** It's just a typical starting value. The right choice depends on the problem:

```
Too large (α = 1.0)   → steps overshoot the minimum, loss bounces or explodes
Too small (α = 0.0001) → steps are tiny, takes forever to converge
Just right (α = 0.01)  → steady progress, converges smoothly
```

```
Loss                        Loss                       Loss
  │  *                        │*                         │     *
  │    *  ← overshoots        │ *                        │   *
  │  *                        │  *                       │  *
  │    *                      │   *                      │ *
  └──────── β₁                └──────── β₁               └──────── β₁
  Too large α                Too small α               Good α
```

**α is not learned — you set it.**

- β₀ and β₁ are **parameters** — the model learns them from data
- α is a **hyperparameter** — you set it before training; it controls *how* learning happens, not *what* is learned

This is why OLS has no α at all. There are no steps, so there is nothing to tune — you just solve the equation directly.

### Concrete example — same 3 points, true answer β₁ = 1.5

**α = 1.0 (too large)**

```
Iter 1:
  β₁ = 0, residuals = [2, 4, 5]
  gradient = -50
  β₁ = 0 − 1.0 × (−50) = 50        ← jumps way past 1.5

Iter 2:
  ŷ = [50, 100, 150], residuals = [−48, −96, −145]
  gradient = −2(1×−48 + 2×−96 + 3×−145) = +1350
  β₁ = 50 − 1.0 × 1350 = −1300     ← explodes in the opposite direction
```

Each step gets worse, not better.

**α = 0.0001 (too small)**

```
Iter 1:
  gradient = -50
  β₁ = 0 − 0.0001 × (−50) = 0.005  ← tiny step

Iter 2:
  gradient ≈ -49.86
  β₁ = 0.005 + 0.005 = 0.010

Iter 1000:  β₁ ≈ 0.05               ← still nowhere near 1.5
```

Technically moving in the right direction but painfully slow.

**α = 0.01 (just right)**

```
Iter 1:  β₁ = 0.00 → 0.50
Iter 2:  β₁ = 0.50 → 0.86
Iter 3:  β₁ = 0.86 → 1.10
Iter 4:  β₁ = 1.10 → 1.27
...
Iter ~50: β₁ ≈ 1.5  ✓
```

Steady steps, converges to the right answer.

**Summary**

```
α = 1.0    →  overshoots, bounces, explodes      ✗
α = 0.0001 →  moves right but needs 10,000 steps ✗
α = 0.01   →  converges cleanly in ~50 steps     ✓
```

There is no formula to get the perfect α — you try a few values, watch the loss, and pick what works.

### What does the gradient of β₁ mean?

The gradient is the **slope of the loss curve at your current position**.

It answers: *"If I increase β₁ by a tiny amount, does the loss go up or down, and by how much?"*

```
Loss
  │         *              gradient = steep positive slope
  │       *                → β₁ is too small, move right
  │     *     ← you are here
  │   *  ← gradient = 0   → you're at the minimum, stop
  │ *
  └──────────────── β₁
     0   0.5   1.5
```

- **Large negative gradient (−50):** loss is falling steeply as β₁ increases → β₁ needs to go up a lot
- **Small gradient:** you're near the bottom → small adjustment needed
- **Gradient = 0:** you're at the minimum → stop

### Relationship between Iteration 1 and 2

**The output of iteration 1 is the input of iteration 2.** Each iteration uses the β updated by the previous one.

```
Iteration 1:
  Start:     β₁ = 0
  Residuals: [2, 4, 5]       ← big, model is far off
  Gradient:  -50              ← steep, large correction needed
  Update:    β₁ = 0 + 0.5 = 0.5

        ↓  feed β₁=0.5 into next iteration

Iteration 2:
  Start:     β₁ = 0.5
  ŷ = [0.5, 1.0, 1.5]        ← predictions improved
  Residuals: [1.5, 3.0, 3.5]  ← smaller than before
  Gradient:  -36              ← less steep, smaller correction needed
  Update:    β₁ = 0.5 + 0.36 = 0.86

        ↓  feed β₁=0.86 into next iteration
        ...
        → eventually β₁ converges to 1.5
```

Each iteration: residuals shrink → gradient shrinks → update shrinks → β₁ creeps toward the true value.

**The pattern:** every iteration makes the model slightly less wrong than the one before.

### Concrete example (same 3 points)

Start with β₀=0, β₁=0 (predicts 0 for everything), α=0.01:

```
Iteration 1:
  ŷ = β₀ + β₁x = 0 + 0·x = 0  → predicts 0 for every x

  x=1: actual=2, ŷ=0, residual = 2−0 = 2
  x=2: actual=4, ŷ=0, residual = 4−0 = 4
  x=3: actual=5, ŷ=0, residual = 5−0 = 5

  residuals = [2, 4, 5]  (just the original y — model hasn't learned anything yet)
  ŷ = [0, 0, 0]   residuals = [2, 4, 5]
  gradient β₁ = -2 Σ xᵢ(yᵢ − ŷᵢ)   ← formula: each x × its residual, sum, multiply by -2

  i=1: x=1, residual=2  → 1×2  =  2
  i=2: x=2, residual=4  → 2×4  =  8
  i=3: x=3, residual=5  → 3×5  = 15
                           sum  = 25

  gradient β₁ = -2 × 25 = -50
  (-2 comes from differentiating the squared loss — chain rule on (y − β₀ − β₁x)²)

  β₁ = 0 - 0.01×(-50) = 0 + 0.5 = 0.5
  (subtracting a negative gradient → β₁ grows toward the true value 1.5)

Iteration 2:
  ŷ = [0.5, 1.0, 1.5]   residuals = [1.5, 3, 3.5]
  gradient β₁ = -2(1·1.5 + 2·3 + 3·3.5) = -2×19 = -38
  β₁ = 0.5 - 0.01×(-38) = 0.88

... hundreds of steps later → β₁ ≈ 1.5  (same as OLS)
```

OLS got there in one formula. Gradient descent took hundreds of steps to converge to the same answer.

### Why O(p³) is the bottleneck for OLS

Inverting a matrix of size p×p requires roughly p³ operations.

| Features (p) | p³ operations |
|---|---|
| 10 | 1,000 |
| 100 | 1,000,000 |
| 1,000 | 1,000,000,000 |
| 10,000 | 10,000,000,000,000 |

With 10,000 features (common in NLP, genomics), OLS inversion becomes impractical. Gradient descent scales much better — each step is just O(n×p), and you can even do it on mini-batches.

### The Big Picture

Both OLS and Gradient Descent are trying to do the **same thing** — find the line y = β₀ + β₁x that sits as close as possible to the actual data points.

They just take different routes to get there:

| | OLS | Gradient Descent |
|---|---|---|
| **How** | Solve directly using matrix formula | Repeatedly adjust β using differentiation |
| **Steps** | One shot | Many iterations |
| **Tool** | Matrix inversion: β = (XᵀX)⁻¹ Xᵀy | Derivative of loss: β = β − α × ∂(SSE)/∂β |
| **Analogy** | Solving for x in ax = b algebraically | Feeling your way downhill in the dark |

The destination is the same — the best fitting line. Only the journey differs.

### When to use which

| | OLS | Gradient Descent |
|---|---|---|
| Features | Small–medium (p < ~10k) | Large / very large |
| Speed | One shot, exact | Many iterations, approximate |
| Memory | Must fit XᵀX in RAM | Can stream data |

---

## sklearn — OLS Only, No Learning Rate

sklearn's `LinearRegression()` uses OLS internally — no iterations, no learning rate:

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)   # solves β = (XᵀX)⁻¹ Xᵀy directly
```

Learning rate α is not a concept here — OLS is one matrix calculation, done.

If you explicitly want gradient descent for linear regression, use `SGDRegressor`:

```python
from sklearn.linear_model import SGDRegressor

model = SGDRegressor(learning_rate='constant', eta0=0.01)
```

For Logistic Regression there is no closed-form solution (sigmoid makes the math non-linear), so sklearn **must** use an iterative solver:

```python
from sklearn.linear_model import LogisticRegression

LogisticRegression(solver='lbfgs', max_iter=100)
#                                  ↑
#                    how many iterations the solver gets to converge
```

`max_iter` is the equivalent concern for Logistic Regression — not learning rate, but how many steps the solver runs.

| | LinearRegression | LogisticRegression |
|-|------------------|--------------------|
| Internal method | OLS (closed-form) | Iterative solver (lbfgs etc.) |
| Learning rate | Not applicable | Not exposed — solver manages it |
| Key parameter | — | `solver`, `max_iter` |
| Used by | `sklearn LinearRegression` | Neural networks, large-scale ML |
