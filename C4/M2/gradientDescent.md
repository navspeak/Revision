# Gradient Descent — Hand Calculation

---

## Setup

**Dataset:**

| x | y |
|---|---|
| 1 | 2 |
| 2 | 4 |
| 3 | 5 |

**Model:** ŷ = β₀ + β₁x

**Cost function:** MSE = (1/n) × Σ(yᵢ − ŷᵢ)²

**Start:** β₀ = 0, β₁ = 0, α = 0.1

---

## Step 1 — Derive the Partial Derivatives

Substitute ŷ = β₀ + β₁x into MSE:

```
MSE = (1/n) × Σ(yᵢ − β₀ − β₁xᵢ)²
```

**∂(MSE)/∂β₀** — differentiate with respect to β₀ (treat β₁ as constant):

```
∂(MSE)/∂β₀ = (1/n) × Σ 2(yᵢ − β₀ − β₁xᵢ) × (−1)
            = (−2/n) × Σ(yᵢ − ŷᵢ)
            = (−2/n) × Σ residuals
```

**∂(MSE)/∂β₁** — differentiate with respect to β₁ (treat β₀ as constant):

```
∂(MSE)/∂β₁ = (1/n) × Σ 2(yᵢ − β₀ − β₁xᵢ) × (−xᵢ)
            = (−2/n) × Σ xᵢ(yᵢ − ŷᵢ)
            = (−2/n) × Σ xᵢ × residuals
```

**Update rule:**

```
β₀ = β₀ − α × ∂(MSE)/∂β₀
β₁ = β₁ − α × ∂(MSE)/∂β₁
```

---

## Iteration 1

**Current:** β₀ = 0, β₁ = 0

Predictions and residuals:

| x | y | ŷ = 0 + 0×x | residual (y − ŷ) |
|---|---|-------------|-----------------|
| 1 | 2 | 0 | 2 |
| 2 | 4 | 0 | 4 |
| 3 | 5 | 0 | 5 |

Partial derivatives:

```
∂(MSE)/∂β₀ = (−2/3) × (2 + 4 + 5)
            = (−2/3) × 11
            = −7.33

∂(MSE)/∂β₁ = (−2/3) × (1×2 + 2×4 + 3×5)
            = (−2/3) × (2 + 8 + 15)
            = (−2/3) × 25
            = −16.67
```

Update:

```
β₀ = 0 − 0.1 × (−7.33)  = 0 + 0.733  = 0.733
β₁ = 0 − 0.1 × (−16.67) = 0 + 1.667  = 1.667
```

Both β values moved up — negative gradient means cost decreases as β increases, so we add.

---

## Iteration 2

**Current:** β₀ = 0.733, β₁ = 1.667

Predictions and residuals:

| x | y | ŷ = 0.733 + 1.667×x | residual (y − ŷ) |
|---|---|---------------------|-----------------|
| 1 | 2 | 2.400 | −0.400 |
| 2 | 4 | 4.067 | −0.067 |
| 3 | 5 | 5.734 | −0.734 |

Partial derivatives:

```
∂(MSE)/∂β₀ = (−2/3) × (−0.400 + (−0.067) + (−0.734))
            = (−2/3) × (−1.201)
            = +0.801

∂(MSE)/∂β₁ = (−2/3) × (1×(−0.400) + 2×(−0.067) + 3×(−0.734))
            = (−2/3) × (−0.400 − 0.134 − 2.202)
            = (−2/3) × (−2.736)
            = +1.824
```

Update:

```
β₀ = 0.733 − 0.1 × 0.801  = 0.733 − 0.080  = 0.653
β₁ = 1.667 − 0.1 × 1.824  = 1.667 − 0.182  = 1.485
```

Both β values moved down slightly — model overshot in iteration 1, now correcting.

---

## Convergence

After many iterations β converges to:

```
β₀ ≈ 1.0,  β₁ ≈ 1.5
```

Which is exactly what OLS gives:  β = (XᵀX)⁻¹ Xᵀy = [1.0, 1.5]

---

## What the Partial Derivative Tells You

```
∂(MSE)/∂β₁ = −16.67   (iteration 1)
```

- Negative → increasing β₁ decreases the cost
- So subtract a negative → β₁ goes up
- Magnitude 16.67 → steep slope, big step needed

```
∂(MSE)/∂β₁ = +1.824   (iteration 2)
```

- Positive → increasing β₁ increases the cost
- So subtract a positive → β₁ comes down
- Magnitude 1.824 → shallow slope, small correction

The sign tells direction. The magnitude tells how steep — and therefore how big the step.

---

## Summary

```
Partial derivative of cost w.r.t. β  →  how much does cost change per unit change in β?

Negative → β too small, push up
Positive → β too large, push down
Zero     → at the minimum, stop
```

Each iteration both β₀ and β₁ are updated simultaneously using their own partial derivatives. After enough iterations the cost stops decreasing — that's convergence.
