# CDF — Its Relationship to PMF and PDF

The **CDF** is the running total of probability up to a value.

```
CDF: F(x) = P(X ≤ x)
     "What's the probability X is at most x?"

PMF / PDF: tells you about a SINGLE value
   PMF (discrete):    P(X = x)
   PDF (continuous):  f(x) — density at x (NOT a probability)
```

The CDF is **derived from** the PMF or PDF — it's their cumulative version.

---

## The Relationships in One Picture

```
Discrete:
   CDF: F(x) = Σ P(X = xᵢ)         ← SUM of PMF up to x
              xᵢ ≤ x

Continuous:
   CDF: F(x) = ∫ f(t) dt           ← INTEGRAL of PDF up to x
              −∞

Recovering PMF/PDF from CDF:
   Discrete:    P(X = x) = F(x) − F(x−)        ← jump in CDF
   Continuous:  f(x) = dF/dx                    ← derivative of CDF
```

---

## Discrete Case (PMF ↔ CDF)

Suppose `X` = number on a single die roll. PMF:

```
x      P(X = x)
1       1/6
2       1/6
3       1/6
4       1/6
5       1/6
6       1/6
```

The CDF `F(x) = P(X ≤ x)` is the running sum:

```
F(1) = P(X ≤ 1) = P(X=1)              = 1/6 ≈ 0.167
F(2) = P(X ≤ 2) = P(X=1) + P(X=2)     = 2/6 ≈ 0.333
F(3) = P(X ≤ 3) = ... + P(X=3)         = 3/6 = 0.500
F(4)                                    = 4/6 ≈ 0.667
F(5)                                    = 5/6 ≈ 0.833
F(6) = P(X ≤ 6) = ... + P(X=6)         = 6/6 = 1.000
```

### Visual — CDF Is a Staircase

```
F(x)
  1.0 │                              ┌───────
  0.83│                       ┌──────┘
  0.67│                ┌──────┘
  0.50│         ┌──────┘
  0.33│  ┌──────┘
  0.17│┌─┘
  0.0 │
      └──────────────────────────────────── x
         1    2    3    4    5    6
```

Each **step up** = the PMF value at that point.

```
PMF(x) = jump in CDF at x
       = F(x) − F(x − 1)        (for integer-valued)
```

```
P(X = 3) = F(3) − F(2)
        = 0.5  − 0.333
        = 0.167   ✓
```

---

## Continuous Case (PDF ↔ CDF)

For continuous `X` (e.g., heights), the PDF is a **density**, not a probability. `P(X = exactly anything) = 0`.

The CDF is the **integral** of the PDF:

```
F(x) = ∫ f(t) dt        from −∞ to x
```

### Example — Standard Normal

```
PDF:  f(x) = (1/√(2π)) · exp(−x²/2)        bell curve

CDF:  F(x) = area under the bell curve from −∞ to x
```

```
PDF f(x):                            CDF F(x):
   bell curve                            S-curve
        _                              
       / \                          1.0 │       ┌──────
      /   \                         0.5 │   ┌───┘
     /     \                        0.0 │───┘
   ____|____                            └───────────
     0                                    0
```

The CDF starts at 0, rises, and reaches 1 — a smooth S-curve for continuous distributions.

### Recovering PDF from CDF

```
f(x) = dF/dx          (derivative)
```

The PDF is the **slope** of the CDF at each point.

```
Where CDF rises STEEPLY → PDF is HIGH (lots of density)
Where CDF is FLAT        → PDF is LOW (little density)
```

---

## Computing Probabilities Using the CDF

The CDF is what you actually **use to compute probabilities**:

```
P(X ≤ a)         =  F(a)                     ← direct
P(X > a)         =  1 − F(a)
P(a < X ≤ b)     =  F(b) − F(a)              ← interval

For continuous variables:
   P(X = a) = 0           (no width)
   P(X ≤ a) = P(X < a)    (no jump)
```

### Example — Find P(2 < X ≤ 5) for the Die

```
P(2 < X ≤ 5) = F(5) − F(2)
            = (5/6) − (2/6)
            = 3/6 = 0.5
```

Same as `P(X=3) + P(X=4) + P(X=5)` but with **one subtraction** instead of a sum.

---

## Key Properties of a CDF

For any CDF `F`:

```
1. NON-DECREASING
   x₁ < x₂  →  F(x₁) ≤ F(x₂)
   (probability can only accumulate, never decrease)

2. STARTS AT 0
   lim F(x) = 0     as x → −∞

3. ENDS AT 1
   lim F(x) = 1     as x → +∞

4. RIGHT-CONTINUOUS
   F(x) is continuous from the right
   (matters only for discrete distributions — the steps)
```

---

## Why CDF Is Useful

```
✓ DIRECTLY gives probabilities of ranges
   P(X ≤ a), P(a < X ≤ b) — one or two function evaluations

✓ Works for BOTH discrete and continuous (unified concept)
   PMF and PDF look different; CDF looks the same

✓ Always BOUNDED in [0, 1]
   easy to interpret

✓ Survival function S(x) = 1 − F(x) is useful in reliability / survival analysis

✓ Enables INVERSE SAMPLING
   Generate uniform U ∈ [0,1], compute F⁻¹(U) → samples from the distribution
```

The PDF/PMF tells you "what does the distribution look like locally?". The CDF tells you "how much probability has accumulated?".

---

## Side-by-Side Comparison

| Aspect | PMF / PDF | CDF |
|--------|-----------|-----|
| **Symbol** | `p(x)` / `f(x)` | `F(x)` |
| **Meaning (discrete)** | P(X = x) — probability of exact value | P(X ≤ x) — cumulative |
| **Meaning (continuous)** | density (not probability) | P(X ≤ x) — cumulative |
| **Range** | discrete: [0, 1]; continuous: ≥ 0 (can be > 1) | always [0, 1] |
| **Sum/integral** | sums/integrates to 1 | reaches 1 at the right end |
| **Shape** | bell, spike, etc. | non-decreasing, starts at 0, ends at 1 |
| **Recovery from CDF** | — | Differentiate (continuous) or difference (discrete) |
| **Usage** | "Shape of the distribution" | "Probability of being ≤ a value" |

---

## In Code

### Discrete — Binomial

```python
from scipy.stats import binom

n, p = 10, 0.5

# PMF — probability of exact value
print(binom.pmf(5, n, p))     # P(X = 5)
# ≈ 0.246

# CDF — cumulative
print(binom.cdf(5, n, p))     # P(X ≤ 5)
# ≈ 0.623

# Verify: CDF is the SUM of PMF
total = sum(binom.pmf(k, n, p) for k in range(6))
print(total)                   # ≈ 0.623 (same as cdf(5, n, p))
```

### Continuous — Normal

```python
from scipy.stats import norm

# PDF (density)
print(norm.pdf(0))             # density at x=0 — about 0.399

# CDF
print(norm.cdf(0))             # P(X ≤ 0) — exactly 0.5
print(norm.cdf(1.96))          # P(X ≤ 1.96) — about 0.975
print(norm.cdf(1.96) - norm.cdf(-1.96))  # P(−1.96 < X < 1.96) ≈ 0.95

# Recovering PDF from CDF via numerical derivative
import numpy as np
x = np.linspace(-3, 3, 1000)
F = norm.cdf(x)
f_estimated = np.gradient(F, x)   # ≈ PDF
```

---

## Visual Recap

```
PMF (discrete):                CDF (discrete):
     |                         1.0│         ┌────
   |   |                          │     ┌───┘
 | | | | |                     0.5│  ┌──┘
 ___________                   0.0│──┘
                                  └────────────────
                                  
PDF (continuous):              CDF (continuous):
   smooth bell                    smooth S-curve
      /\                       1.0│      ┌────────
     /  \                         │    ┌─┘
    /    \                     0.5│  ┌─┘
   ________                    0.0│ ─┘
                                  └────────────────
```

In all cases: the CDF goes from **0 to 1**, monotonically.

---

## Common Use Cases

```
"What's the probability of at most 5 successes?"
   → P(X ≤ 5) = F(5)

"What's the probability of more than 5?"
   → P(X > 5) = 1 − F(5)

"What's the probability of between 3 and 7?"
   → P(3 < X ≤ 7) = F(7) − F(3)

"What value has 95% of the probability below it?"
   → x such that F(x) = 0.95   (the 95th percentile)
   → use inverse CDF: F⁻¹(0.95)
```

The **inverse CDF** (`ppf` in scipy) is how you compute quantiles / percentiles.

```python
from scipy.stats import norm
norm.ppf(0.95)   # ≈ 1.645 — the 95th percentile of standard normal
```

---

## The Empirical CDF

For a sample (not a known distribution), you can compute the **empirical CDF**:

```
F_n(x) = (number of data points ≤ x) / n
```

Use it when you don't know the distribution but have data:

```python
import numpy as np
import matplotlib.pyplot as plt

data = np.random.randn(100)
sorted_data = np.sort(data)
ecdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

plt.step(sorted_data, ecdf, where='post')
plt.xlabel('x'); plt.ylabel('F(x)')
plt.title('Empirical CDF')
```

The empirical CDF converges to the true CDF as `n → ∞` (Glivenko-Cantelli theorem).

---

## Summary

```
CDF = F(x) = P(X ≤ x)
   "Accumulated probability up to x"

Relationship to PMF (discrete):
   F(x) = Σ P(X = xᵢ)        ← running sum
          xᵢ ≤ x
   
   PMF = jump in CDF: P(X = x) = F(x) − F(x−)

Relationship to PDF (continuous):
   F(x) = ∫ f(t) dt           ← integral
          from −∞ to x
   
   PDF = derivative of CDF: f(x) = dF/dx

Why use CDF:
   ✓ Probabilities of ranges in one or two evaluations
   ✓ Unified concept for discrete & continuous
   ✓ Always bounded [0, 1]
   ✓ Foundation for inverse sampling and quantiles
```

> PMF / PDF describe the **shape** of the distribution.
> CDF tracks how much **probability has accumulated**.
> They contain the same information, but the CDF is what you usually use to compute actual probabilities.
