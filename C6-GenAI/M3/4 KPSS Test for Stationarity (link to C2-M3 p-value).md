# KPSS Test for Stationarity — and its link to the p-value method

The **KPSS test** (Kwiatkowski–Phillips–Schmidt–Shin) checks whether a time series is **stationary**. It's the formal hypothesis test that follows on from the visual ideas in [`1 Components of Time Series Data.md`](1%20Components%20of%20Time%20Series%20Data.md) — and it runs on exactly the **p-value machinery** from **C2 → M3**.

**Related notes:**
- [`3pValue.md`](../../C2/M3/3pValue.md) — the p-value method (p ≤ α → reject H₀)
- [`2HypothesisTesting.md`](../../C2/M3/2HypothesisTesting.md) — H₀/H₁, α, Type I/II errors
- [`1 Components of Time Series Data.md`](1%20Components%20of%20Time%20Series%20Data.md) — level, trend, seasonality (what breaks stationarity)
- [`2 Lineplot Tutorial.ipynb`](2%20Lineplot%20Tutorial.ipynb) — the `df` we test below

---

## 1. What is stationarity? (quick recap)

A series is **stationary** if its statistical properties don't change over time:

| Property | Stationary series | Non-stationary series |
|----------|-------------------|------------------------|
| Mean (level) | constant | drifts (a **trend**) |
| Variance | constant | grows/shrinks over time |
| Autocovariance | depends only on lag, not on *when* | changes over time |

From [1 Components](1%20Components%20of%20Time%20Series%20Data.md): a **trend** or **seasonality** makes the mean depend on time → **non-stationary**. Pure **noise** (additive, normally distributed) is stationary. Most forecasting models (ARMA etc.) require stationarity, so we *test* for it.

---

## 2. What KPSS actually tests — the flipped null ⚠️

This is the single most important thing to get right, and it's where C2/M3 hypothesis-testing intuition must be applied **carefully**:

| | KPSS | (contrast: ADF test) |
|---|---|---|
| **H₀** | series **is stationary** | series is **non-stationary** (has a unit root) |
| **H₁** | series is **non-stationary** | series is stationary |

> **KPSS flips the usual "H₀ = no effect" framing.** Here H₀ = "all good, stationary." So **rejecting H₀ is bad news** — it means non-stationary.

The C2/M3 rules still hold exactly — H₀ contains the equality/status-quo claim, the burden of proof is on H₁ — it's just that "status quo" here happens to be *stationarity*.

KPSS is a **right-tailed** test: the test statistic (an LM statistic) is always ≥ 0, and only **large** values are surprising under H₀. So large stat → small p → reject H₀ → non-stationary. (Compare the right-tailed picture in [3pValue.md](../../C2/M3/3pValue.md#computing-p-value-from-z).)

---

## 3. The decision rule — identical to C2/M3, conclusion reversed

The p-value comparison is **exactly** the rule from [3pValue.md](../../C2/M3/3pValue.md#decision-rule):

| p-value vs α | Statistical decision | **Meaning for KPSS** |
|---|---|---|
| p ≤ α | **Reject H₀** | series is **NON-stationary** ✗ |
| p > α | **Fail to reject H₀** | **treat as stationary** ✓ |

So the muscle memory "small p = significant = exciting effect" must be inverted: in KPSS, **small p = non-stationary = you have work to do** (difference the series, remove trend, etc.).

> **Caveat (worth a mental note):** `statsmodels` computes the KPSS p-value by interpolating a small **lookup table** of critical values, so it's reported only within `[0.01, 0.10]` and gets clipped at the ends (with a warning). Unlike the smooth Z-table F(Z) in C2/M3, you can't read an arbitrarily tiny p — you just know "p < 0.01."

---

## 4. Concrete example — testing the notebook's `df`

Recall the series built in [`2 Lineplot Tutorial.ipynb`](2%20Lineplot%20Tutorial.ipynb):

```python
trend  = np.linspace(100, 160, 365)              # upward trend  → breaks stationarity
season = 15 * np.sin(np.arange(365) * 2*np.pi/30)  # 30-day seasonality
noise  = rng.normal(0, 4, 365)                   # stationary noise
sales  = trend + season + noise
```

That series has a clear **upward trend**, so we *expect* KPSS to flag it as non-stationary.

### Run KPSS

```python
from statsmodels.tsa.stattools import kpss

# regression="c": test stationarity around a constant (level stationarity)
stat, p_value, n_lags, crit = kpss(df["sales"], regression="c", nlags="auto")

print(f"KPSS statistic : {stat:.4f}")
print(f"p-value        : {p_value:.4f}")
print(f"critical values: {crit}")    # e.g. {'10%':0.347,'5%':0.463,'2.5%':0.574,'1%':0.739}
```

**Typical output for this trended series:**

```
KPSS statistic : 2.10   (≫ the 5% critical value 0.463)
p-value        : 0.01   (clipped — actually < 0.01)
critical values: {'10%': 0.347, '5%': 0.463, '2.5%': 0.574, '1%': 0.739}
```

### Apply the C2/M3 decision — both methods, same answer

| Method | Comparison | C2/M3 source |
|--------|-----------|--------------|
| **Critical-value** | stat 2.10 > Z\*-analogue 0.463 (5%) → reject H₀ | [2HypothesisTesting](../../C2/M3/2HypothesisTesting.md#the-critical-value-method) |
| **p-value** | p = 0.01 ≤ α = 0.05 → reject H₀ | [3pValue](../../C2/M3/3pValue.md#decision-rule) |

**Conclusion:** Reject H₀ ⇒ the `sales` series is **non-stationary** (the trend gives it away — exactly as the line plot showed visually).

### Fix it and re-test

Differencing removes the trend. The residual should then look like the stationary `noise` component:

```python
diff = df["sales"].diff().dropna()      # first difference
stat2, p2, _, crit2 = kpss(diff, regression="c", nlags="auto")
print(f"differenced p-value: {p2:.4f}")   # ≈ 0.10 (clipped) → p > α
```

Now **p > α → fail to reject H₀ → treat as stationary** ✓. Same test, opposite conclusion, because we removed the trend that was violating H₀.

---

## 5. KPSS + ADF together (why analysts run both)

Because their nulls are **opposite**, the two tests cross-check each other:

| ADF result | KPSS result | Verdict |
|------------|-------------|---------|
| reject H₀ (stationary) | fail to reject H₀ (stationary) | ✅ **Stationary** — strong agreement |
| fail to reject (non-stat.) | reject H₀ (non-stat.) | ❌ **Non-stationary** — strong agreement |
| fail to reject | fail to reject | ⚠️ trend-stationary — try `regression="ct"` / de-trend |
| reject | reject | ⚠️ difference-stationary — try differencing |

> Remember the **direction** of "reject" is opposite in each column — that's the whole point of pairing them. Mixing up KPSS's flipped null is the #1 student error here, which is why anchoring it to the C2/M3 H₀/H₁ rules is worth doing.

---

## 6. Tie-back to Type I / Type II errors

The error framing from [2HypothesisTesting.md](../../C2/M3/2HypothesisTesting.md#two-types-of-errors) maps cleanly:

- **Type I error (α):** declaring the series non-stationary when it actually *is* stationary → you needlessly difference it (over-differencing → loses information).
- **Type II error (β):** failing to flag a truly non-stationary series → you fit a model on bad data → unreliable forecasts.

Choosing α here is the same trade-off as everywhere in C2/M3 — just with time-series consequences.

---

## 7. One-line summary

> KPSS uses the **exact p-value rule from C2/M3** (`p ≤ α → reject H₀`), but its **H₀ is "stationary"**, so **rejecting means non-stationary**. Small p = trend/unit-root present = difference the series and re-test.

## Try it
1. Run KPSS with `regression="ct"` (trend-stationary) on `df["sales"]` — does the conclusion change? Why might a trend-aware test fail to reject?
2. Run KPSS on the pure `noise` array alone — confirm p > α (stationary).
3. State the H₀, H₁, and the meaning of a Type I error for the differenced series in one sentence each.
