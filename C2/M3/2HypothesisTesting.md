# Hypothesis Testing

## Why Hypothesis Testing?

So far, inferential statistics helped us **estimate** population parameters from a sample (e.g. build a CI for μ when nothing is known).

Hypothesis testing is different — you start with a **specific claim** about the population (based on past data, industry standards, or business expectations) and use sample data to decide whether that claim holds up.

> Example: "Our average delivery time is 30 minutes." Is that still true given today's sample data?

---

## Core Idea

1. State a claim about the population
2. Collect sample data
3. Ask: is this sample result surprising if the claim were true?
4. If surprising enough → reject the claim. If not → cannot reject it.

---

## Types of Hypotheses

Every hypothesis test has exactly two competing hypotheses:

| | Symbol | Name | Meaning |
|---|---|---|---|
| **Null Hypothesis** | H₀ | Status quo | The claim assumed to be true until evidence says otherwise |
| **Alternative Hypothesis** | H₁ (or Hₐ) | Challenge | What you're trying to find evidence for |

**Key rules:**
- H₀ always contains an equality (=, ≥, ≤)
- H₁ always contains a strict inequality (≠, >, <)
- You never prove H₀ true — you either **reject H₀** or **fail to reject H₀**
- The burden of proof is on H₁ — you need evidence to overturn H₀

**Example — Facebook:**
- H₀: proportion preferring B ≤ 50% (no majority preference for B)
- H₁: proportion preferring B > 50% (majority prefers B)

---

## Types of Tests — One-tailed vs Two-tailed

Determined by the direction in H₁:

| H₁ | Test Type | Reject region |
|---|---|---|
| μ ≠ μ₀ | **Two-tailed** | Both tails |
| μ > μ₀ | **Right-tailed** (one-tailed) | Right tail only |
| μ < μ₀ | **Left-tailed** (one-tailed) | Left tail only |

```
Two-tailed                Right-tailed              Left-tailed
reject | accept | reject  accept  | reject       reject | accept
───────────────────────   ──────────────────       ──────────────────
  -Z*     0      +Z*            0    +Z*            -Z*     0

 Two-tailed (α = 0.05)

    Critical  |                    |  Critical
     Region   |    Acceptance      |   Region
              |      Region        |
  ────────────┼────────────────────┼────────────
            -1.96        0       +1.96
               ↑                    ↑
          critical value        critical value
              (Z*)                  (Z*)

  So:
  - Critical value (Z*) — the number (e.g. 1.96)
  - Critical region — the zone where Z* starts (e.g. everything beyond ±1.96)

  If your computed Z falls in the critical region → reject H₀.
```

**When to use which:**
- Two-tailed: "has anything changed?" — you care about deviation in either direction
- One-tailed: "has it increased/decreased?" — you have a specific direction in mind

---

## Decision Criteria

### Significance Level (α)

α is the probability of rejecting H₀ when it is actually true — the threshold for "surprising enough."

| α | Meaning |
|---|---|
| 0.05 | 5% chance of wrongly rejecting H₀ (most common) |
| 0.01 | 1% — stricter, used in medical/scientific research |
| 0.10 | 10% — more lenient |

> α is chosen **before** collecting data, not after.

### What α Actually Is — Visually

α is the **area in the tails** of the normal curve. It defines the rejection region — the zone where your sample result is so extreme that you say "this is too unlikely if H₀ were true."

For a two-tailed test at α = 0.05:

```
      α/2 = 2.5%              α/2 = 2.5%
  ┌──────────┐                ┌──────────┐
  │  Reject  │    Accept H₀   │  Reject  │
──┴──────────┴────────────────┴──────────┴──
            -Z*       0      +Z*
           -1.96             +1.96
```

The 95% in the middle is where "normal" sample results land if H₀ is true.
The 5% in the tails is where results land that are too extreme to be explained by chance.

**Z\* is the boundary.** It is found from the Z-table as the value that cuts off α/2 in each tail.

### Why Z and Z\* Are Different

| | Z (test statistic) | Z\* (critical value) |
|---|---|---|
| **What** | Computed from your sample | Fixed boundary from α |
| **How** | Z = (x̄ − μ₀) / SE | Looked up from Z-table using α |
| **Varies?** | Yes — changes with every sample | No — fixed once α is chosen |
| **Role** | Tells you where your result sits | Tells you where the rejection region starts |

You compare them: **if \|Z\| > Z\*, reject H₀.**

### Worked Example — What α Means in Practice

**Claim:** A machine fills bags with μ = 1000g. You suspect it has drifted.  
**Sample:** n = 36, x̄ = 1008g, σ = 24g. Test at α = 0.05 (two-tailed).

**Step 1 — Hypotheses:**
- H₀: μ = 1000 (machine is fine)
- H₁: μ ≠ 1000 (machine has drifted — either direction)

**Step 2 — Test statistic Z (from your data):**

$$Z = \frac{1008 - 1000}{24/\sqrt{36}} = \frac{8}{4} = 2.0$$

**Step 3 — Critical value Z\* (from α):**

α = 0.05, two-tailed → each tail = 2.5% → Z\* = 1.96

**Step 4 — Compare:**

Z = 2.0 > Z\* = 1.96 → falls in rejection region → **reject H₀**

```
      Reject          Accept H₀          Reject
─────────────┼─────────────────────────┼──────●──
           -1.96          0          +1.96   +2.0
                                              ↑
                                        your Z = 2.0
                                        (just past Z*)
```

**Conclusion:** At 5% significance, there is enough evidence that the machine has drifted from 1000g.

> **What α = 0.05 meant here:** You accepted a 5% risk of being wrong. Your Z of 2.0 fell in the outer 5% of the distribution — meaning this result would only happen 5% of the time by chance if H₀ were true. That's unlikely enough to reject H₀.

### Two Types of Errors

| | H₀ is actually True | H₀ is actually False |
|---|---|---|
| **Reject H₀** | Type I Error (α) | Correct ✓ |
| **Fail to reject H₀** | Correct ✓ | Type II Error (β) |

- **Type I Error** — false positive. Concluding there is an effect when there isn't.
- **Type II Error** — false negative. Missing a real effect.

Reducing α makes Type I errors less likely but Type II errors more likely — there is always a trade-off.

---

## The Critical Value Method

### Exam Flow

**Step 1 — From α get Z\*:**

```
α  →  Confidence Level (1 − α)  →  Z*
```

| α | Confidence | Two-tailed Z\* | One-tailed Z\* |
|---|---|---|---|
| 0.10 | 90% | 1.645 | 1.28 |
| 0.05 | 95% | 1.96 | 1.645 |
| 0.01 | 99% | 2.576 | 2.326 |

> Two-tailed splits α across both tails (α/2 each). One-tailed puts all α in one tail → smaller Z\*.

**UCV and LCV** — alternate names for Z\* depending on which tail:

| Term | Full Name | Used in |
|---|---|---|
| UCV | Upper Critical Value | Right-tailed test — boundary on the right |
| LCV | Lower Critical Value | Left-tailed test — boundary on the left |
| ±Z\* | Both | Two-tailed test — one boundary on each side |

UCV/LCV are just Z\* with a direction label. Same number, same Z-table lookup.

**Step 2 — From data compute Z:**

$$Z = \frac{\bar{x} - \mu_0}{SE} \quad \text{where } SE = \frac{\sigma}{\sqrt{n}}$$

**Step 3 — Compare and decide:**

| Test | H₁ | Reject H₀ if |
|---|---|---|
| Two-tailed | μ ≠ μ₀ | \|Z\| > Z\* (i.e. Z < −Z\* or Z > +Z\*) |
| Right-tailed | μ > μ₀ | Z > +Z\* |
| Left-tailed | μ < μ₀ | Z < −Z\* |

```
Two-tailed                       Right-tailed                Left-tailed

 Reject |  Accept  | Reject        Accept   | Reject      Reject |  Accept
────────┼──────────┼────────    ────────────┼────────     ───────┼────────────
       -Z*    0   +Z*                   0  +Z*                 -Z*    0
```

### Steps

1. State H₀ and H₁
2. Choose significance level α
3. Compute the test statistic from sample data:

$$Z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}$$

4. Find the critical value Z\* from the Z-table based on α and test type
5. Compare: if test statistic falls in the rejection region → reject H₀

### Rejection Regions

| Test | Reject H₀ if |
|---|---|
| Two-tailed (α=0.05) | Z < −1.96 or Z > +1.96 |
| Right-tailed (α=0.05) | Z > +1.645 |
| Left-tailed (α=0.05) | Z < −1.645 |

```
Two-tailed (α = 0.05)

Reject  |          Accept          |  Reject
────────┼──────────────────────────┼────────
       -1.96         0           +1.96
```

### Worked Example — Delivery Time

**Claim:** Average delivery time = 30 minutes.  
**Sample:** n = 50, x̄ = 32 min, σ = 8 min.  
**Test at α = 0.05 — has the delivery time changed?**

| Step | Detail |
|---|---|
| H₀ | μ = 30 |
| H₁ | μ ≠ 30 (two-tailed — "changed") |
| SE | 8/√50 = 1.13 |
| Z | (32 − 30) / 1.13 = **1.77** |
| Z\* | ±1.96 (two-tailed, α=0.05) |
| Decision | 1.77 < 1.96 → **fail to reject H₀** |

**Conclusion:** Not enough evidence to say delivery time has changed at 5% significance.

---

## Connection to Confidence Intervals

Hypothesis testing and CIs are two sides of the same coin:

| | CI approach | Hypothesis test approach |
|---|---|---|
| Question | Where is μ likely to be? | Is μ = μ₀ plausible? |
| Answer | A range: (a, b) | Reject / fail to reject |
| Link | If μ₀ falls outside the CI → reject H₀ at the same α |

> For the delivery example: 95% CI = 32 ± 1.96×1.13 = (29.79, 34.21). Since 30 is inside the CI → fail to reject H₀. Same conclusion, different method.

---

## Practice Questions

### Q1 — Frame H₀ and H₁, identify test type

For each scenario, write H₀ and H₁ and state whether it is left-tailed, right-tailed, or two-tailed.

**a)** A bank claims its average loan processing time is 5 days. An auditor suspects it is taking longer.

<details>
<summary>Answer</summary>

- H₀: μ ≤ 5 days
- H₁: μ > 5 days
- **Right-tailed** — auditor suspects it has increased

</details>

---

**b)** A manufacturer claims its bulbs last 1,000 hours. A consumer group wants to check if the claim is false (in either direction).

<details>
<summary>Answer</summary>

- H₀: μ = 1,000 hours
- H₁: μ ≠ 1,000 hours
- **Two-tailed** — "false" means could be above or below

</details>

---

**c)** A new drug is claimed to reduce blood pressure. A researcher wants to test if it actually reduces it.

<details>
<summary>Answer</summary>

- H₀: μ ≥ μ_old (drug has no reduction or increases BP)
- H₁: μ < μ_old (drug reduces BP)
- **Left-tailed** — looking for a decrease

</details>

---

**d)** A factory claims its bags are filled with at least 500g. A regulator suspects underfilling.

<details>
<summary>Answer</summary>

- H₀: μ ≥ 500g
- H₁: μ < 500g
- **Left-tailed** — regulator suspects it is below 500g

</details>

---

### Q2 — Reject or Fail to Reject

**a)** Z = 2.1, two-tailed test, α = 0.05 (Z\* = 1.96)

<details>
<summary>Answer</summary>

|Z| = 2.1 > 1.96 → **Reject H₀**

</details>

---

**b)** Z = 1.5, right-tailed test, α = 0.05 (Z\* = 1.645)

<details>
<summary>Answer</summary>

Z = 1.5 < 1.645 → **Fail to reject H₀**

</details>

---

**c)** Z = −2.0, left-tailed test, α = 0.01 (Z\* = −2.326)

<details>
<summary>Answer</summary>

Z = −2.0 > −2.326 → does not cross into rejection region → **Fail to reject H₀**

</details>

---

**d)** Z = 1.7, two-tailed test, α = 0.10 (Z\* = 1.645)

<details>
<summary>Answer</summary>

|Z| = 1.7 > 1.645 → **Reject H₀**

Note: same Z = 1.7 would **fail to reject** at α = 0.05 (Z\* = 1.96). α matters.

</details>

---

### Q3 — Type I and Type II Errors

**a)** A court uses "innocent until proven guilty." Map this to H₀/H₁ and identify what Type I and Type II errors mean here.

<details>
<summary>Answer</summary>

- H₀: defendant is innocent
- H₁: defendant is guilty
- **Type I Error:** convicting an innocent person (wrongly rejecting H₀)
- **Type II Error:** acquitting a guilty person (failing to reject a false H₀)

</details>

---

**b)** A doctor tests whether a patient has a disease. What are the two errors and which is more dangerous?

<details>
<summary>Answer</summary>

- H₀: patient does not have the disease
- H₁: patient has the disease
- **Type I Error:** diagnosing a healthy patient as sick (false positive) → unnecessary treatment
- **Type II Error:** missing the disease in a sick patient (false negative) → untreated illness
- **Type II is more dangerous** — a missed disease can be fatal. So α is kept higher (more lenient) to reduce Type II errors, accepting more false positives.

</details>

---

**c)** If you lower α from 0.05 to 0.01, what happens to Type I and Type II error rates?

<details>
<summary>Answer</summary>

- Type I error rate **decreases** (harder to wrongly reject H₀)
- Type II error rate **increases** (easier to miss a real effect)
- There is always a trade-off between the two.

</details>

---

**d)** A spam filter flags emails as spam (H₁) or not spam (H₀). Which error is Type I and which is Type II? Which would users find more annoying?

<details>
<summary>Answer</summary>

- **Type I Error:** marking a legitimate email as spam (false positive)
- **Type II Error:** letting spam through to inbox (false negative)
- Most users find **Type I more annoying** — missing an important email is worse than seeing some spam. So spam filters are tuned to keep α low, accepting more spam to avoid losing real emails.

</details>

---

---

## Summary

| Concept | Detail |
|---|---|
| H₀ | Status quo, contains equality, assumed true |
| H₁ | What you want to prove, contains strict inequality |
| α | Significance level — threshold for rejecting H₀ |
| Test statistic | Z = (x̄ − μ₀) / (σ/√n) |
| Critical value Z\* | From Z-table based on α and test direction |
| Reject H₀ | When test statistic falls in rejection region |
| Type I Error | Wrongly rejecting H₀ (probability = α) |
| Type II Error | Failing to detect a real effect (probability = β) |

---

## Topics Covered

| Topic | Covered |
|---|---|
| Types of hypotheses (H₀, H₁, rules, examples) | ✓ |
| Types of statistical tests (two-tailed, left, right — decided by H₁) | ✓ |
| Criteria for making decisions (α, Type I, Type II, trade-off) | ✓ |
| Critical value method (exam flow: α → Z\* → Z → compare) | ✓ |
