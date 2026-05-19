# Hypothesis Testing — Practice Problems

## Q1 — FSSAI Lead Content Test

The maximum permissible lead in any food product is **2.5 ppm**. As an FSSAI analyst, you test Sunshine brand. A random sample of **n = 100** units gives a sample mean of **x̄ = 2.6 ppm** with standard deviation **s = 0.6 ppm**.

**(a)** Is 2.6 the population mean or sample mean?

<details>
<summary>Answer</summary>

**Sample mean (x̄).** You took 100 samples — their mean was 2.6. The true population mean μ is unknown. The regulatory limit 2.5 is μ₀ (the threshold being tested against).

</details>

---

**(b)** Frame H₀ and H₁. What type of test?

<details>
<summary>Answer</summary>

- H₀: μ ≤ 2.5 (lead within permissible limit)
- H₁: μ > 2.5 (lead exceeds limit)
- **Right-tailed** — you only care if it exceeds the limit

</details>

---

**(c)** Calculate SE and the test statistic Z.

<details>
<summary>Answer</summary>

SE = s/√n = 0.6/√100 = **0.06**

$$Z = \frac{\bar{x} - \mu_0}{SE} = \frac{2.6 - 2.5}{0.06} = \frac{0.1}{0.06} = 1.67$$

> Common mistake: using σ = 0.6 directly → (2.6 ± 0.6) = (2, 3.2). Wrong — that uses individual spread, not SE.

</details>

---

**(d)** Find Z\* and make the decision at α = 5%.

<details>
<summary>Answer</summary>

Right-tailed, α = 0.05 → F(Z\*) = 1 − 0.05 = 0.95 → Z\* = **1.645**

Z = 1.67 > Z\* = 1.645 → falls in critical region → **Reject H₀**

**Conclusion:** At 5% significance, there is sufficient evidence that the lead content exceeds 2.5 ppm. Sunshine fails the FSSAI standard.

</details>

---

**(e)** Calculate the Z-critical score at α = 3% and make the decision.

<details>
<summary>Answer</summary>

Right-tailed, α = 0.03 → F(Z\*) = 1 − 0.03 = **0.97**

Look up 0.97 in Z-table → Z\* = **1.88**

Z = 1.67 < Z\* = 1.88 → does NOT fall in critical region → **Fail to reject H₀**

**Conclusion:** At 3% significance, there is not enough evidence to say lead content exceeds 2.5 ppm.

**UCV on original scale (α = 3%):**

$$UCV = \mu_0 + Z^* \times SE = 2.5 + 1.88 \times 0.06 = 2.6128 \text{ ppm}$$

x̄ = 2.6 < UCV = 2.6128 → just inside acceptance region → **no alarm to raise** at 3%.

**Compare with α = 5%:**

$$UCV = 2.5 + 1.645 \times 0.06 = 2.5987 \text{ ppm}$$

x̄ = 2.6 > UCV = 2.5987 → just crosses → **alarm raised** at 5%.

> Same data, different α → different conclusion. A razor thin margin — which is exactly why α must be chosen before the test, not after.

</details>

---

## Q2 — Manufacturer's Claim (Product Life)

A manufacturer claims the average life of its product is **36 months**. An auditor selects a sample of **49 units**, finds sample mean = **34.5 months**, population σ = **4 months**. Test at **α = 3%**.

**(a)** Frame H₀, H₁ and identify test type.

<details>
<summary>Answer</summary>

- H₀: μ = 36 (claim holds)
- H₁: μ ≠ 36 (claim is false — either direction)
- **Two-tailed** — auditor tests whether the claim is true or false

</details>

---

**(b)** Calculate SE, Z, Z\* and decide.

<details>
<summary>Answer</summary>

SE = 4/√49 = **0.5714**

$$Z = \frac{34.5 - 36}{0.5714} = \frac{-1.5}{0.5714} = -2.625$$

Two-tailed, α = 0.03 → α/2 = 0.015 → F(Z\*) = 1 − 0.015 = 0.985 → Z\* = **2.17**

|Z| = 2.625 > Z\* = 2.17 → **Reject H₀**

**Conclusion:** At 3% significance, the manufacturer's claim of 36 months is rejected.

</details>

---

**(c)** Find UCV and LCV in original scale and verify the decision.

<details>
<summary>Answer</summary>

$$UCV = 36 + 2.17 \times 0.5714 = 37.24 \text{ months}$$
$$LCV = 36 - 2.17 \times 0.5714 = 34.76 \text{ months}$$

x̄ = 34.5 < LCV = 34.76 → falls below LCV → **Reject H₀** ✓

</details>

---

## Q4 — Paracetamol Confidence Interval

**Setup:**
- Acceptable range: 450–550 mg (±10% of 500 mg)
- Sample: n = 100 tablets, x̄ = 530 mg, s = 100 mg
- Confidence level: 95%

**(a)** Calculate the 95% CI for the true population mean paracetamol content.

<details>
<summary>Answer</summary>

SE = s/√n = 100/√100 = **10 mg**

Z\* = 1.96 (95% CI)

$$CI = \bar{x} \pm Z^* \times SE = 530 \pm 1.96 \times 10 = 530 \pm 19.6$$

$$CI = \mathbf{(510.4\ mg,\ 549.6\ mg)}$$

</details>

---

**(b)** Is the manufacturing process running successfully?

<details>
<summary>Answer</summary>

Acceptable range: 450–550 mg.

CI = (510.4, 549.6) — entirely within 450–550 → **process is running successfully**.

We are 95% confident the true mean paracetamol content is between 510.4 mg and 549.6 mg, which is within the permissible range.

> Note: even though x̄ = 530 is above 500, the CI stays within 550 — no regulatory alarm.

</details>

---

**(c)** What is the margin of error?

<details>
<summary>Answer</summary>

$$ME = Z^* \times SE = 1.96 \times 10 = \mathbf{19.6\ mg}$$

</details>

---

## Q3 — Paracetamol Manufacturing Process

A pharma company manufactures paracetamol tablets. The regulatory safe amount is **500 mg**. Too low → quality issue. Too high → regulatory issue. A sample of **n = 900** tablets gives x̄ = **510 mg**, s = **110 mg**. Test at **α = 5%**.

**(a)** Frame H₀, H₁ and identify test type.

<details>
<summary>Answer</summary>

- H₀: μ = 500 (process running correctly)
- H₁: μ ≠ 500 (too low or too high — either is a problem)
- **Two-tailed** — both directions matter

</details>

---

**(b)** Solve using the p-value method.

<details>
<summary>Answer</summary>

SE = s/√n = 110/√900 = 110/30 = **3.67**

$$Z = \frac{510 - 500}{3.67} = \frac{10}{3.67} = 2.72$$

Z is positive (x̄ > μ₀) → right side → p = 2 × (1 − F(2.72))

F(2.72) = 0.9967  
p = 2 × (1 − 0.9967) = 2 × 0.0033 = **0.0065**

p = 0.0065 < α = 0.05 → **Reject H₀**

**Conclusion:** The manufacturing process is not running at 500 mg. Since x̄ = 510 > 500 → **regulatory alarm** (excess paracetamol).

> Note: population σ unknown → used s = 110 as estimate, valid since n = 900 is large.

</details>
