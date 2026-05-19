# Binomial — Expected Value and Variance

The two most important descriptive statistics for a Binomial distribution.

```
For X ~ Binomial(n, p):
   E(X)   =  n · p                    ← expected number of successes
   Var(X) =  n · p · (1 − p)           ← spread around the mean
   SD(X)  =  √(n · p · (1 − p))        ← spread in original units
```

These come from one underlying idea: a Binomial is just **n independent Bernoulli trials added together**.

---

## E(X) — The Shortcut: `np`

For Binomial(n, p):

```
E(X) = n · p
```

### Intuition

```
You flip a fair coin (p = 0.5) ten times.
Expected number of heads = 10 × 0.5 = 5
```

You don't need to compute the long sum `Σ x · P(X = x)` — just multiply n by p.

### Why it works

A Binomial(n, p) random variable is the **sum of n Bernoulli(p) random variables**:

```
X = Y₁ + Y₂ + ... + Yₙ      where each Yᵢ ~ Bernoulli(p)

E(Yᵢ) = p             (each Bernoulli has expected value p)

By linearity of expectation:
   E(X) = E(Y₁) + E(Y₂) + ... + E(Yₙ)
        = p + p + ... + p
        = n · p
```

**`E(X) = np` is the shortcut you should always use.** No need to expand the formula.

### Examples

```
20 students take a 70%-pass-rate exam:
   Expected passes = 20 × 0.7 = 14

100 customers visit, 5% buy:
   Expected buyers = 100 × 0.05 = 5

3 dice rolled — expected number of 6s:
   E(X) = 3 × (1/6) = 0.5
```

---

## Variance — The Spread

Three views of variance, all equivalent:

| Concept | Formula | Meaning |
|---|---|---|
| Variance | E[(X − μ)²] | spread around mean |
| Variance (discrete) | Σ(x − μ)² · P(X = x) | same idea, in sum form |
| Bernoulli variance | p(1 − p) | single trial uncertainty |
| Binomial variance | n · p · (1 − p) | sum of n trials |
| Std deviation | √Var(X) | spread in original units |

---

## Bernoulli Variance — The Building Block

```
For Y ~ Bernoulli(p):
   Var(Y) = p(1 − p)
```

### Derivation

```
Y takes values 0 (probability 1−p) or 1 (probability p)
E(Y) = p

Var(Y) = E[(Y − p)²]
       = (0 − p)² · (1−p) + (1 − p)² · p
       = p² · (1−p)    + (1 − p)² · p
       = p · (1 − p) · [p + (1 − p)]
       = p · (1 − p) · 1
       = p(1 − p)
```

### Maximum at p = 0.5

```
p(1 − p):
   p = 0.0  → 0.00  (no uncertainty — always 0)
   p = 0.1  → 0.09
   p = 0.3  → 0.21
   p = 0.5  → 0.25  ← MAXIMUM uncertainty
   p = 0.7  → 0.21
   p = 0.9  → 0.09
   p = 1.0  → 0.00  (no uncertainty — always 1)
```

**Uncertainty peaks when the coin is fair.** Extreme probabilities → less uncertainty.

---

## Binomial Variance — Sum of n Bernoullis

```
For X ~ Binomial(n, p):
   X = Y₁ + Y₂ + ... + Yₙ      independent Bernoullis

Var(X) = Var(Y₁) + Var(Y₂) + ... + Var(Yₙ)     (independence)
       = p(1−p) + p(1−p) + ... + p(1−p)
       = n · p · (1 − p)
```

Because the trials are **independent**, variances simply add.

---

## Standard Deviation

```
SD(X) = √Var(X) = √(n · p · (1 − p))
```

SD is in the **same units as X** — much easier to interpret than variance.

### Example

```
n = 100 coin flips, p = 0.5

E(X)   = 100 × 0.5         = 50      heads on average
Var(X) = 100 × 0.5 × 0.5   = 25
SD(X)  = √25                = 5      "spread" of ±5 heads

→ typically observe between 45-55 heads (±1 SD)
→ rarely observe below 35 or above 65 (±3 SD)
```

---

## Worked Example

A drug trial: 200 patients, treatment success rate is 60%.

```
n = 200,  p = 0.6

E(X)   = 200 × 0.6           = 120 successes expected
Var(X) = 200 × 0.6 × 0.4     = 48
SD(X)  = √48                  ≈ 6.93

68% range:  120 ± 7   →  ~113 to ~127 successes
95% range:  120 ± 14  →  ~106 to ~134 successes
```

If you actually saw only 90 successes, that would be about 4 SDs below expected — a very rare outcome under this model. Either luck or the success rate is lower than claimed.

---

## When These Formulas Apply

```
Binomial requires:
   ✓ Fixed number of trials n
   ✓ Each trial independent
   ✓ Each trial has same probability p of success
   ✓ Each trial is a binary outcome (success / failure)
```

If trials are dependent or p varies → not Binomial → formulas don't apply.

---

## Quick Reference

| Quantity | Formula | What it tells you |
|----------|---------|-------------------|
| **E(X)** | `n · p` | Long-run average number of successes |
| **Var(X)** | `n · p · (1 − p)` | Squared spread around the mean |
| **SD(X)** | `√(n · p · (1 − p))` | Typical deviation in success-count units |

---

## Comparing Binomial to its Pieces

| | Bernoulli (1 trial) | Binomial (n trials) |
|-|---------------------|--------------------|
| Mean | p | np |
| Variance | p(1−p) | np(1−p) |
| Std dev | √[p(1−p)] | √[np(1−p)] |
| Values | 0 or 1 | 0, 1, 2, ..., n |

Binomial = n × Bernoulli (since variance and mean both scale linearly with n under independence).

---

## In Code

```python
import numpy as np
from scipy.stats import binom

n, p = 200, 0.6

# Theoretical
print(f"E(X)  = {n * p}")              # 120.0
print(f"Var   = {n * p * (1 - p)}")    # 48.0
print(f"SD    = {np.sqrt(n * p * (1 - p)):.3f}")   # 6.928

# Via scipy
print(f"E(X)  = {binom.mean(n, p)}")
print(f"Var   = {binom.var(n, p)}")
print(f"SD    = {binom.std(n, p):.3f}")

# Verify by simulation
samples = binom.rvs(n, p, size=100_000)
print(f"\nSimulated mean: {samples.mean():.3f}")    # ≈ 120
print(f"Simulated var:  {samples.var():.3f}")       # ≈ 48
print(f"Simulated std:  {samples.std():.3f}")       # ≈ 6.928
```

---

## Summary

```
For X ~ Binomial(n, p):

   E(X)   = n · p                        ← the "np shortcut"
   Var(X) = n · p · (1 − p)
   SD(X)  = √[n · p · (1 − p)]

Why these work:
   Binomial = sum of n independent Bernoulli(p) trials
   Bernoulli mean       = p
   Bernoulli variance   = p(1 − p)
   For independent sums:
      means ADD       → E(X) = np
      variances ADD   → Var(X) = np(1 − p)

p(1 − p) is maximum at p = 0.5 — fair coin = most uncertain.
```

> The **np shortcut** for expected value works because each Bernoulli trial contributes p to the mean, and you have n of them. The **n·p·(1−p)** variance formula works because variances of independent variables sum. Two of the most useful formulas in probability — and both come from the same "sum of Bernoullis" interpretation.
