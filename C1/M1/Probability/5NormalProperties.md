# Properties of the Normal Distribution

```
Normal distribution = symmetric, bell-shaped, fully described by μ and σ.
```

Below are the **defining properties** every "perfectly normal" distribution satisfies — including the shape statistics (skewness, kurtosis) and the empirical 68-95-99.7 rule.

---

## The Core Properties

### 1. Symmetric and Bell-Shaped

```
       ___
      /   \
     /     \
    /       \
 ____________________
       μ
```

The curve is **mirror-symmetric** around the mean μ. Left and right halves are identical reflections.

### 2. Mean = Median = Mode

```
For a normal distribution, all three measures of central tendency
coincide at the same point: μ.

   Mean (average)         =  μ
   Median (middle value)  =  μ
   Mode (most common)     =  μ
```

This is a hallmark of symmetric distributions. Skewed distributions have these at different points.

### 3. Skewness = 0

```
Skewness = E[((X − μ)/σ)³]

For a normal distribution: skewness = 0   (perfectly symmetric)
```

**Skewness** measures asymmetry:

```
SKEW = 0  (Symmetric — Normal)    SKEW > 0 (Right-skewed)        SKEW < 0 (Left-skewed)

      ___                              ___                              ___
     /   \                            /   \                            /   \
    /     \                          /     \____                    __/     \
   /       \                        /          \____             __/         \
  ─────────────                     ─────────────────              ─────────────
       μ                          μ ← median        →            ←        μ
   mean = median                    mean > median                 mean < median
```

Real-world examples:

```
Right-skewed (positive):
   Income, house prices, reaction times, earthquake sizes

Left-skewed (negative):
   Age at retirement, easy test scores, lifespan
```

### 4. Kurtosis = 3 (Excess Kurtosis = 0)

```
Kurtosis = E[((X − μ)/σ)⁴]

For a normal distribution: kurtosis = 3
   or equivalently: excess kurtosis = 3 − 3 = 0
```

**Kurtosis** measures tail heaviness:

```
MESOKURTIC                 LEPTOKURTIC                PLATYKURTIC
kurtosis = 3               kurtosis > 3                kurtosis < 3
(or excess = 0)            (heavy tails)               (light tails)

      ___                       ___                         _____
     /   \                     /   \                       /     \
    /     \                   /|   |\                     /       \
   /       \                 / |   | \                   /         \
  ─────────────              ────|   |────              ─────────────
                                                
   Normal                  More peak, FATTER tails    Flatter, THINNER tails
                          → more extreme values        → fewer outliers
```

Real-world examples:

```
Leptokurtic (heavy tails — more extremes than normal):
   Financial returns (crashes happen more than normal would predict)
   Earthquake magnitudes
   Internet traffic spikes

Platykurtic (light tails):
   Uniform distribution
   Bounded variables
```

### 5. The 68-95-99.7 Rule

```
About 68%   of values lie within   ±1σ of μ
About 95%   of values lie within   ±2σ of μ
About 99.7% of values lie within   ±3σ of μ
```

Direct consequence of the normal PDF — gives quick mental estimates of unusualness.

### 6. Total Area Under the Curve = 1

```
∫ f(x) dx = 1     over all x

The TOTAL probability is 1 (valid PDF).
```

### 7. Asymptotic to the X-Axis

```
The tails APPROACH the x-axis but NEVER touch it.

f(x) > 0 for all x in (−∞, +∞)
```

There's always some (tiny) probability of an extreme value — the curve never reaches exactly zero.

### 8. Fully Defined by Two Parameters

```
Normal(μ, σ²)
   μ → controls LOCATION (where the peak sits)
   σ → controls SPREAD (how wide the bell is)
```

Two numbers fully describe the entire distribution.

### 9. Inflection Points at μ ± σ

```
The curve changes from CONCAVE DOWN to CONCAVE UP
exactly at one standard deviation from the mean.

         ___ ← peak (concave down)
        /   \
       /     \
       |     | ← inflection points (μ ± σ)
       |     |
   ____|     |_____________
       
       μ−σ μ μ+σ
```

This makes σ visually identifiable.

### 10. Standardisable

```
Any Normal(μ, σ²) can be converted to STANDARD NORMAL N(0, 1):

   Z = (X − μ) / σ

Then use ONE table (the Z-table) for all normals.
```

### 11. Linear Combinations Stay Normal

```
If X ~ Normal(μ₁, σ₁²) and Y ~ Normal(μ₂, σ₂²), independent:

   aX + bY ~ Normal(aμ₁ + bμ₂,  a²σ₁² + b²σ₂²)
```

Adding, scaling, or combining independent normals → still normal. This is why **sample means of normal data are also normal**.

### 12. CLT — Sample Means Become Normal

```
Sample means of ANY distribution → approximately normal (large n).
   → this is why normal is everywhere in statistical inference.
```

---

## Quiz — Which Is True for a Perfectly Normal Distribution?

```
A) Mean, median, and mode are equal
B) Skewness = 0 and kurtosis = 3
C) 95% of data lies within ±2 standard deviations of the mean
D) All of the above
```

### Answer: **D — All of the Above** ✓

All three statements describe defining properties of the normal distribution.

```
Statement A: Mean = Median = Mode = μ    →  ✓ TRUE (symmetry)
Statement B: Skewness = 0, Kurtosis = 3   →  ✓ TRUE (defining shape moments)
Statement C: 95% within ±2σ                →  ✓ TRUE (empirical rule)

Each alone is correct → "all of the above" is the right answer.
```

### Why the Three Together Define "Normal"

```
A perfect normal distribution passes 3 quick tests:

   1. CENTRE check:    mean = median = mode
   2. SHAPE check:     skewness = 0, kurtosis = 3
   3. SPREAD check:    68-95-99.7 rule

Pass all 3 → normal.
Fail any 1 → NOT normal.
```

These are not independent — they all follow from the **same PDF**:

```
f(x) = (1 / σ√(2π)) · exp(−(x − μ)² / (2σ²))
```

If you know any one precisely, the others follow.

---

## Interpretation Rules for Sample Statistics

```
Skewness:
   |skew| < 0.5      →  approximately symmetric (≈ normal)
   0.5 < |skew| < 1   →  moderately skewed
   |skew| > 1         →  highly skewed

Kurtosis (excess):
   ≈ 0           →  normal-like tails
   > 0           →  heavier tails than normal (leptokurtic)
   < 0           →  lighter tails than normal (platykurtic)
```

Quick way to check normality from sample statistics:

```
Sample skew ≈ 0   AND   sample excess kurtosis ≈ 0
   → data looks approximately normal
```

---

## Pearson's Skewness Coefficient

Quick approximation using mean, median, and σ:

```
Pearson skewness = 3 × (mean − median) / σ

mean > median  →  positive skew (right-skewed)
mean < median  →  negative skew (left-skewed)
mean = median  →  symmetric (no skew)
```

Useful for back-of-envelope checks.

---

## Computing in Python

```python
import numpy as np
import pandas as pd
from scipy import stats

# Generate truly normal data
data = np.random.normal(loc=100, scale=15, size=1_000_000)

# Property 1: Central tendency
print(f"Mean:   {data.mean():.2f}")            # ≈ 100
print(f"Median: {np.median(data):.2f}")        # ≈ 100

# Property 2: Shape (skewness and kurtosis)
print(f"Skewness:          {stats.skew(data):.3f}")            # ≈ 0
print(f"Kurtosis (excess): {stats.kurtosis(data):.3f}")        # ≈ 0
print(f"Kurtosis (raw):    {stats.kurtosis(data, fisher=False):.3f}")  # ≈ 3

# Property 3: 95% within ±2σ
within_2sd = np.mean(np.abs(data - 100) < 2 * 15)
print(f"Within ±2σ: {within_2sd * 100:.2f}%")  # ≈ 95%

# Pandas alternatives
s = pd.Series(data)
print(s.skew())     # ≈ 0
print(s.kurt())     # ≈ 0 (excess, by pandas convention)
```

```
⚠ scipy.stats.kurtosis returns EXCESS kurtosis by default
   fisher=True (default) → excess (subtracts 3)
   fisher=False           → raw (3 for normal)

⚠ pandas .kurt() returns EXCESS kurtosis by default
```

---

## Tail Probabilities for Normal

```
Above +3σ: 0.135%
Above +2σ: 2.5%
Above +1σ: 16%
Between ±1σ: 68%
Below −1σ: 16%
Below −2σ: 2.5%
Below −3σ: 0.135%
```

For non-normal distributions (skewed or fat-tailed), these percentages will differ — the 68-95-99.7 rule only holds when the data is approximately normal.

---

## Properties Summary Table

| # | Property | Value for Normal |
|---|----------|------------------|
| 1 | Symmetric | Yes |
| 2 | Bell-shaped | Yes |
| 3 | Mean = Median = Mode | All = μ |
| 4 | Skewness | 0 |
| 5 | Kurtosis | 3 (excess = 0) |
| 6 | 68-95-99.7 rule | Applies exactly |
| 7 | Total area | 1 |
| 8 | Asymptotic tails | Yes |
| 9 | Parameters | μ, σ |
| 10 | Inflection points | μ ± σ |
| 11 | Standardisable | Z = (X − μ)/σ |
| 12 | Linear combinations | Stay normal |
| 13 | CLT applies | Yes (for sample means) |

---

## Summary

```
For a perfectly normal distribution:

   ✓ Mean = Median = Mode = μ              (symmetric centre)
   ✓ Skewness = 0                          (no asymmetry)
   ✓ Kurtosis = 3 (excess = 0)              (no heavy tails)
   ✓ 95% of data within ±2σ                 (68-95-99.7 rule)
   ✓ Fully defined by (μ, σ)
   ✓ Standardisable via Z = (X − μ)/σ
   ✓ Linear combinations stay normal
   ✓ Sample means → normal (CLT)

ANY of these can be used to TEST normality.
ALL of them follow from the same bell-curve formula.
```

> Mean and variance describe **where** and **how spread** the distribution is. **Skewness and kurtosis describe its shape**. For a perfect normal: **skewness = 0, kurtosis = 3, mean = median = mode**, and **95% sits within ±2σ**. All four are true simultaneously — none is "more correct" than the others.
