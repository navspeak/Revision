# The Maximum-Margin Classifier

We left [[3cRecallQuiz]] with a question: many lines separate the data equally well —
**which one is best?** The SVM answer:

```
Pick the hyperplane with the WIDEST MARGIN —
the largest gap to the nearest point of EITHER class.
```

This is the **maximum-margin classifier**, the heart of SVM. See [[2SVMMotivation]].

---

## The Problem — Many Valid Lines

All three lines below separate spam from ham with **zero training error**.
But they are not equally good for *new* emails.

```
   money
   │  •  •      ╱  │  ╲
   │ •  •  •   ╱   │   ╲
   │  •  •    ╱  ╳ │ ╳  ╲
   │        ╱   ╳  │  ╳  ╲
   │      ╱  ╳ ╳   │   ╳  ╲
   └────────────────────────── technology
          ╱        │        ╲
       line A    line B    line C
```

A line hugging one class will misclassify the moment a new point lands just over it.
The **safest** line stays as far as possible from both classes.

---

## The Margin

```
The margin = the perpendicular distance from the hyperplane
             to the closest data point on each side.

SVM maximises this margin → "maximum-margin" / "large-margin" classifier.
```

```
              margin
          ┌──────┴──────┐
   • • •  │             │  ╳ ╳ ╳
   • • •  ┊·············┊  ╳ ╳ ╳
   • • •  │  hyperplane │  ╳ ╳ ╳
          │   (middle)  │
   class A│             │ class B
          └─────────────┘
       margin edge   margin edge
```

The hyperplane sits **dead centre** of the widest "street" you can draw between the
two classes. Wider street ⇒ more room for error ⇒ better generalisation.

---

## Support Vectors

```
Support vectors = the data points sitting ON the margin edges.
They alone define the hyperplane.
```

```
        • •
        • •  ●  ← support vector (touches the margin)
      ──────────  margin edge
      │ STREET │
      ──────────  margin edge
        ● ╳  ← support vector
        ╳ ╳
```

Key consequences:

```
✓ Move a NON-support-vector → boundary unchanged.
✓ Move/remove a SUPPORT VECTOR → boundary shifts.
✓ Model stores only the support vectors → memory-efficient.
✓ Far-away points don't matter → robust.
```

That is literally why it's called a **Support Vector** Machine.

---

## Hard Margin — the Strict Version

```
Hard margin: demand that EVERY point is on the correct side of the margin.
             No point is allowed inside the street or across the line.
```

```
✓ Works only if the data is PERFECTLY linearly separable.
✗ One outlier or any class overlap → no solution exists.
✗ Extremely sensitive to noise (a single stray point warps the boundary).
```

Real data (like spam) almost always overlaps a little, so a strict hard margin
is too brittle. The fix is the **soft margin** → [[4bSoftMarginAndC]].

---

## A Little Geometry (intuition, not proof)

For a hyperplane `W·x + c = 0`, the margin width works out to:

```
margin width  =  2 / ‖W‖
```

```
So MAXIMISE margin  ⇔  MINIMISE ‖W‖
   subject to every point being correctly classified with room to spare:

        y_i (W·x_i + c) ≥ 1    for every point i
        (y_i = +1 or −1 is the class label)
```

```
"≥ 1"  → the point is on the correct side AND outside the margin.
"= 1"  → the point is exactly on the margin edge  → a support vector.
```

You don't need to solve this by hand — just hold the picture: **small ‖W‖ = wide street**.

---

## The Two Constraints (Lecture-Notes Formulation)

The lecture states the optimisation as **maximise the margin `M`** subject to **two
constraints**:

**Constraint 1 — normalise the coefficients.** The sum of the squares of all
coefficients must equal 1:

```
   ∑ Wᵢ²  = 1        e.g. 20 attributes → W₀² + W₁² + … + W₂₀² = 1
```

Why: scaling all the `W`s up or down describes the *same* line but changes the raw
score. Fixing `ΣWᵢ² = 1` (a unit vector) makes the score `W₀ + W₁x₁ + W₂x₂` equal to
the **actual perpendicular distance** from the point to the hyperplane — so `M`
becomes a real geometric margin, not an arbitrary number.

**Constraint 2 — every point at least a margin `M` away** (on the correct side):

```
   lᵢ · (Wᵢ · Yᵢ)  ≥  M        for every point i

   lᵢ = label (+1 / −1)
   Wᵢ = coefficients
   Yᵢ = the point's feature values (a row)
```

This is exactly the correctness condition from [[2SVMMotivation]] §2.2, now demanding a
**full margin `M`** of clearance rather than mere correctness.

### Worked Example — Figures (A) and (B)

Take a 2D hyperplane `W₀ + W₁x₁ + W₂x₂ = 0` and a point `Y(p, q)`:

```
Figure (A): RED dots, BELOW the line, label = −l
   i)  W₀ + W₁p + W₂q  <  0        (negative score, below the line)
   ii) label = −l
   ⇒  −l × (W₀ + W₁p + W₂q)  ≥  M     (neg × neg = POSITIVE ≥ M)  ✓

Figure (B): BLUE dots, ABOVE the line, label = +l
   i)  W₀ + W₁p + W₂q  >  0        (positive score, above the line)
   ii) label = +l
   ⇒  +l × (W₀ + W₁p + W₂q)  ≥  M     (pos × pos = POSITIVE ≥ M)  ✓
```

In **both** cases `label × score ≥ M`. The label's sign cancels the score's sign, so a
correctly-classified point *always* yields a positive product — and we require that
product to clear the margin `M`. One inequality, both classes.

### How this matches the `≥ 1` version above

```
 Normalised form:   ΣWᵢ² = 1,   maximise M,   yᵢ(W·xᵢ) ≥ M
 Scaled form:       margin = 2/‖W‖,  minimise ‖W‖,  yᵢ(W·xᵢ + c) ≥ 1
```

They're the **same problem** in two skins. The lecture normalises the weights and
maximises the distance `M` directly; the geometry section above instead fixes the
margin edge at `1` and shrinks `‖W‖`. Both land on the identical maximum-margin line.

---

## When Maximal Margin Is Impossible

Maximal margin assumes the classes *can* be perfectly split by a straight line. Often
they can't — the classes are **intermingled**:

```
   X₂ │      +  +
      │   •    + +
      │  •  • •   +   •          ← reds and blues overlap;
      │  •  •      +  +  +          no straight line cleanly
      │   •   •  +   +              separates them
      │     •  +
      └──────────────────── X₁
```

Here **no** maximal-margin hyperplane exists — any straight line *must* misclassify a
few points (some will fall on the wrong side). The hard-margin demand "zero violations"
has no solution.

> The fix: deliberately *allow* a few misclassifications in exchange for a robust,
> workable boundary — the **Soft Margin Classifier** → [[4bSoftMarginAndC]].

---

## Summary

```
Maximum-margin classifier:
  • Of all separating hyperplanes, choose the one with the WIDEST margin.
  • Margin = distance to the nearest point on each side.
  • Support vectors = points on the margin edges; they alone fix the boundary.
  • Wider margin → better generalisation.

  Hard margin = no violations allowed → needs perfectly separable data, brittle.

  Geometry:  margin = 2/‖W‖  →  maximise margin = minimise ‖W‖.
```

> **Next:** real data overlaps, so we relax "no violations" into a **soft margin**
> controlled by the hyperparameter `C` → [[4bSoftMarginAndC]]. See the companion
> notebook `4_MaximumMargin.ipynb`.
