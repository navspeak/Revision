# UCV, LCV and Alpha

## UCV and LCV — Z-score vs Original Scale

Z\* and −Z\* are UCV and LCV in **Z-score terms**. To convert to the **original scale**:

$$UCV = \mu + Z^* \times SE$$
$$LCV = \mu - Z^* \times SE$$

F(Z\*) is only the intermediate step used to **look up** Z\* in the Z-table. Once you have Z\*, that number is the UCV/LCV in Z-score terms.

```
F(Z*) = 0.975  →  Z-table  →  Z* = 1.96 = UCV (Z-score)
                               -Z* = -1.96 = LCV (Z-score)

Original scale:
  UCV = μ + 1.96 × SE
  LCV = μ - 1.96 × SE
```

**Example — Manufacturer claim (μ=36, σ=4, n=49, Z\*=2.17):**

| | Formula | Value |
|---|---|---|
| SE | 4/√49 | 0.5714 months |
| UCV | 36 + 2.17 × 0.5714 | **37.24 months** |
| LCV | 36 − 2.17 × 0.5714 | **34.76 months** |

x̄ = 34.5 < LCV = 34.76 → falls below LCV → **reject H₀**

> Decision on original scale and Z-score scale always give the same answer — just two ways of expressing the same comparison.

---

## Cumulative Probability at the Critical Value

The Z-table always gives area to the **left**. So you always convert your tail area into a left-area before looking up.

| Test | Cumulative probability at Z\* | Look up in Z-table |
|---|---|---|
| Right-tailed / UCV | 1 − α | F(Z\*) = 1 − α |
| Left-tailed / LCV | α | F(Z\*) = α |
| Two-tailed UCV | 1 − α/2 | F(Z\*) = 1 − α/2 |
| Two-tailed LCV | α/2 | F(Z\*) = α/2 |

---

## Practice Questions

**Q1.** α = 3%, upper-tailed test. What is the cumulative probability at UCV?

<details>
<summary>Answer</summary>

Right-tailed → all α in right tail → left area = 1 − 0.03 = **0.97**  
Look up 0.97 in Z-table → Z\* ≈ 1.88

</details>

---

**Q2.** α = 5%, lower-tailed test. What is the cumulative probability at LCV?

<details>
<summary>Answer</summary>

Left-tailed → all α in left tail → left area = α = **0.05**  
Look up 0.05 in Z-table → Z\* ≈ −1.645

</details>

---

**Q3.** α = 1%, two-tailed test. What are the cumulative probabilities at LCV and UCV?

<details>
<summary>Answer</summary>

Two-tailed → α/2 = 0.005 in each tail  
- LCV: left area = 0.005 → Z\* = −2.576  
- UCV: left area = 1 − 0.005 = **0.995** → Z\* = +2.576

</details>

---

**Q4.** α = 10%, upper-tailed test. What is the cumulative probability at UCV and the Z\*?

<details>
<summary>Answer</summary>

Right-tailed → left area = 1 − 0.10 = **0.90**  
Look up 0.90 in Z-table → Z\* = 1.28

</details>

---

**Q5.** α = 2%, two-tailed test. What is the cumulative probability at UCV?

<details>
<summary>Answer</summary>

Two-tailed → α/2 = 0.01 in each tail  
UCV: left area = 1 − 0.01 = **0.99**  
Look up 0.99 in Z-table → Z\* = 2.326

</details>

---

**Q6.** The cumulative probability at UCV is 0.96. What is α and what type of test is it?

<details>
<summary>Answer</summary>

UCV cumulative = 1 − α = 0.96 → α = **0.04 = 4%**  
UCV exists → **right-tailed test**

</details>
