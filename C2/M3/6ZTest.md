# Z-Test

Used to test hypotheses about a population mean when the **population standard deviation (σ) is known**.

```
Z = (x̄ − μ₀) / (σ / √n)

x̄  = sample mean
μ₀ = hypothesised population mean (under H₀)
σ  = POPULATION standard deviation (KNOWN)
n  = sample size
```

The resulting Z-statistic is compared to a critical value from the standard normal distribution.

---

## The Defining Condition — Known σ

This is the most important rule:

```
σ KNOWN     →  use Z-test
σ UNKNOWN   →  use t-test (uses sample std s)
```

In real life σ is rarely known — so t-tests are far more common in practice. Z-tests appear in:

```
Textbooks
Quality control (long-established σ from production history)
Standardised testing (known population variance)
```

---

## When Z-Test Is Valid

Three scenarios where Z-test holds:

| Scenario | Condition | Why it works |
|----------|-----------|--------------|
| Small n, normal population | Population approximately normal | x̄ is exactly normal — no CLT needed |
| Large n (≥ 30), any population | n ≥ 30 | CLT — x̄ is approximately normal |
| Small n, non-normal population | Don't use Z-test | Neither condition met |

---

## What the n ≥ 30 Rule Really Means

A common misconception: **"Z-test requires n ≥ 30."**

The correct version:

```
Z-test doesn't strictly require n ≥ 30.
What requires n ≥ 30 is the CLT — for non-normal populations.

If the population is ALREADY normal:
   Z-test works for ANY sample size (even n = 5)

If the population is NON-NORMAL:
   Need n ≥ 30 so that CLT makes x̄ approximately normal
```

So `n ≥ 30` is about **when CLT bails out a non-normal population**, not about Z-test specifically.

---

## Worked Example

You manage a factory making bolts. Historical data says the mean length is 5.0 cm with σ = 0.2 cm. A new machine is tested with a sample of 25 bolts. Mean length = 5.05 cm.

**Is the new machine producing different-length bolts (α = 0.05)?**

```
H₀: μ = 5.0  (no change)
H₁: μ ≠ 5.0  (two-tailed)

n = 25, x̄ = 5.05, σ = 0.2 (known)

Z = (5.05 − 5.0) / (0.2 / √25)
  = 0.05 / 0.04
  = 1.25

Critical Z at α=0.05 (two-tailed) = ±1.96

|Z| = 1.25 < 1.96 → fail to reject H₀
```

Conclusion: insufficient evidence that the new machine is different.

---

## Quiz — Multi-Select

**Q: Which statements about Z-test are correct?**

```
A) Used when population variance is known
B) Requires large sample size (n ≥ 30)
C) Assumes population is approximately normal for small samples
D) Can be applied when population is not normal if n is large (CLT)
```

**Answer: A, C, D**

### Statement A — Used when population variance is known  ✓

Correct. This is the defining condition.

```
Z formula uses σ (population std):
   Z = (x̄ − μ) / (σ / √n)

If σ unknown → must use t-test (uses sample s).
```

### Statement B — Requires n ≥ 30  ✗

**Common trap.** Z-test doesn't strictly require this.

```
Population normal + σ known → Z-test works for ANY n
Population non-normal + σ known → need n ≥ 30 for CLT
```

The n ≥ 30 rule is **about CLT**, not Z-test itself.

### Statement C — Small sample → assumes population is normal  ✓

Correct. With small n, you can't rely on CLT — so the data must come from something approximately normal.

```
Small n + non-normal population → Z-test NOT reliable
Small n + normal population     → Z-test valid
```

### Statement D — Large n → Z-test works on non-normal data via CLT  ✓

Correct. CLT says:

```
For sufficiently large n (≥ 30 typically),
the sampling distribution of x̄ is approximately normal
regardless of the population's underlying distribution.
```

So Z-test is still valid because the **statistic** is normal, even if the **data** isn't.

---

## Z-test vs t-test — Quick Compare

| | Z-test | t-test |
|-|--------|--------|
| Population σ | KNOWN | UNKNOWN (use sample s) |
| Distribution | Z (standard normal) | t (depends on df = n−1) |
| Small n + normal population | ✓ | ✓ |
| Small n + non-normal | ✗ | ✗ |
| Large n | ✓ via CLT | ✓ via CLT |
| Most common in practice | Rare | Very common |

For small samples, t-distribution has **fatter tails** — slightly more cautious than Z to account for the extra uncertainty from estimating σ from data.

---

## Common Variants of Z-Test

```
1. One-sample Z-test
   Test if a sample mean differs from a known population mean.
   
2. Two-sample Z-test
   Test if two sample means differ (when both σ's are known).
   
3. Z-test for proportions
   Test if a sample proportion p̂ differs from a hypothesised p₀.
   Z = (p̂ − p₀) / √(p₀(1−p₀)/n)
```

---

## Summary

```
Z-test conditions:
   ✓ Population variance σ is KNOWN
   ✓ Sample comes from a normal population
      OR sample size is large enough for CLT (typically n ≥ 30)

Z = (x̄ − μ₀) / (σ / √n)
Compare |Z| to critical Z (e.g., 1.96 for α=0.05 two-tailed)

Common quiz trap: "Z requires n ≥ 30" is partially true.
   → real rule: needs known σ, plus EITHER normal data OR large n.
```

> The defining feature of Z-test is **known σ**, not sample size. Sample size matters only when the population is non-normal — in which case CLT (n ≥ 30) makes Z still valid.
