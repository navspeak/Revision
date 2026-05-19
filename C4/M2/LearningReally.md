# Does the Model Really "Learn"?

---

## OLS — Solves, Doesn't Learn

OLS doesn't "learn" in the iterative sense — it **solves**. Like solving 2x = 6 → x = 3. No adjustment, no iterations.

```
β = (XᵀX)⁻¹ Xᵀy
```

Hand calculation and sklearn give **identical** results:

```
You do it on paper  →  β₀ = 1.0, β₁ = 1.5
sklearn does it     →  β₀ = 1.0, β₁ = 1.5   ← same
```

There is only one answer — the formula gives it directly.

---

## Gradient Descent — Genuinely Learns

Gradient descent starts knowing nothing, then adjusts step by step based on feedback:

```
Start:  β₀ = 0, β₁ = 0   ← random / zero guess
        ↓
Iteration 1: make predictions, measure error, nudge β
        ↓
Iteration 2: slightly better, nudge again
        ↓
Iteration 3: better still...
        ↓
...converges → β₀ = 1.0, β₁ = 1.5
```

Each iteration the model looks at how wrong it is and adjusts — that's genuine learning.

---

## Side by Side

| | OLS | Gradient Descent |
|-|-----|-----------------|
| Process | Solve the equation | Adjust until close enough |
| Iterations | 1 (one matrix calc) | Many |
| Deterministic? | Yes — same data, always same answer | Yes — but depends on α, iterations |
| "Learning"? | Algebra, not adjustment | True iterative adjustment |

---

## So Why Do We Say a Model "Learns"?

It's loose language. What it really means:

```
"Learning" = finding the β values from data
```

OLS finds them in one shot via algebra.
Gradient descent finds them by iterating.

Both arrive at the same β. OLS just takes a shortcut.

> **OLS** — finds the answer  
> **Gradient Descent** — learns the answer  
> The result is the same. The process is fundamentally different.

---

## So What's the Point of Nudging?

The nudging matters when you **can't solve on paper**.

OLS works because linear regression has a clean closed-form solution. Most models don't:

```
Linear Regression:    β = (XᵀX)⁻¹ Xᵀy   ← algebra works, solve directly

Logistic Regression:  sigmoid makes it non-linear → no closed form → must iterate
Neural Networks:      millions of parameters      → no closed form → must iterate
Deep Learning:        same
```

For these, there is no equation to solve. Gradient descent is the **only option**.

Nudging isn't better than solving — it's what you do **when solving isn't possible**.

```
Can you solve it algebraically?
    Yes → OLS (Linear Regression)
    No  → Gradient Descent (everything else)
```

Linear regression is the exception, not the rule. For almost every other model in machine learning, gradient descent is how learning happens.
