# Z — Notation and Critical Values

## Z vs Z*

Both are Z-scores, but they come from opposite directions:

| Symbol | What it is | How you get it |
|---|---|---|
| **Z** | Computed value — how far your data is from μ | From your data: Z = (x̄ − μ) / SE |
| **Z\*** | Threshold value — the Z that puts X% in the centre | Looked up in advance based on confidence level |

Z\* is sometimes written as Z_α/2 — same thing, different textbooks.

---

## Three Forms of Z

| Context | Formula | Denominator | Covered in |
|---|---|---|---|
| Single observation (probability) | Z = (X − μ) / σ | σ — SD of individuals | Probability / Normal distribution |
| Sample mean (CLT) | Z = (x̄ − μ) / (σ/√n) | SE = σ/√n — SD of sample means | Inferential statistics |
| Critical value | Z\* | Fixed threshold from Z-table | Confidence intervals / Hypothesis testing |

All three ask the same question — "how many standard deviations away from the mean?" — but the denominator changes based on what you are measuring.

---

## How 95% Confidence Gives Z* = 1.96

You want 95% in the **centre**, so 5% is left over in the tails — split equally as 2.5% on each side.

```
     2.5%  |←────────── 95% ──────────→|  2.5%
─────────────────────────────────────────────────
           -Z*           0            +Z*
```

The Z-table gives area to the **left**. You need the Z where the left area = 95% + 2.5% = **97.5% = 0.975**.

Look up 0.975 in the Z-table body → **Z = 1.96**.

---

## General Rule

> The Z\* value depends on the test type — the same confidence level gives a different Z\* for one-tailed vs two-tailed.

### Two-tailed (α split across both tails)

| Confidence | α | Each tail = α/2 | Look up F(Z\*) = 1 − α/2 | Z\* |
|---|---|---|---|---|
| 90% | 0.10 | 5% | 0.95 | 1.645 |
| 95% | 0.05 | 2.5% | 0.975 | 1.96 |
| 99% | 0.01 | 0.5% | 0.995 | 2.576 |

### One-tailed (all α in one tail)

| Confidence | α | Full tail = α | Look up F(Z\*) = 1 − α | Z\* |
|---|---|---|---|---|
| 90% | 0.10 | 10% | 0.90 | 1.28 |
| 95% | 0.05 | 5% | 0.95 | 1.645 |
| 99% | 0.01 | 1% | 0.99 | 2.326 |

### The Overlap — Same Z\* appearing twice

| Z\* | Two-tailed at | One-tailed at |
|---|---|---|
| 1.645 | 90% CL (α=10%) | 95% CL (α=5%) |
| 1.96 | 95% CL (α=5%) | 97.5% CL (α=2.5%) |
| 2.576 | 99% CL (α=1%) | 99.5% CL (α=0.5%) |


```       
 Two-tailed    2.5% |<────────── 95% ──────────>| 2.5%
                ─────┼──────────────────────────────┼─────
                   -1.96          0              +1.96

  One-tailed    <──────────── 97.5% ──────────────>| 2.5%
                ──────────────────────────────────┼──────
                                0              +1.96

* Why Confidence level = 95% in 2 tail == 97.5 in 1 tail
```

Same Z\*, different context — always check the test type before reading off Z\*.
