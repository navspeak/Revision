# Soft Margin and the `C` Hyperparameter

The hard margin from [[4aMaximumMarginClassifier]] demands a *perfect* split — which
real data (spam, ham, overlap, outliers) never gives. The fix:

```
Soft margin: ALLOW some points to violate the margin (or even be misclassified),
             but PENALISE each violation.
```

This trades a few mistakes for a wider, more robust street.

---

## Slack — Measuring the Violation

Each point gets a **slack** value `ξ` (xi) = how far it intrudes:

```
ξ = 0      → point is on the correct side, outside the margin   (good)
0 < ξ ≤ 1  → point is inside the margin but still correctly classified
ξ > 1      → point is on the WRONG side (misclassified)
```

```
        • •
        • • ●           margin edge
      ─────────────
      │  ξ=0.6 •     │   ← inside the street (small slack)
      │  hyperplane  │
      │        ╳ ξ=1.3│  ← crossed over (misclassified, big slack)
      ─────────────
        ╳ ╳
```

The SVM now minimises:

```
   minimise   ‖W‖² / 2   +   C · Σ ξ_i
              └───┬────┘       └──┬───┘
            wide margin      total violation penalty
```

`C` sets the exchange rate between **"keep the margin wide"** and
**"don't violate it"**.

---

## Lecture Formulation — Slack on the Normalised Margin

[[4aMaximumMarginClassifier]] wrote the **hard** margin in the normalised form
(`ΣWᵢ² = 1`, maximise `M`):

```
   lᵢ · (W · Yᵢ)  ≥  M        every point at least a full margin M away

   lᵢ  = label of the i-th observation (+1 spam / −1 ham)
   W   = coefficient vector  [w₀, w₁, w₂, w₃]
   Yᵢ  = the point's values  [1, y₁, y₂, y₃]
   W·Yᵢ = w₀ + w₁y₁ + w₂y₂ + w₃y₃   (the hyperplane score)
```

Because the weights are normalised, `W·Yᵢ` is literally the **perpendicular
distance** of point `i` from the hyperplane — its sign says which side, its size
says how far.

Demanding a *full* margin `M` for every point is the brittle hard margin. To relax
it, attach a **slack variable** `εᵢ` to each point and shrink its required clearance:

```
   lᵢ · (W · Yᵢ)  ≥  M (1 − εᵢ)          εᵢ ∈ [0, ∞)
```

```
εᵢ = 0        → full margin met → correct side, safely outside the street
0 < εᵢ ≤ 1    → inside the margin, but STILL correctly classified
εᵢ > 1        → pushed past the hyperplane → on the WRONG side (misclassified)
```

This is the same relaxation as the `ξ` slack above — just written on the normalised
`M` formulation instead of the scaled `‖W‖`/`C` objective. `M(1 − εᵢ)` lowers the bar
for awkward points so a workable boundary exists.

---

## What `C` Does

```
Large C  → violations are EXPENSIVE → narrow margin, few mistakes
           → tries hard to classify every training point correctly
           → approaches HARD margin → OVERFIT risk

Small C  → violations are CHEAP → wide margin, tolerates mistakes
           → smoother, more general boundary
           → too small → UNDERFIT risk
```

```
   Small C (wide margin)            Large C (narrow margin)
   ──────────────────               ──────────────────
   •  •   │░░░░░│   ╳ ╳             •  • │▒│ ╳ ╳
   •  • ● │░░░░░│ ● ╳               •  •●│▒│● ╳
   •   ●  │░░░░░│  ● ╳ ╳            • ● │▒│ ●╳ ╳
   wide street, a few inside        thin street, hugs the points
   (more bias, less variance)       (less bias, more variance)
```

---

## `C` Is a Bias-Variance Knob

This is the direct link back to [[1BiasVsVariance]]:

| `C` | Margin | Bias | Variance | Behaviour |
|-----|--------|------|----------|-----------|
| **Small** | Wide | High | Low | Underfit — too forgiving |
| **Just right** | Balanced | Low | Low | Generalises well |
| **Large** | Narrow | Low | High | Overfit — memorises noise |

```
C ↑  →  variance ↑, bias ↓   (stricter, hugs the data)
C ↓  →  bias ↑, variance ↓   (looser, wider street)
```

You **tune `C`** (e.g. by cross-validation / grid search) to find the bottom of the
bias-variance U-curve.

---

## Hard vs Soft Margin

| | Hard margin | Soft margin |
|-|-------------|-------------|
| Violations | None allowed | Allowed, penalised by `C` |
| Needs | Perfectly separable data | Works on overlapping / noisy data |
| Outliers | Catastrophic | Tolerated |
| Hyperparameter | — | `C` |
| Real-world use | Rare | **The default in practice** |

> `C → ∞` recovers the hard margin (no violations tolerated).

---

## Summary

```
Soft margin = max-margin + permission to break the rules, at a price.

  slack ξ   measures each violation (0 = clean, >1 = misclassified)
  objective: minimise  ‖W‖²/2  +  C·Σξ
                       (wide margin)  (penalty)

  Large C → strict, narrow margin, low bias / HIGH variance → overfit
  Small C → lenient, wide margin, HIGH bias / low variance → underfit
  Tune C  → balance the bias-variance trade-off  [[1BiasVsVariance]]

Soft margin is what real SVMs use; hard margin is the C→∞ special case.
```

> **Next:** when even a soft *line* can't separate the classes (non-linear data),
> we use the **kernel trick** to bend the boundary. See the companion notebook
> `4_MaximumMargin.ipynb` for the effect of `C` on the spam data.
