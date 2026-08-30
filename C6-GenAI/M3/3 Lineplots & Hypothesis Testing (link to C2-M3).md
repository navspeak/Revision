# Line Plots ↔ Hypothesis Testing — How They Connect

A bridge note linking the visualisation work in [`2 Lineplot Tutorial.ipynb`](2%20Lineplot%20Tutorial.ipynb) back to the inferential statistics from **C2 → M3**.

**Related notes (C2/M3):**
- [`2HypothesisTesting.md`](../../C2/M3/2HypothesisTesting.md) — H₀/H₁, α, Z vs Z\*, errors
- [`3pValue.md`](../../C2/M3/3pValue.md) — the p-value method
- [`6CLT_Inference.md`](../../C2/M3/6CLT_Inference.md) — CLT, sampling distribution, standard error
- [`0ZStar.md`](../../C2/M3/0ZStar.md) — critical values

---

## The one idea that ties them together

When `sns.lineplot` is given **many y-values per x**, it doesn't just draw a line — it draws the **mean** and shades a **95% confidence interval** around it. That shaded band *is* inferential statistics, rendered visually.

```python
# From the notebook — many days share a month, so seaborn aggregates:
sns.lineplot(data=df, x="month", y="sales")   # mean line + 95% CI band
```

Every piece of that band traces straight back to C2/M3:

| In the line plot | C2/M3 concept | Note |
|------------------|---------------|------|
| The solid line | **point estimate** (sample mean x̄) | the `estimator` (default `mean`) |
| The shaded band | **confidence interval** for μ | [6CLT_Inference](../../C2/M3/6CLT_Inference.md) |
| Band width | **standard error** SE = σ/√n | narrower with more data per x |
| 95% (default) | **confidence level** 1 − α | α = 0.05 |
| `errorbar=("ci", 90)` | choosing a different **α** | 90% → α = 0.10 |
| `errorbar="sd"` | spread of the data, **not** a CI | describes data, doesn't infer μ |

> **Key distinction the band makes visible:** `errorbar="ci"` is *inference about the mean* (gets tighter as n grows). `errorbar="sd"` is *description of the spread* (stays roughly fixed). Same-looking band, completely different claim — exactly the estimate-vs-describe split from C2/M3.

---

## Reading a CI band as a hypothesis test

C2/M3 established that **CIs and hypothesis tests are two sides of the same coin** (see the "Connection to Confidence Intervals" section in [2HypothesisTesting.md](../../C2/M3/2HypothesisTesting.md#connection-to-confidence-intervals)):

> If a claimed value μ₀ falls **outside** the CI → **reject H₀** at that same α.

So you can run a visual hypothesis test straight off the plot:

```
        H₀: μ = μ₀                 ── claimed value (e.g. target sales)
   ─────●───────────────           μ₀ sits INSIDE the band  → fail to reject H₀
        │░░░░░░░░░░░░░│
   ─────┼──── x̄ ─────┼──           95% CI band from lineplot
        │░░░░░░░░░░░░░│
                  ●                 μ₀ sits OUTSIDE the band → reject H₀
```

**Worked link** — suppose the business target is μ₀ = 130 sales:
1. `sns.lineplot` shows the mean monthly sales with its 95% band.
2. Draw `plt.axhline(130)` across the plot.
3. If the line pierces *outside* the band in some month → the data is inconsistent with the 130 target at α = 0.05 → **reject H₀** for that month.

```python
sns.lineplot(data=df, x="month", y="sales")
plt.axhline(130, color="red", ls="--", label="target μ₀ = 130")  # the H₀ claim
plt.legend()
```

This is the **critical-value method** (`|Z| > Z*` → reject) and the **CI method** producing the *same* decision — just read with your eyes instead of a Z-table.

---

## Why the synthetic dataset reinforces this

The notebook builds `sales = trend + season + noise`, where:

```python
noise = rng.normal(0, 4, 365)   # mean 0, std 4, NORMALLY distributed
```

That `rng.normal(...)` is the same **normality** assumption hypothesis testing leans on:
- C2/M3's Z-test assumes the sampling distribution of x̄ is normal (the **CLT** — [6CLT_Inference](../../C2/M3/6CLT_Inference.md)).
- Your time-series notes ([`1 Components of Time Series Data.md`](1%20Components%20of%20Time%20Series%20Data.md)) state noise should be **additive and normally distributed**.
- Same Gaussian assumption, two different courses — which is why the residual ("noise") component is exactly what you'd run a hypothesis test on later (e.g. "is the residual mean really 0?").

---

## Quick cross-reference cheatsheet

| Question | Visual tool (C6/M3 notebook) | Formal tool (C2/M3) |
|----------|------------------------------|----------------------|
| Where is μ likely to be? | CI band in `lineplot` | confidence interval |
| Is a claim μ₀ plausible? | does μ₀ fall outside the band? | hypothesis test, `\|Z\| > Z*` |
| How confident? | 95% band (default) | 1 − α |
| How much risk of false alarm? | widen/narrow via `errorbar` | significance level α |
| Is an effect real or noise? | does the band exclude the baseline? | reject vs fail-to-reject H₀ |

---

## Try it (ties both courses together)

1. Plot monthly sales with the default 95% band, then with `errorbar=("ci", 99)`. Which band is wider, and why? (Link to α = 0.05 vs 0.01 in C2/M3.)
2. Add `plt.axhline` at a target value. For which months would you **reject H₀**?
3. Switch `errorbar="ci"` → `errorbar="sd"`. Explain why one shrinks with more data and the other doesn't — the estimate-vs-describe distinction from C2/M3.
