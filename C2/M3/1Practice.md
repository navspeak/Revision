# Practice — Sampling Distribution

## Given

A CSV with multiple samples, each row having:
- n — sample size
- mean — sample mean

## Notation

| Symbol | Meaning |
|---|---|
| x̄₁, x̄₂, x̄₃, ... | Individual sample means from each row |
| k | Total number of samples (rows in CSV) |
| μ_x̄ | Mean of the sampling distribution |

## Calculate μ_x̄

$$\mu_{\bar{x}} = \frac{\bar{x}_1 + \bar{x}_2 + \bar{x}_3 + \cdots + \bar{x}_k}{k}$$

Simply the average of all the sample means.

## What to Expect

By CLT, μ_x̄ should be very close to the true population mean μ — because E(x̄) = μ. The more samples in the CSV, the closer μ_x̄ will be to μ.

---

## Calculate σ_x̄ — Standard Deviation of the Sampling Distribution

$$\sigma_{\bar{x}} = \sqrt{\frac{\sum(\bar{x}_i - \mu_{\bar{x}})^2}{k}}$$

**Why divide by k and not k−1?**

Because you have all 100 sample means — that makes the 100 entries the **full population** of the sampling distribution, not a sample from it. Bessel's correction (n−1) only applies when you have a sample and are estimating σ from it. When you have the entire population, you divide by n.
