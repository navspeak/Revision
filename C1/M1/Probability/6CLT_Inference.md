# CLT → Confidence Intervals & Hypothesis Tests

The Central Limit Theorem gives us the framework. From there, the same building blocks (Z*, SE, ME) drive **both confidence intervals and hypothesis tests**.

```
CLT gives the foundation:
   "Sample means are normally distributed around μ with SE = σ/√n"

From that, two interrelated tools:
   1. Confidence Interval (CI):   x̄ ± ME = x̄ ± Z* · SE
   2. Hypothesis Test:             compare Z = (x̄ − μ₀)/SE to Z*
```

---

## The Building Blocks

```
CLT          →  sample means follow Normal(μ, σ²/n)
SE           →  σ/√n  (standard error of the mean)
CL           →  Confidence Level (e.g., 95%, 99%)
α            →  1 − CL/100  (significance level)
Z*           →  CRITICAL Z-value (the boundary in the Z-table for that CL)
Z            →  COMPUTED test statistic from the sample
ME           →  Z* · SE  (margin of error)
```

---

## Path 1 — Confidence Interval (CI)

```
You sampled n values. Got x̄. Want a RANGE for μ.

Step 1: Choose CL (e.g., 95%)
Step 2: Look up Z* for CL/2 in each tail
            CL = 90%   →  Z* = 1.645
            CL = 95%   →  Z* = 1.96
            CL = 99%   →  Z* = 2.576

Step 3: Compute SE = σ / √n

Step 4: Compute ME = Z* · SE

Step 5: CI = x̄ ± ME

Result: "We are 95% confident μ is in [x̄ − ME, x̄ + ME]"
```

### Visual

```
                ME = Z* · SE
   ←──────────────|──────────────→
                 x̄
   |─────────────|─────────────|
                 ↑
            sample mean
   ←──── ME ────→←──── ME ────→
   
   CI = [x̄ − ME,  x̄ + ME]
```

### Quick Example

```
σ = 10, n = 100, x̄ = 50, CL = 95%

SE = 10/√100 = 1
Z* = 1.96
ME = 1.96 × 1 = 1.96

CI = 50 ± 1.96 = [48.04, 51.96]
   → 95% confident μ is in [48.04, 51.96]
```

---

## Path 2 — Hypothesis Test (Compare Z to Z*)

```
You're testing if μ equals some hypothesised value μ₀.

Step 1: State hypotheses
            H₀: μ = μ₀
            H₁: μ ≠ μ₀  (two-tailed)
            or H₁: μ > μ₀  (right-tailed)
            or H₁: μ < μ₀  (left-tailed)

Step 2: Choose α (e.g., 0.05 = 5%)
            (or equivalently CL = 1 − α = 95%)

Step 3: Look up Z* — the CRITICAL boundary
            Two-tailed α=0.05  →  Z* = ±1.96
            Right-tailed α=0.05 →  Z* = +1.645
            Left-tailed α=0.05  →  Z* = −1.645

Step 4: Compute the test statistic Z from the data
            Z = (x̄ − μ₀) / SE
            where SE = σ/√n

Step 5: Compare |Z| to |Z*|
            |Z| > |Z*|  →  REJECT H₀  (in the tail / extreme)
            |Z| ≤ |Z*|  →  FAIL to reject H₀
```

### Visual — Two-Tailed Decision Rule

```
         REJECT          FAIL TO REJECT         REJECT
         ──────       ────────────────────       ──────
                              μ₀
                               ↑
                     test stat Z computed here
                     
         |─────────────|─────────────|
        −Z*           0             +Z*
        (e.g., −1.96)              (e.g., +1.96)
```

```
If Z falls in the REJECT region  →  evidence against H₀
If Z falls in the middle         →  insufficient evidence
```

### One-Tailed Example (Right Tail)

```
H₁: μ > μ₀   →  reject only if Z is LARGE (positive)

       FAIL TO REJECT                  REJECT
       ──────────────────────       ──────────
                                Z* = +1.645
                                
       Z > Z*  →  reject H₀
       Z ≤ Z*  →  fail to reject
```

### Quick Example

```
H₀: μ = 50    H₁: μ ≠ 50    α = 0.05  (two-tailed)
σ = 10, n = 100, x̄ = 52

SE = 1
Z = (52 − 50) / 1 = 2.0
Z* = ±1.96

|Z| = 2.0 > 1.96  →  REJECT H₀
   → evidence that μ ≠ 50
```

---

## The Two Paths Are Equivalent

```
Confidence interval:    CI = x̄ ± Z* · SE   →   does it contain μ₀?
Hypothesis test:         Z = (x̄ − μ₀)/SE    →   is |Z| > Z*?

If CI excludes μ₀  ⇔  |Z| > Z*  ⇔  reject H₀
If CI includes μ₀  ⇔  |Z| ≤ Z*  ⇔  fail to reject H₀
```

### Same Conclusion, Two Views

```
Example:
   μ₀ = 50, x̄ = 52, ME = 1.96 → CI = [50.04, 53.96]
   
   CI [50.04, 53.96] does NOT include 50  →  rejects H₀ ✓
   Z = 2.0, |Z| > 1.96  →  rejects H₀ ✓
   
   Same evidence, expressed two ways.
```

---

## The Decision Rule Outline (Hypothesis Test)

```
GIVEN: x̄ (sample mean), σ or s, n, μ₀ (hypothesised mean), CL or α

1. SE = σ/√n           ← from CLT
2. Z = (x̄ − μ₀) / SE   ← test statistic

3. Look up Z* in the Z-table for the chosen α:
       Two-tailed:    Z* at α/2  (e.g., α=0.05 → Z* = 1.96)
       One-tailed:    Z* at α    (e.g., α=0.05 → Z* = 1.645)

4. Decision:
       Two-tailed:    |Z| > |Z*|  →  REJECT H₀
       Right-tailed:  Z > Z*       →  REJECT H₀
       Left-tailed:   Z < −Z*      →  REJECT H₀

   OR equivalently:
       Compute CI = x̄ ± Z* · SE
       If μ₀ NOT in CI → REJECT H₀
```

---

## CL ↔ α ↔ Z* Quick Reference

| Confidence Level | α (significance) | Two-tailed Z* | One-tailed Z* |
|------------------|------------------|---------------|---------------|
| 90% | 0.10 | ±1.645 | ±1.282 |
| 95% | 0.05 | ±1.960 | ±1.645 |
| 98% | 0.02 | ±2.326 | ±2.054 |
| 99% | 0.01 | ±2.576 | ±2.326 |
| 99.9% | 0.001 | ±3.291 | ±3.090 |

```
CL = 1 − α
   95% CL ↔ α = 0.05
   99% CL ↔ α = 0.01
```

---

## p-Value Alternative (Same Idea, Different Form)

Instead of comparing Z to Z*, you can compare **p-value** to α:

```
p-value = P(observing Z this extreme or more | H₀ true)

If p-value < α  →  REJECT H₀     (equivalent to |Z| > |Z*|)
If p-value ≥ α  →  fail to reject (equivalent to |Z| ≤ |Z*|)
```

### Three Equivalent Decision Rules

```
1. Compare Z to Z*           (classical "critical value" approach)
2. Check if CI contains μ₀    (confidence-interval approach)
3. Compare p-value to α        (most common in modern software)
```

Modern tools (scipy, R, statsmodels) output p-value directly — no Z-table needed.

---

## When to Use t Instead of Z

```
σ KNOWN  →  Z-test
   SE = σ/√n
   look up Z*

σ UNKNOWN  →  t-test (use sample s)
   SE = s/√n
   look up t* with df = n − 1
   
For large n (≥ 30): t ≈ Z, so difference is negligible
For small n:        Z ≠ t, must use t-distribution
```

The workflow is identical — just swap Z* ↔ t* and σ ↔ s.

---

## Complete End-to-End Example

```
Claim:    Average exam score is μ₀ = 70
Sample:   n = 50, x̄ = 73, σ = 12
Test:     Is the true mean different from 70?
Level:    α = 0.05  (two-tailed)

Step 1:  SE = 12 / √50 = 1.70

Step 2:  Z = (73 − 70) / 1.70 = 1.77

Step 3:  Z* = ±1.96  (two-tailed, α = 0.05)

Step 4:  |Z| = 1.77 < 1.96
         → FAIL to reject H₀
         → insufficient evidence that true mean differs from 70

Equivalently — CI version:
   ME = 1.96 × 1.70 = 3.33
   CI = 73 ± 3.33 = [69.67, 76.33]
   μ₀ = 70 IS in CI → fail to reject ✓

Equivalently — p-value version:
   p = 2 × P(Z > 1.77) ≈ 2 × 0.0384 = 0.077
   p = 0.077 > 0.05 → fail to reject ✓
```

All three methods give the same conclusion.

---

## Connecting Back to CLT

```
WHY does this Z-based inference work?

CLT says:
   For large n, x̄ ~ Normal(μ, σ²/n)
   regardless of the underlying data distribution!

Therefore:
   (x̄ − μ) / (σ/√n) ~ Standard Normal Z

That's why we can use the Z-table for ANY data:
   ✓ Normal data
   ✓ Skewed data (large n)
   ✓ Discrete data (large n)
   
   → as long as the SAMPLE MEAN can be treated as normal.
```

This is the magic that makes inference work in the real world.

---

## Visual Summary of the Flow

```
                       CLT
                  ┌─────────────┐
                  │ x̄ ~ Normal  │
                  │ SE = σ/√n   │
                  └─────┬───────┘
                        │
            ┌───────────┴────────────┐
            ▼                          ▼
       CL or α                  Sample x̄
        │                            │
        ▼                            ▼
   Look up Z*           Compute Z = (x̄ − μ₀)/SE
        │                            │
        ├──── ME = Z* · SE  ────┐    │
        │                       │    │
        ▼                       ▼    │
   x̄ ± ME = CI           |Z| ≷ |Z*|? │
        │                            │
        ▼                            ▼
   Does CI contain μ₀?    Reject H₀ or not
                                     │
                                     ▼
                              SAME CONCLUSION
```

---

## Summary

```
CLT gives the foundation:
   x̄ ~ Normal(μ, σ²/n)
   SE = σ/√n

From there:
   CL → Z*           (look up the critical value)
   SE × Z* → ME      (margin of error)
   x̄ ± ME → CI       (confidence interval)
   
   Z = (x̄ − μ₀)/SE   (compute test statistic)
   
   |Z| > |Z*| → reject H₀  (in the rejection region)
   μ₀ not in CI → reject H₀
   p < α → reject H₀

THREE equivalent decision rules:
   1. Compare Z to Z*
   2. Check if CI excludes μ₀
   3. Compare p-value to α

The CLT lets us treat the SAMPLE MEAN AS NORMAL — that's why all
of this Z-table-based inference works for any underlying distribution
when n is large enough.
```

> The flow: **CLT gives SE → CL gives Z\* → ME = Z\* · SE → CI**. Hypothesis testing uses the SAME pieces in reverse: compute Z from your data, compare to Z* from the table, decide. The two paths are mirror images — both arrive at the same conclusion.
