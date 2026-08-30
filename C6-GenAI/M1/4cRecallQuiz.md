# Recall Quiz — Maximum Margin & Its Constraints (M1)

Covers [[4aMaximumMarginClassifier]] (and sets up [[4bSoftMarginAndC]]).
Try each before peeking at the answer.

---

## Q1 — Which separating line does SVM pick?

> Several straight lines separate the two classes with zero training error.
> Which one does the maximum-margin classifier choose, and why that one?

<details><summary>Answer</summary>

The line with the **widest margin** — the largest perpendicular gap to the nearest
point of **either** class.

```
Wider street between the classes
   → more room before a new point crosses the boundary
   → better GENERALISATION on unseen data.
```

Hugging one class would misclassify the instant a new point lands just over the line.
See [[4aMaximumMarginClassifier]].
</details>

---

## Q2 — Constraint 1: why `ΣWᵢ² = 1`?

> The maximal-margin formulation requires the coefficients to satisfy `∑ Wᵢ² = 1`.
> What is this constraint for?

<details><summary>Answer</summary>

It **normalises the weight vector to unit length**.

Scaling all the `W`s up or down describes the *same* line but changes the raw score
`W₀ + W₁x₁ + W₂x₂`. Fixing `ΣWᵢ² = 1` pins the scale so that the score equals the
**actual perpendicular distance** from a point to the hyperplane.

```
Without it → M is an arbitrary number (you could rescale W to make it anything).
With it    → M is a real geometric margin (a distance you can compare).
```
</details>

---

## Q3 — Constraint 2: what does `lᵢ·(Wᵢ·Yᵢ) ≥ M` say?

> Decode the second constraint `lᵢ · (Wᵢ · Yᵢ) ≥ M`. What is each symbol, and what does
> the whole inequality demand?

<details><summary>Answer</summary>

```
lᵢ = the label  (+1 or −1)
Wᵢ = the coefficients (the hyperplane)
Yᵢ = the point's feature values (one row of data)
M  = the margin (the safe distance we are maximising)
```

It demands that **every** point sit on the **correct side** *and* at least a full
margin `M` away from the hyperplane. It's the §2.2 correctness condition
(`label × score > 0`) tightened from "merely correct" to "correct with `M` clearance".
See [[2SVMMotivation]].
</details>

---

## Q4 — The sign trick (Figures A & B)

> A red point `Y(p,q)` has label `−l` and sits **below** the line, so
> `W₀ + W₁p + W₂q < 0`. A blue point has label `+l` and sits **above**, so its score is
> `> 0`. Show that the **same** inequality `label × score ≥ M` holds for both.

<details><summary>Answer</summary>

```
RED  (Fig A):  label = −l,  score < 0
   −l × (W₀ + W₁p + W₂q)  =  (neg) × (neg)  =  POSITIVE  ≥ M   ✓

BLUE (Fig B):  label = +l,  score > 0
   +l × (W₀ + W₁p + W₂q)  =  (pos) × (pos)  =  POSITIVE  ≥ M   ✓
```

The label's sign **cancels** the score's sign, so a correctly-classified point always
gives a positive product — for *both* classes. One inequality covers them both; we
just require that product to clear `M`. See [[4aMaximumMarginClassifier]].
</details>

---

## Q5 — `≥ M` vs `≥ 1`

> One source writes the constraint as `yᵢ(W·xᵢ) ≥ M` with `ΣWᵢ²=1`; another writes
> `yᵢ(W·xᵢ + c) ≥ 1` with `margin = 2/‖W‖`. Are these different methods?

<details><summary>Answer</summary>

**No — same problem, two skins.**

```
Normalised form:  ΣWᵢ² = 1,  MAXIMISE M,        yᵢ(W·xᵢ)     ≥ M
Scaled form:      margin = 2/‖W‖,  MINIMISE ‖W‖,  yᵢ(W·xᵢ+c)  ≥ 1
```

The first normalises the weights and maximises the distance `M` directly. The second
fixes the margin edge at `1` and shrinks `‖W‖` (since `margin = 2/‖W‖`, smaller `‖W‖`
= wider margin). Both solve for the **identical** maximum-margin hyperplane.
</details>

---

## Q6 — What are support vectors here?

> In terms of the constraint, which training points are the **support vectors**?

<details><summary>Answer</summary>

The points for which the constraint is **tight** — equality holds:

```
yᵢ (W·xᵢ + c) = 1     (equivalently  lᵢ·(Wᵢ·Yᵢ) = M)
   → the point sits exactly ON the margin edge.
```

Only these points define the hyperplane. Move a non-support-vector → boundary
unchanged; move a support vector → boundary shifts. See [[4aMaximumMarginClassifier]].
</details>

---

## Q7 — When does maximal margin break?

> Sketch (mentally) two classes whose points are **intermingled**. Can the maximal
> margin classifier find a hyperplane? What is the consequence, and the fix?

<details><summary>Answer</summary>

**No valid hyperplane exists.** If the classes overlap, *no* straight line puts every
point on the correct side — the hard constraint `lᵢ·(Wᵢ·Yᵢ) ≥ M` has **no solution**.
Any linear boundary **must** misclassify a few points.

```
Hard margin → demands zero violations → fails on overlapping / noisy data.
Fix         → deliberately ALLOW a few misclassifications → Soft Margin Classifier.
```

→ [[4bSoftMarginAndC]] (the `C` hyperparameter controls how many violations are
tolerated — a direct bias-variance knob, see [[1BiasVsVariance]]).
</details>

---

## Score yourself

```
7/7 → solid. The two constraints + the sign trick are locked in. On to soft margin.
5–6 → reread the "Two Constraints" + "Figure A/B" sections of 4a.
≤4  → revisit 4a end-to-end and replay 4_MaximumMargin.ipynb.
```

> **Next:** relax "no violations" into the **soft margin** controlled by `C`
> → [[4bSoftMarginAndC]], then **kernels** for non-linear data (5-series).
