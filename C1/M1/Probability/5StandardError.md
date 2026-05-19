# σ vs s vs σ/√n — When to Use Each

```
σ      →  population standard deviation
s      →  sample standard deviation (estimate of σ)
σ/√n   →  standard error (SE) — spread of SAMPLE MEANS
```

When you use which depends on **what variable** you're z-scoring — an individual value or a sample mean.

---

## Two Different Things You Might Z-Score

### Z-Score for ONE Individual Observation

```
You want to know how unusual ONE person / value is.

   Z = (X − μ) / σ
       
       X = the individual value
       μ = population mean
       σ = population std dev
```

**Example:** is a single person's height of 190 cm unusual?

```
Population mean μ = 175,  population σ = 8

Z = (190 − 175) / 8 = 1.875
   → person is 1.875 SDs above the mean → roughly top 3%
```

### Z-Score for a SAMPLE MEAN

```
You took a sample of size n and computed the mean.
How unusual is this MEAN compared to the population?

   Z = (x̄ − μ) / (σ/√n)
       
       x̄ = sample mean
       μ = population mean
       σ/√n = standard error (NOT σ!)
```

**Example:** sampled 100 people, their average height was 180 cm. Is that unusual?

```
Population μ = 175, σ = 8, n = 100
SE = σ/√n = 8/10 = 0.8

Z = (180 − 175) / 0.8 = 6.25
   → 6.25 SDs above the expected mean → VERY unusual
```

Same numerical difference (5 cm above mean) is **far more surprising for a group average** than for an individual.

---

## Why `σ/√n` (Not Just σ)?

Sample means **vary less** than individual values.

```
Individual heights:    spread σ = 8 cm
Mean of 100 people:    they tend to AVERAGE close to 175

The bigger the sample, the closer the sample mean is to μ.
   → less spread
   → smaller SE
```

The exact formula comes from probability theory:

```
If X has variance σ²:
   Var(X̄) = σ²/n           (variance of mean of n independent samples)
   SD(X̄) = σ/√n            (standard error)
```

### Intuition — SE Shrinks with n

```
n = 1:      SE = σ          (sample of 1 = same spread as individuals)
n = 4:      SE = σ/2        (mean of 4 has half the spread)
n = 100:    SE = σ/10       (mean of 100 has 1/10 the spread)
n = 10000:  SE = σ/100      (mean of 10K has 1/100 the spread)
```

Doubling the sample size **doesn't** halve the SE — you need **4×** the data to halve it.

---

## Rule of Thumb

```
Looking at ONE value?  → divide by σ
Looking at an AVERAGE? → divide by σ/√n

ONE individual value (X):
   Z = (X − μ) / σ
   
SAMPLE MEAN of n values (x̄):
   Z = (x̄ − μ) / (σ/√n)
```

---

## What If You Don't Know σ?

In practice, `σ` (true population SD) is **rarely known**. You estimate it with `s` (sample SD).

```
σ known:      use Z-test    →   Z = (x̄ − μ) / (σ/√n)
σ unknown:    use t-test    →   t = (x̄ − μ) / (s/√n)
```

The substitution `σ → s` adds extra uncertainty → use **t-distribution** (slightly fatter tails) instead of normal.

| | Z-test | t-test |
|-|--------|--------|
| Population σ | KNOWN | UNKNOWN |
| Statistic | (x̄ − μ) / (σ/√n) | (x̄ − μ) / (s/√n) |
| Distribution | Standard normal | t with n−1 df |
| In practice | Rare (σ usually unknown) | Very common |

---

## Sample Standard Deviation Formula

```
σ (population):    σ = √[ Σ(xᵢ − μ)² / N ]
                                          ↑
                                       divide by N

s (sample):        s = √[ Σ(xᵢ − x̄)² / (n − 1) ]
                                          ↑↑↑↑↑
                                  divide by n − 1
```

```
Why n − 1?
   Sample mean x̄ is computed FROM the data itself.
   This uses 1 "degree of freedom" → only (n − 1) are free to vary.
   Dividing by (n − 1) gives an UNBIASED estimate of σ².
```

This is **Bessel's correction**. NumPy uses `ddof=1` for sample SD; default is `ddof=0` (population).

```python
import numpy as np

data = [10, 12, 14, 16, 18]

np.std(data)                  # 2.83 — population (ddof=0, DEFAULT)
np.std(data, ddof=1)          # 3.16 — sample (Bessel-corrected)

# pandas DEFAULTS to sample SD (ddof=1)
import pandas as pd
pd.Series(data).std()          # 3.16 — sample
```

⚠ NumPy's default is **population** (ddof=0). Pandas's default is **sample** (ddof=1). Always check which you want.

---

## Summary Table — Four Cases

| Situation | Formula | Notes |
|-----------|---------|-------|
| One value, σ known | `Z = (X − μ) / σ` | Most basic z-score |
| One value, σ unknown | rare in practice | Use t with n−1 df if needed |
| Sample mean, σ known | `Z = (x̄ − μ) / (σ/√n)` | Z-test |
| Sample mean, σ unknown | `t = (x̄ − μ) / (s/√n)` | t-test (very common) |

---

## Quick Visual

```
Distribution of INDIVIDUAL values:        Distribution of SAMPLE MEANS (n=100):
   spread = σ                              spread = σ/√n = σ/10
   
        ___                                       ___
       /   \                                     /  \
      /     \                                   /    \
     /       \                                  |    |
    /         \                                 |    |
   ──────────────                              ─────────                              
   broad bell                                  narrow bell
   centred at μ                                centred at μ (same)
```

Same centre. Different spread. That's why you divide by `σ/√n` when working with means.

---

## The CLT Connection

The reason `σ/√n` shows up is the **Central Limit Theorem**:

```
If X₁, X₂, ..., Xₙ are iid with mean μ and SD σ,
then for large n:

   x̄ ≈ Normal(μ, σ²/n)
   
   SD of x̄ = σ/√n  (the standard error)
```

This is why sample means are always **approximately normally distributed** for reasonably large n, regardless of the underlying distribution.

---

## Worked Examples

### Example 1 — Z-Score for an Individual

```
IQ ~ Normal(μ=100, σ=15)
A person scores 130.

Z = (130 − 100) / 15 = 2.0

→ 2 SDs above mean → roughly top 2.5%
```

### Example 2 — Z-Score for a Sample Mean

```
A class of 25 students has a mean IQ of 108.
Is this surprising (assuming μ=100, σ=15)?

SE = σ/√n = 15/√25 = 15/5 = 3

Z = (108 − 100) / 3 = 2.67

→ 2.67 SE above mean → about top 0.4%
→ very unusual class
```

Same mean difference (8 points), but very different conclusions:
- Individual scoring 108 → Z = 0.53 → totally normal
- Class of 25 averaging 108 → Z = 2.67 → very unusual

The **collective** is harder to be off-centre than the **individual**.

### Example 3 — When σ Is Unknown (t-test)

```
n = 25 students,  x̄ = 108,  s = 14   (estimated from sample)

t = (108 − 100) / (14/√25)
  = (108 − 100) / 2.8
  = 8 / 2.8 ≈ 2.86

Compare to t-distribution with df = 24
   → still very unusual, p-value tiny
```

The t-statistic looks similar to Z, but is judged against a slightly **wider** distribution (fatter tails) to account for uncertainty in σ.

---

## Common Confusion

```
✗ "I have n values, so I always divide by σ/√n"
   → wrong if you're z-scoring an INDIVIDUAL value
   → σ/√n is only for the SAMPLE MEAN

✓ Ask: am I asking about ONE value (Z = (X − μ)/σ)
       or a MEAN of n values (Z = (x̄ − μ)/(σ/√n))?
```

```
✗ "I'm using s, so I use Z"
   → wrong → using s means σ is unknown → use t
   
✓ σ known → Z-test
  σ unknown → t-test
```

---

## Summary

```
σ           → population SD          (rarely known in practice)
s           → sample SD              (used as estimate of σ)
σ/√n        → standard ERROR         (spread of SAMPLE MEANS)
s/√n        → estimated SE           (used when σ unknown)

ONE individual value:
   Z = (X − μ) / σ
   (divide by σ — the spread of individual values)

SAMPLE MEAN of n values:
   Z = (x̄ − μ) / (σ/√n)         if σ known
   t = (x̄ − μ) / (s/√n)         if σ unknown (almost always)

Rule:
   Single value  →  σ
   Average       →  σ/√n   (smaller spread, because averages cluster)

   Population SD known?  →  Z-test
   Estimated from data?  →  t-test
```

> `σ` is for individuals. `σ/√n` is for sample means. The denominator shrinks with n because **averages of many values are tighter than the individual values themselves** — that's the Central Limit Theorem in action.
