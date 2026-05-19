# p-Value — Formulas and Worked Examples

The **p-value** is the probability of observing a test statistic as extreme (or more extreme) as the one you got, assuming H₀ is true.

```
p-value = P(test stat as extreme as observed | H₀ true)
```

Small p-value → your data is surprising under H₀ → evidence against H₀.

---

## First: Z_observed vs Z*

A common confusion — these are **different things**:

```
Z_observed (Z):
   Computed FROM YOUR DATA
   Z = (x̄ − μ₀) / SE
   "What your sample tells you"

Z* (Z-critical):
   Looked up FROM Z-TABLE
   Boundary of the rejection region at chosen α
   "The threshold to compare against"
```

```
Decision:
   |Z_observed| > |Z*|  →  REJECT H₀ (in the tail beyond Z*)
   |Z_observed| ≤ |Z*|  →  fail to reject H₀
```

```
Example:
   Z_observed = 2.1   (computed from your data)
   Z* = ±1.96         (looked up for α = 0.05 two-tailed)
   |2.1| > 1.96       → REJECT H₀
```

These are **two separate numbers playing different roles**.

---

## The Three p-Value Formulas

The formula depends on which **direction** your alternative hypothesis (H₁) is.

```
Right-tailed test  (H₁: μ > μ₀):
   p = P(Z > Z_observed)
     = 1 − F(Z_observed)

Left-tailed test   (H₁: μ < μ₀):
   p = P(Z < Z_observed)
     = F(Z_observed)

Two-tailed test    (H₁: μ ≠ μ₀):
   p = 2 × P(Z > |Z_observed|)
     = 2 × (1 − F(|Z_observed|))
```

Where `F(z) = P(Z ≤ z)` is the standard normal CDF.

---

## Visual — What Each Formula Captures

```
Right-tailed:                           Left-tailed:

       fail to reject     REJECT          REJECT         fail to reject
       ───────────────────  ────           ────           ──────────────
                          Z_obs              Z_obs
                          
       p = area to RIGHT of Z_obs           p = area to LEFT of Z_obs


Two-tailed:

       REJECT          fail to reject               REJECT
       ──────       ────────────────────             ──────
                                 0
              -|Z_obs|                          +|Z_obs|

       p = BOTH tail areas combined = 2 × one-tail area
```

The p-value is always the **area in the tails beyond the observed statistic**.

---

## Why 2× for Two-Tailed?

```
Two-tailed alternative: H₁: μ ≠ μ₀
   → REJECT if Z is large in EITHER direction (positive or negative)
   → "extreme" means far from 0 in EITHER tail

Symmetric normal:
   P(Z > 1.5) = P(Z < −1.5) = same value (by symmetry)

Total tail area = P(Z > 1.5) + P(Z < −1.5) = 2 × P(Z > 1.5)
```

Hence the factor of 2.

---

## Worked Example 1 — Right-Tailed Test

```
Claim:   New medication reduces healing time by MORE than the average.
H₀:      μ = 7 days  (no improvement over baseline)
H₁:      μ < 7 days  (medication is FASTER — LEFT-tailed actually)

Wait — let me reframe as RIGHT-tailed:
Claim:   New fertiliser INCREASES yield above the standard 50 kg.
H₀:      μ = 50
H₁:      μ > 50    (right-tailed)

Sample:  n = 36, x̄ = 53, σ = 6
α = 0.05
```

### Step-by-Step

```
SE = σ / √n = 6 / √36 = 1.0

Z_observed = (x̄ − μ₀) / SE
            = (53 − 50) / 1.0
            = 3.0

Direction: right-tailed (H₁: μ > μ₀)
   → p-value = P(Z > 3.0)
            = 1 − F(3.0)
            = 1 − 0.9987
            = 0.0013

Decision (α = 0.05):
   0.0013 < 0.05  →  REJECT H₀
   → strong evidence that fertiliser increases yield
```

Or using Z*:

```
Z* (right-tailed, α=0.05) = +1.645
Z_observed = 3.0 > 1.645  →  REJECT H₀  ✓ same answer
```

---

## Worked Example 2 — Left-Tailed Test

```
Claim:   New process REDUCES defect rate below 5%.
H₀:      p = 0.05    (no improvement)
H₁:      p < 0.05    (defect rate decreased — left-tailed)

Sample:  n = 400, found 12 defects.
α = 0.05
```

### Step-by-Step

```
p̂ = 12 / 400 = 0.03
SE = √(p₀(1−p₀)/n)
   = √(0.05 × 0.95 / 400)
   = √(0.0475/400)
   = √0.0001188
   = 0.0109

Z_observed = (p̂ − p₀) / SE
            = (0.03 − 0.05) / 0.0109
            = −0.02 / 0.0109
            = −1.835

Direction: left-tailed (H₁: p < p₀)
   → p-value = P(Z < −1.835)
            = F(−1.835)
            = 0.0333

Decision (α = 0.05):
   0.0333 < 0.05  →  REJECT H₀
   → evidence the defect rate is below 5%
```

Or using Z*:

```
Z* (left-tailed, α=0.05) = −1.645
Z_observed = −1.835 < −1.645  →  REJECT H₀  ✓ same answer
```

---

## Worked Example 3 — Two-Tailed Test (the Brand A Example)

```
Claim:   "70% of customers prefer Brand A."
H₀:      p = 0.70
H₁:      p ≠ 0.70    (two-tailed)

Sample:  n = 200, 130 said yes
α = 0.05
```

### Step-by-Step

```
p̂ = 130 / 200 = 0.65
SE = √(p₀(1−p₀)/n)
   = √(0.70 × 0.30 / 200)
   = √0.00105
   = 0.0324

Z_observed = (0.65 − 0.70) / 0.0324
            = −1.543

Direction: two-tailed (H₁: p ≠ p₀)
   → p-value = 2 × P(Z > |−1.543|)
             = 2 × P(Z > 1.543)
             = 2 × (1 − F(1.543))
             = 2 × (1 − 0.9386)
             = 2 × 0.0614
             = 0.1228   ≈ 0.123

Decision (α = 0.05):
   0.123 > 0.05  →  FAIL to reject H₀
   → insufficient evidence that the proportion differs from 70%
```

Or using Z*:

```
Z* (two-tailed, α=0.05) = ±1.96
|Z_observed| = 1.543 < 1.96  →  FAIL to reject H₀  ✓ same answer
```

---

## All Three Decision Rules — Equivalent

For any test, three equivalent ways to decide:

```
RULE 1: Compare Z_observed to Z*
   |Z_observed| > |Z*|   →   reject H₀

RULE 2: Check if μ₀ is in CI
   μ₀ NOT in CI          →   reject H₀

RULE 3: Compare p-value to α
   p < α                 →   reject H₀
```

```
All three SHOULD give the SAME answer.
They're three views of the same evidence.
```

---

## p-Value Tables — Common Values

```
p-value rough guide:

   p < 0.001    →  very strong evidence against H₀
   p < 0.01     →  strong evidence
   p < 0.05     →  moderate evidence (typical threshold)
   p < 0.10     →  weak evidence (marginal)
   p ≥ 0.10     →  insufficient evidence
```

```
Common α values:
   α = 0.05     →  most common
   α = 0.01     →  stricter
   α = 0.10     →  exploratory
```

---

## In Python

```python
from scipy import stats

z_obs = 1.543

# Right-tailed
p_right = 1 - stats.norm.cdf(z_obs)
print(f"Right-tailed p: {p_right:.4f}")    # 0.0614

# Left-tailed (use negative z)
p_left = stats.norm.cdf(-z_obs)
print(f"Left-tailed p:  {p_left:.4f}")     # 0.0614 (same by symmetry)

# Two-tailed
p_two = 2 * (1 - stats.norm.cdf(abs(z_obs)))
print(f"Two-tailed p:   {p_two:.4f}")      # 0.1228

# Alternative — using survival function (numerically stable for large z)
p_two = 2 * stats.norm.sf(abs(z_obs))
print(f"Two-tailed (sf): {p_two:.4f}")    # 0.1228
```

### For t-Tests

Use t-CDF instead:

```python
df = 24    # degrees of freedom
t_obs = 1.543

# Same three formulas, but with stats.t.cdf and df
p_right = 1 - stats.t.cdf(t_obs, df)
p_left  = stats.t.cdf(t_obs, df)
p_two   = 2 * (1 - stats.t.cdf(abs(t_obs), df))
```

---

## What "Extreme" Means by Direction

```
RIGHT-TAILED (H₁: μ > μ₀):
   "extreme" = far in the POSITIVE direction
   p-value uses RIGHT tail only

LEFT-TAILED (H₁: μ < μ₀):
   "extreme" = far in the NEGATIVE direction
   p-value uses LEFT tail only

TWO-TAILED (H₁: μ ≠ μ₀):
   "extreme" = far from 0 in EITHER direction
   p-value uses BOTH tails (hence 2×)
```

The direction of H₁ tells you which tail(s) count.

---

## Decision Rule with p-Value

```
If p < α  →  REJECT H₀     (your data is surprising under H₀)
If p ≥ α  →  FAIL to reject (data is consistent with H₀)
```

This is **equivalent** to the |Z_observed| vs |Z*| comparison:

```
p < α  ⇔  |Z_observed| > |Z*|
   → both mean "in the rejection region"
```

---

## Common Misinterpretations

```
✗ "p-value is the probability that H₀ is true"
   → WRONG. p-value assumes H₀ IS true and computes
     the probability of seeing the observed (or more extreme) data.

✗ "If p > 0.05, then H₀ is true"
   → WRONG. Failing to reject ≠ proving H₀.
   → It means "insufficient evidence to REJECT".

✗ "Lower p-value means a bigger effect"
   → WRONG. Small p-value means strong EVIDENCE,
     but the effect size could still be tiny (especially with large n).

✓ p-value = "How surprising is my data, ASSUMING H₀?"
✓ Small p → data is surprising under H₀ → maybe H₀ is wrong
```

---

## Reference Table

| Test type | Alternative | p-value formula | When extreme means |
|-----------|------------|-----------------|---------------------|
| **Right-tailed** | H₁: μ > μ₀ | `p = 1 − F(Z)` | Z is large positive |
| **Left-tailed** | H₁: μ < μ₀ | `p = F(Z)` | Z is large negative |
| **Two-tailed** | H₁: μ ≠ μ₀ | `p = 2 × (1 − F(|Z|))` | Z is large in either direction |

For t-tests: same formulas, replace `F` (standard normal CDF) with `F_t(·;  df)` (t-CDF with appropriate degrees of freedom).

---

## Summary

```
p-value = probability of seeing your test statistic OR more extreme,
          IF H₀ were true.

The 3 formulas depend on H₁'s direction:
   Right-tailed:   p = 1 − F(Z_observed)
   Left-tailed:    p = F(Z_observed)
   Two-tailed:     p = 2 × (1 − F(|Z_observed|))

Decision rule:
   p < α  →  REJECT H₀
   p ≥ α  →  fail to reject H₀

Equivalent to comparing |Z_observed| with |Z*|:
   |Z_observed| > |Z*|  ⇔  p < α
```

> The **p-value** tells you how surprising your data is **under H₀**. Small p → data is unlikely if H₀ were true → reject. The exact formula depends on **which way** your alternative hypothesis points — one tail or both.
