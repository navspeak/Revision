# Exit Poll — MCD Ward 75N (Ashok Vihar)

## Setup

A news agency surveys **n = 100** randomly selected voters.

| Party | Voters |
|---|---|
| Party A | 58 |
| Party B | 42 |

---

## Define the Random Variable

Let X be the indicator for voting Party A:

$$X = \begin{cases} 1 & \text{if voted for Party A} \\ 0 & \text{otherwise} \end{cases}$$

From the sample:

$$P(X = 1) = \hat{p} = \frac{58}{100} = 0.58$$
$$P(X = 0) = 1 - \hat{p} = \frac{42}{100} = 0.42$$

---

## Expected Value (Sample Mean)

$$E(X) = \bar{x} = \sum x \cdot P(X=x) = 1 \times 0.58 + 0 \times 0.42 = \mathbf{0.58}$$

Interpretation: on average, 58% of voters chose Party A.

---

## Variance and Standard Deviation

**Population variance for a Bernoulli variable:**

$$\sigma^2 = p(1-p) = 0.58 \times 0.42 = 0.2436$$

> **Where does p(1−p) come from?** From the EV formula (C1):
> $$Var(X) = E(X^2) - [E(X)]^2$$
> For a 0/1 variable: $E(X^2) = 1^2 \times p + 0^2 \times (1-p) = p$ and $E(X)^2 = p^2$
> $$\therefore Var(X) = p - p^2 = p(1-p)$$
> Here **p = P(X=1)** and **1−p = P(X=0)** — just the two probabilities of the Bernoulli variable.

**Symmetry — why Party B has the same SD as Party A:**

For Party B: p = 0.42, 1−p = 0.58 → p(1−p) = 0.42 × 0.58 = 0.2436

Same product — swapping p and 1−p gives the same result. Whenever two proportions are complements (sum to 1), their standard deviations are identical.

**Sample variance (Bessel's correction, divides by n−1):**

$$s^2 = \frac{\sum(x_i - \bar{x})^2}{n-1} = \frac{58 \times (1-0.58)^2 + 42 \times (0-0.58)^2}{99}$$

$$= \frac{58 \times 0.1764 + 42 \times 0.3364}{99} = \frac{10.23 + 14.13}{99} = \frac{24.36}{99} = \mathbf{0.2461}$$

$$s = \sqrt{0.2461} = \mathbf{0.496}$$

> Why n−1? Because σ is unknown — we are estimating it from the sample. See `1Basics.md`.

---

## Sampling Distribution (CLT)

Multiple samples of size 100 are taken and their means form the sampling distribution:

$$\mu_{\hat{p}} = 0.50 \quad \text{(given — mean of the sampling distribution)}$$
$$SE = 0.052 \quad \text{(given)}$$

**Population proportion:**

By CLT: E(x̄) = μ → the mean of the sampling distribution = the true population proportion.

$$\mu_{\hat{p}} = 0.50 \Rightarrow p = \mathbf{50\%}$$

> The single sample gave x̄ = 0.58, but averaged across many samples the true population proportion is 50% — a genuine 50-50 race. The 58% was sampling variation in one sample.

> **Key distinction:** x̄ = 0.58 is the **sample mean** (one sample). μ_x̄ = 0.50 is the **mean of the sampling distribution** (average over many samples) = the population mean.

**Standard Error (given vs calculated):**

$$SE_{\text{given}} = 0.052 \quad \text{vs} \quad SE_{\text{calculated}} = \frac{0.496}{\sqrt{100}} = 0.0496$$

Close but not identical — because SE_given is based on the true population SD, SE_calculated uses s from one sample.

---

## Confidence Interval

Can we say Party A will win (i.e. p > 50%)?

**95% CI for true population proportion p:**

$$CI = \hat{p} \pm Z^* \times SE = 0.58 \pm 1.96 \times 0.0496$$

$$= 0.58 \pm 0.097 = \mathbf{(0.483,\ 0.677)}$$

**Lower bound = 0.483 < 0.50** → CI straddles 50% → **cannot conclusively say Party A wins** at 95% confidence.

**90% CI:**

$$CI = 0.58 \pm 1.645 \times 0.0496 = 0.58 \pm 0.082 = \mathbf{(0.498,\ 0.662)}$$

Lower bound = 0.498 < 0.50 → still straddles 50% → still cannot conclude.

---

## 95% Confidence Intervals — BJP vs INC

SE = s/√n = 0.496/√100 = **0.0496**, Z\* = 1.96, ME = 1.96 × 0.0496 = **0.0972 ≈ 9.72%**

| Party | Mean | CI |
|---|---|---|
| BJP | 58% | (48.28%, 67.72%) |
| INC | 42% | (32.28%, 51.72%) |

**Decision:**

- BJP CI lower bound = **48.28% < 50%** → straddles 50% → cannot conclusively say BJP wins
- INC CI upper bound = **51.72% > 50%** → straddles 50% → cannot conclusively say INC wins
- The two CIs **overlap** → no clear winner can be declared

> Both CIs overlap around 50% — the sample of 100 voters is not large enough to confidently predict the winner. A larger sample would narrow both CIs and potentially separate them.

---

## Hypothesis Test

**Can we reject the claim that it's a 50-50 race?**

- H₀: p = 0.50 (tie)
- H₁: p > 0.50 (Party A leads)
- Right-tailed test, α = 5%

$$Z = \frac{\hat{p} - p_0}{SE} = \frac{0.58 - 0.50}{0.0496} = \frac{0.08}{0.0496} = \mathbf{1.61}$$

Z\* = 1.645 (right-tailed, α = 5%)

Z = 1.61 < Z\* = 1.645 → **Fail to reject H₀**

**Conclusion:** At 5% significance, the sample does not provide enough evidence to declare Party A the winner. The margin is too close relative to the sample size.

> To get a conclusive result, a **larger sample** is needed — increasing n shrinks SE and narrows the CI.
