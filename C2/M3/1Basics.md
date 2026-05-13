# Inferential Statistics — Central Limit Theorem

## Motivating Example — Facebook Feature Test

Facebook wants to add a fact-checking warning below posts to counter fake news. Before rolling it out to **1.86 billion users**, they run a pilot on **10,000 users** and ask: do you prefer the new timeline (Feature B) or the old one (Feature A)?

Result: **50.5% prefer Feature B.**

| | Detail |
|---|---|
| Population | 1.86 billion Facebook users |
| Sample | 10,000 pilot users |
| Sample statistic | 50.5% prefer Feature B |
| Goal | Infer whether the majority of the full population prefers B |

**Why sample instead of the full population?**
- Saves time and money
- Avoids risk of rolling out an untested feature to everyone

**The problem:** Just because 50.5% of 10,000 users preferred B, can you confidently say 50.5% of 1.86 billion users will too?

> Not yet — 50.5% is very close to 50%. This could easily be due to chance in the sample. You need **sampling distributions, CLT, and confidence intervals** to answer this properly.

This is the core question inferential statistics answers: *how much can you trust what a sample tells you about a population?*

### The Decision Rule — Using CI to Conclude Majority Preference

The point estimate (50.5%) alone is not enough. What matters is where the **confidence interval sits relative to 50%**:

| CI | Conclusion |
|---|---|
| Lower bound > 50% | Confidently majority prefer B |
| CI straddles 50% | Too close to call — could go either way |
| Upper bound < 50% | Confidently majority prefer A |

The **lower bound is your worst-case estimate**. If even the worst case is above 50%, you're safe to conclude majority preference.

**Example:**
- 50.5%, CI = (49.5%, 51.5%) → straddles 50% → cannot conclude B is preferred, could be noise
- 50.5%, CI = (51.2%, 52.8%) → entirely above 50% → confident majority prefers B

This is identical to how exit polls work in elections. When news channels say "too close to call", it means the CI straddles 50% — the sample isn't large enough to be certain which candidate is actually ahead. A larger sample shrinks the CI, which is why pollsters push for bigger samples when the race is tight.

### Worked Example — Facebook 90% CI

**Given:**
- x̄ = 0.505 (50.5% prefer Feature B)
- n = 10,000
- s = 0.2 (20%) — sample SD, used as approximation for σ since population SD is unknown
- Confidence level = 90% → Z\* = 1.645

**Step 1 — SE:**

$$SE = \frac{s}{\sqrt{n}} = \frac{0.2}{\sqrt{10000}} = \frac{0.2}{100} = 0.002$$

**Step 2 — Margin of Error:**

$$ME = Z^* \times SE = 1.645 \times 0.002 = 0.00329 \approx 0.33\%$$

**Step 3 — CI:**

$$CI = 50.5\% \pm 0.33\% = (50.17\%,\ 50.83\%)$$

**Conclusion:** Lower bound = 50.17% > 50% → Feature B is preferred by the majority with 90% confidence.

**Why margin of error matters:**

| ME | CI | Conclusion |
|---|---|---|
| 1% | (49.5%, 51.5%) | Straddles 50% → cannot conclude B preferred |
| 0.3% | (50.2%, 50.8%) | Entirely above 50% → B is preferred |
| **0.33%** | **(50.17%, 50.83%)** | **Entirely above 50% → B is preferred ✓** |

---

## What is Inferential Statistics?

**Descriptive statistics** summarises data you have.  
**Inferential statistics** uses a *sample* to draw conclusions about a *population*.

| Term | Definition |
|------|------------|
| **Population** | The entire group you care about (often too large to measure fully) |
| **Sample** | A subset of the population that you actually observe |

**Example:**
- Population: all voters in a country
- Sample: 1,000 randomly surveyed voters
- Inference: estimate the election outcome from that sample

> Core challenge: samples are never perfect representations of the population. Every sample-based estimate carries some error — the question is: how much?

---

## Populations and Samples

### Parameters vs Statistics

| | **Parameter** | **Statistic** |
|---|---|---|
| Describes | Population (fixed, usually unknown) | Sample (varies between samples) |
| Mean | μ (mu) | x̄ (x-bar) |
| Std Dev | σ (sigma) | s |
| Proportion | p | p̂ (p-hat) |

> Key idea: we use **statistics** (sample values) to **estimate** parameters (population values).

---

## Why Samples Vary — Sampling Error

Draw two different samples from the same population → you'll get two different x̄ values.  
This variability is called **sampling error**. It is not a mistake — it's inherent to sampling.

**Example** — heights of all adults in a city, μ = 170 cm:
- Sample 1 (n=50): x̄ = 168.5 cm
- Sample 2 (n=50): x̄ = 171.2 cm
- Sample 3 (n=50): x̄ = 169.8 cm

If you took **all possible samples** of size n and recorded their means, you would get a **distribution of sample means** — called the **sampling distribution**.

---

## Sampling Distribution of the Sample Mean

### Definition

The sampling distribution of x̄ is the probability distribution of all possible sample means from samples of the same size drawn from the same population.

**How to think about it:**
1. Take a sample of size n → compute x̄₁
2. Take another sample of size n → compute x̄₂
3. Repeat thousands of times → plot all x̄ values
4. The resulting histogram **is** the sampling distribution

This is a theoretical construct — in practice you only take **one** sample. But understanding what would happen over many samples tells you how reliable your one sample mean is.

### Properties of the Sampling Distribution

| Property | Value | Meaning |
|----------|-------|---------|
| **Centre** | E(x̄) = μ | Mean of all sample means equals the population mean |
| **Spread** | SE = σ/√n | Standard deviation of the sampling distribution (Standard Error) |
| **Shape** | Normal (via CLT) | Approaches normal as n increases, regardless of population shape |

> x̄ is an **unbiased estimator** of μ — on average it hits the target.

---

## Standard Error (SE)

SE is the standard deviation of the sampling distribution — it measures how much sample means typically vary around μ.

$$SE = \frac{\sigma}{\sqrt{n}}$$

### Effect of Sample Size on SE

| n | SE (if σ=30) | Precision |
|---|---|---|
| 10 | 9.49 | Low — unreliable estimates |
| 100 | 3.00 | Moderate |
| 1000 | 0.95 | High — reliable estimates |

As n → ∞, SE → 0: with an infinite sample you'd know μ exactly.

**Visualising the effect of n** (same population, σ=30):

```
Small n (n=10, SE≈9.5)          Large n (n=100, SE=3)

     │  ╭──────╮                      │     ╭──╮
     │ ╭╯      ╰╮                     │    ╭╯  ╰╮
     │╭╯         ╰╮                   │   ╭╯    ╰╮
     ╰╯           ╰╯                  │ ╭─╯      ╰─╮
──────────────────────── x̄      ────────────────────── x̄
            μ                                 μ

Wider = less precise                 Narrower = more precise
```

### Spread vs Standard Error — Not the Same Thing

"Spread" is informal. There are **two different spreads** in this topic:

| What it measures | Symbol | Formula | Name |
|---|---|---|---|
| Spread of **individual values** in the population | σ | — (it's a parameter) | Population SD |
| Spread of **individual values** in a sample | s | √[Σ(xᵢ − x̄)² / (n−1)] | Sample SD |
| Spread of **sample means** across repeated samples | SE | σ/√n or s/√n | Standard Error |

σ and SE are **not** the same — they measure spread of completely different things. σ measures how spread out **individuals** are (s estimates this when σ is unknown). SE measures how spread out **sample averages** are.

### σ/√n vs s/√n — Which SE Do You Use?

| SE formula | When to use |
|---|---|
| **σ/√n** | σ is *known* (rare — textbook problems, historical records) |
| **s/√n** | σ is *unknown* — estimated from the sample (almost always in practice) |

When you use s/√n instead of σ/√n, the Z-distribution is no longer exactly right for small samples. That's why for small n with unknown σ you switch to the **t-distribution** (fatter tails to account for the extra uncertainty from estimating σ). For large n (≥ 30+), s ≈ σ and the Z approximation is fine.

### The n−1 Thing — Bessel's Correction

When computing standard deviation **from a sample**, you divide by n−1, not n:

$$s = \sqrt{\frac{\sum(x_i - \bar{x})^2}{n-1}}$$

**Why n−1?** Because you already used the data to compute x̄. Once you know x̄ and n−1 of the deviations, the last deviation is forced — it has no freedom. You only have n−1 **independent** pieces of information. Using n−1 makes s² an unbiased estimator of σ². Using n would systematically underestimate it, especially for small samples.

> As n gets large, n vs n−1 barely matters — the correction vanishes.

### The Full Picture

```
Individual values                  Sample means
────────────────────────────────   ────────────────────────────────────────
σ = population SD   (unknown)      σ/√n = true SE       (theoretical)
s = sample SD       (computed,     s/√n = estimated SE  (used in practice,
    uses n−1)                             since σ is usually unknown)
```

---

## The Central Limit Theorem (CLT)

### Statement

> Regardless of the shape of the population distribution, the sampling distribution of the sample mean x̄ **approaches a normal distribution** as the sample size n increases.

$$\bar{x} \sim N\left(\mu,\ \frac{\sigma^2}{n}\right) \quad \text{for sufficiently large } n$$

Standardised form:

$$Z = \frac{\bar{x} - \mu}{\sigma/\sqrt{n}} \sim N(0, 1)$$

**Rule of thumb:** n ≥ 30 is usually sufficient. For very skewed populations, n ≥ 50+.

### Why It Is Powerful

The CLT works **regardless** of the original population distribution — skewed, uniform, bimodal, exponential. As long as n is large enough, sample means will form a normal distribution.

This is why normal-distribution-based inference (confidence intervals, hypothesis tests) works even on non-normal data.

### CLT in Action — Visual

Population: Uniform distribution (flat, not bell-shaped)

```
Population (n=1)        Sample Means (n=5)      Sample Means (n=30)
┌──────────────┐
│              │             ╭───╮                    ╭──╮
│              │           ╭─╯   ╰─╮                ╭╯  ╰╮
│              │         ╭─╯        ╰─╮            ╭─╯    ╰─╮
│              │       ──╯             ╰──        ──╯        ╰──
└──────────────┘
Flat/uniform           Getting bell-shaped         Close to Normal
```

### Conditions for CLT

| Condition | Detail |
|-----------|--------|
| Random sampling | Observations must be drawn independently |
| Finite population variance | σ² must be finite (always true in practice) |
| Sample size | n ≥ 30 (rule of thumb); n ≥ 50+ for heavily skewed data |

> **Important:** CLT applies to the **mean**. Individual values do NOT become normally distributed — only the means do.

---

## Applying the CLT — Z-score for Sample Means

Once CLT applies, treat x̄ as normally distributed and use Z-scores.

$$Z = \frac{\bar{x} - \mu}{SE} = \frac{\bar{x} - \mu}{\sigma/\sqrt{n}}$$

### Single Observation vs Sample Mean

The logic is identical in both cases — "how many standard deviations is this value away from the mean?" The only difference is *which* standard deviation: when your "value" is a sample mean x̄, the relevant spread is SE, not σ.

| | Formula | Denominator |
|---|---|---|
| Single observation | Z = (X − μ) / σ | σ — SD of individuals |
| Sample mean | Z = (x̄ − μ) / (σ/√n) | σ/√n — SE, SD of sample means |

---

## Worked Example 1 — Production Line

**Setup:** Factory fills bottles. μ = 500 ml, σ = 20 ml. Sample of n = 64 bottles.

SE = 20/√64 = 20/8 = **2.5 ml**  
Sampling distribution: x̄ ~ N(500, 2.5²)

**Q1. P(x̄ > 503)?**

| Step | Calculation |
|------|-------------|
| Standardise | Z = (503 − 500) / 2.5 = **1.2** |
| Z-table | F(1.2) = 0.8849 |
| Answer | P(x̄ > 503) = 1 − 0.8849 = **0.1151 ≈ 11.5%** |

**Q2. P(497 < x̄ < 503)?**

- Z₁ = (497 − 500) / 2.5 = −1.2 → F(−1.2) = 0.1151
- Z₂ = (503 − 500) / 2.5 = +1.2 → F(+1.2) = 0.8849
- P(497 < x̄ < 503) = 0.8849 − 0.1151 = **0.7698 ≈ 77%**

---

## Worked Example 2 — Call Centre

**Setup:** μ = 8 min, σ = 4 min (right-skewed distribution). Sample of n = 100 calls.

SE = 4/√100 = **0.4 min**  
CLT applies (n=100 ≫ 30) → x̄ ~ N(8, 0.4²)

**Q. P(7.5 < x̄ < 8.5)?**

- Z₁ = (7.5 − 8) / 0.4 = −1.25 → F(−1.25) = 0.1056
- Z₂ = (8.5 − 8) / 0.4 = +1.25 → F(+1.25) = 0.8944
- P(7.5 < x̄ < 8.5) = 0.8944 − 0.1056 = **0.7888 ≈ 79%**

> Individual calls vary widely (σ=4 min), but the mean of 100 calls is tightly clustered within ±0.4 min of the true mean. That is SE at work.

---

## Confidence Intervals

### Motivation

We take one sample, get x̄. True μ is unknown. Rather than a **point estimate** (μ = x̄), we build an **interval estimate** that captures μ with known probability.

> "I am 95% confident that the true population mean lies between a and b."

### Formula

$$CI = \bar{x} \pm Z^* \times \frac{\sigma}{\sqrt{n}}$$

**Critical values Z\*:**

| Confidence Level | Z\* |
|-----------------|-----|
| 90% | 1.645 |
| 95% | 1.960 |
| 99% | 2.576 |

**Margin of Error (ME)** = Z\* × (σ/√n)  
**CI** = (x̄ − ME, x̄ + ME)

### Correct Interpretation of a 95% CI

> "If we repeated this sampling process 100 times and built a CI each time, approximately **95 of those intervals** would contain the true μ."

**Wrong interpretation:** "There is a 95% chance μ is in this interval."  
μ is fixed — it either is or isn't in the interval. The 95% refers to the **procedure**, not to any single interval.

```
──────────── true μ ────────────
     [────●────]              ← contains μ ✓
            [────●────]       ← contains μ ✓
          [────●────]         ← contains μ ✓
                       [──●──]← misses μ ✗  (about 1 in 20)
```

### Worked Example 3 — Salary CI

**Setup:** n=100 employees, x̄ = ₹45,000, σ = ₹8,000. Construct 95% CI.

| Step | Calculation |
|------|-------------|
| SE | 8000/√100 = **800** |
| Z\* | **1.96** (95% CI) |
| ME | 1.96 × 800 = **₹1,568** |
| CI | 45,000 ± 1,568 = **(₹43,432, ₹46,568)** |

We are 95% confident the true average salary lies between ₹43,432 and ₹46,568.

### Effect of n and Confidence Level on CI Width

CI Width = 2 × Z\* × σ/√n

| Scenario (σ=20) | Width |
|-----------------|-------|
| n=25, 95% CI | 2 × 1.96 × 20/5 = **15.68** |
| n=100, 95% CI | 2 × 1.96 × 20/10 = **7.84** ← 4× sample → ½ width |
| n=100, 99% CI | 2 × 2.576 × 20/10 = **10.30** ← higher confidence = wider |

> To **halve** the margin of error, you must **quadruple** the sample size.  
> (SE = σ/√n — halving SE requires √n to double → n × 4)

---

## Common Misconceptions

| ✗ Wrong | ✓ Correct |
|---------|-----------|
| "CLT says data is normally distributed" | CLT says **sample means** are approximately normal. Individual data keeps the original shape. |
| "Always need n ≥ 30" | n=30 is a rule of thumb. Nearly normal populations need less; heavily skewed need more. |
| "SE is the sample's standard deviation" | SE = σ/√n is the SD of the **sampling distribution**. Sample SD (s) measures spread of individuals. |
| "95% CI means 95% chance μ is inside" | μ is fixed. 95% refers to the long-run success rate of the **procedure** over repeated sampling. |

---

## Summary — Key Formulas

| Formula | Equation |
|---------|----------|
| Standard Error | SE = σ / √n |
| Z-score for sample mean | Z = (x̄ − μ) / (σ/√n) |
| CLT result | x̄ ~ N(μ, σ²/n) for n ≥ 30 |
| Confidence Interval | CI = x̄ ± Z\* × (σ/√n) |
| Critical values | Z\* = 1.645 (90%), 1.960 (95%), 2.576 (99%) |

---

## Connections to Other Topics

| Topic | Connection |
|-------|------------|
| **Normal Distribution** | CLT produces a normal sampling distribution — all Z-table tools apply directly to sample means |
| **Z-score** | Same formula, but σ is replaced by SE = σ/√n; Z now measures how far a sample mean is from μ |
| **Law of Large Numbers** | Guarantees x̄ → μ as n → ∞; CLT describes the **shape** of that convergence |
| **Hypothesis Testing** (next) | Z = (x̄ − μ₀)/(σ/√n) is built directly on CLT — tests if observed x̄ is "surprising" |
| **A/B Testing (ML)** | CLT justifies comparing sample means between two groups |
| **Bootstrap Resampling** | Mimics CLT to estimate sampling distributions without knowing population distribution |
