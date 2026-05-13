# The p-value Method

## What is the p-value?

The p-value is the probability of observing a result **as extreme or more extreme** than your sample, **assuming H₀ is true**.

> Informal: the higher the p-value, the more likely you are to fail to reject H₀. The lower the p-value, the more evidence against H₀.

**Common misconception:** p-value is NOT the probability that H₀ is true. It is the probability of seeing this data (or more extreme) *if* H₀ were true.

---

## Steps — p-value Method

1. State H₀ and H₁
2. Compute Z from sample data: Z = (x̄ − μ₀) / SE
3. Find cumulative probability F(Z) from Z-table
4. Compute p-value from F(Z) based on test type
5. Compare p-value with α → decide

---

## Computing p-value from Z

### Right-tailed (H₁: μ > μ₀)

```
         Accept H₀          │  Reject H₀
                             │
    ╭────────────────────╮   │  ╭─╮
   ╭╯                    ╰╮  │ ╭╯ ╰─╮
  ╭╯                      ╰──┼─╯    ╰───
──╯                          │
              0             Z*   Z
                                 ↑
                             p = area to right of Z
                             p = 1 − F(Z)
```

p-value = 1 − F(Z)  
Reject H₀ if p ≤ α

---

### Left-tailed (H₁: μ < μ₀)

```
  Reject H₀  │          Accept H₀
             │
  ╭─╮        │   ╭────────────────────╮
╭─╯  ╰╮      │  ╭╯                    ╰╮
╯      ╰─────┼──╯                      ╰╮
             │
          Z  Z*              0
          ↑
      p = area to left of Z
      p = F(Z)
```

p-value = F(Z)  
Reject H₀ if p ≤ α

---

### Two-tailed (H₁: μ ≠ μ₀)

```
  Reject │         Accept H₀          │ Reject
         │                            │
  ╭─╮   │   ╭────────────────────╮   │  ╭─╮
╭─╯  ╰╮ │  ╭╯                    ╰╮  │ ╭╯  ╰╮
╯      ╰─┼──╯                      ╰─┼─╯    ╰─
         │                           │
        -Z*            0            +Z*   +Z
  ←p/2→                                 ←p/2→
  
  p = 2 × (1 − F(|Z|))     ← always use |Z| then multiply by 2
```

Reject H₀ if p ≤ α

---

### Summary — p-value formulas

| Test | Z sign | p-value |
|---|---|---|
| Right-tailed | + | 1 − F(Z) |
| Left-tailed | − | F(Z) |
| Two-tailed | ±  | 2 × (1 − F(\|Z\|)) |

**Example:** Z = +3.02 → F(3.02) = 0.9987
- Right-tailed: p = 1 − 0.9987 = **0.0013**
- Two-tailed: p = 2 × 0.0013 = **0.0026**

**Example:** Z = −3.02 → F(−3.02) = 0.0013
- Left-tailed: p = **0.0013**
- Two-tailed: p = 2 × 0.0013 = **0.0026**

> Z of +3.02 and −3.02 give the same two-tailed p-value by symmetry.

---

## Decision Rule

| p-value vs α | Decision |
|---|---|
| p-value ≤ α | Reject H₀ — result is statistically significant |
| p-value > α | Fail to reject H₀ — insufficient evidence |

---

## p-value vs Critical Value Method

Two methods, same answer — both require α and compute the same Z from data:

| | Critical Value Method | p-value Method |
|---|---|---|
| **Given** | α | α |
| **Compute** | Z from data, Z\* from α | Z from data, p-value from F(Z) |
| **Compare** | Z vs Z\* | p-value vs α |
| **Reject H₀ if** | \|Z\| > Z\* | p-value < α |

> Mathematically equivalent — if Z > Z\* then p < α, always. Same Z, different comparison space (Z-space vs probability space).

---

## Worked Example — FSSAI Lead Content

**Setup:** μ₀ = 2.5 ppm, x̄ = 2.6, s = 0.6, n = 100. Right-tailed test.

| Step | Calculation |
|---|---|
| SE | 0.6/√100 = 0.06 |
| Z | (2.6 − 2.5) / 0.06 = 1.67 |
| F(Z) | F(1.67) = 0.9525 |
| p-value | 1 − 0.9525 = **0.0475** |

**At α = 5% (0.05):** p = 0.0475 < 0.05 → **Reject H₀** ✓  
**At α = 3% (0.03):** p = 0.0475 > 0.03 → **Fail to reject H₀** ✓

Same conclusions as the critical value method.

---

## Worked Example — Manufacturer Claim (Product Life)

**Setup:** μ₀ = 36, x̄ = 34.5, σ = 4, n = 49, α = 3%. Two-tailed test.

**Hypotheses:**
- H₀: μ = 36 months
- H₁: μ ≠ 36 months

**Step 1 — Z from data:**

| | Calculation |
|---|---|
| SE | 4/√49 = 0.5714 |
| Z | (34.5 − 36) / 0.5714 = **−2.62** |

**Step 2 — p-value from Z:**

Sample mean (34.5) is on the **left** of μ₀ (36) → Z is negative → left side of distribution.  
Two-tailed → multiply by 2.

F(−2.62) = **0.0044** (from Z-table)

p-value = 2 × 0.0044 = **0.0088**

**Step 3 — Decision:**

p = 0.0088 < α = 0.03 → **Reject H₀**

**Conclusion:** At 3% significance, there is sufficient evidence to reject the manufacturer's claim. The average product life is not 36 months.

> **Why multiply by 2?** Two-tailed test cares about extreme results in *either* direction. The left tail gives p/2 = 0.0044. The symmetric right tail also contributes 0.0044. Total p = 0.0088.

---

## Key Notes

- **Fail to reject H₀ ≠ H₀ is true** — the data just wasn't extreme enough
- For two-tailed tests always **multiply p by 2** before comparing with α
- When population σ is unknown, use s/√n as SE
- p-value gives more information than just reject/fail to reject — a p of 0.001 is stronger evidence against H₀ than a p of 0.049, even though both reject at α = 0.05
