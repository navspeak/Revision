# MAPE — Mean Absolute Percentage Error

**MAPE = Mean Absolute Percentage Error**

It expresses the error as a **percentage of the actual value** — so instead of saying "I was off by 5 points", it says "I was off by 8%".

```
MAPE = mean(|y - ŷ| / y) × 100
```

---

## Concrete Example (5-student dataset)

| Student | y (actual) | ŷ (predicted) | \|y − ŷ\| | \|y − ŷ\| / y | % error |
|---------|-----------|--------------|-----------|--------------|---------|
| A | 52 | 51.6 | 0.4 | 0.4/52 | 0.77% |
| B | 58 | 58.3 | 0.3 | 0.3/58 | 0.52% |
| C | 65 | 65.0 | 0.0 | 0.0/65 | 0.00% |
| D | 71 | 71.7 | 0.7 | 0.7/71 | 0.99% |
| E | 79 | 78.4 | 0.6 | 0.6/79 | 0.76% |

```
MAPE = (0.77 + 0.52 + 0.00 + 0.99 + 0.76) / 5 = 3.04 / 5 = 0.61%
```

Model is off by **0.61% on average** — very good.

---

## MAPE vs RMSE — Same Data, Different Story

Both measure prediction error. The difference is **what they express it in**.

Using the same 5 students:

```
SSE  = 1.10
MSE  = 0.22
RMSE = √0.22 = 0.47 score points
MAPE = 0.61%
```

**RMSE says:** "on average, predictions are off by 0.47 score points"
**MAPE says:** "on average, predictions are off by 0.61% of the actual score"

RMSE is harder to judge without context — 0.47 out of 65 is great, but 0.47 out of 0.5 would be terrible. MAPE removes that ambiguity.

---

## Why Use MAPE Over RMSE?

| Situation | Better metric |
|-----------|--------------|
| Need to explain error to non-technical stakeholders | MAPE — "we're off by 8%" is intuitive |
| Comparing models across different scales of y | MAPE — scale-independent |
| Large errors are very costly | RMSE — penalises big errors more due to squaring |
| y has values close to 0 | Avoid MAPE — division by near-zero explodes |
| Outliers present | Avoid RMSE — squaring amplifies outlier impact |

---

## Scale Problem — Why RMSE Needs Context

Imagine two different prediction problems:

```
Problem 1 — Exam scores (range 0–100):
  RMSE = 5.0   → off by 5 out of 100 → not bad
  MAPE = 6.2%  → immediately clear

Problem 2 — House prices (range ₹50L–₹5Cr):
  RMSE = 5.0   → off by ₹5 → excellent!
  RMSE = 500000 → off by ₹5L → bad

MAPE = 8% means the same thing in both problems.
```

---

## When MAPE Breaks Down

```
y = 0  →  |y - ŷ| / y = anything / 0  →  undefined
y = 2  →  error of 1.5 → MAPE = 75%  (looks terrible)
y = 200 →  error of 1.5 → MAPE = 0.75% (looks great)
```

Same absolute error, wildly different MAPE — MAPE is sensitive to small actual values.

---

## Thumb Rule

```
MAPE < 10%   → good
MAPE 10–20%  → acceptable
MAPE > 20%   → poor
```

---

## Summary

| Metric | Formula | Unit | Strength | Weakness |
|--------|---------|------|----------|----------|
| RMSE | √(SSE/n) | Same as y | Penalises large errors | Hard to judge without knowing scale of y |
| MAPE | mean(\|y−ŷ\|/y)×100 | % | Intuitive, scale-free | Breaks when y is near 0 |
