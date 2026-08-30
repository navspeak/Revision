# Motivation for SVM — Why Support Vector Machines?

Support Vector Machines (SVMs) are a class of **extremely popular classification models**. Besides solving complex problems, they bring several advantages over other classifiers:

```
✓ Handle high-dimensional feature spaces well
✓ Classify non-linearly separable data (via the kernel trick)
✓ Robust — decisions driven by a few key points, not all of them
```

We explore these in the upcoming notes.

---

## SVMs Are a LINEAR Model

This is the most important thing to remember.

```
SVM            → linear model
Logistic Reg.  → linear model
```

"Linear" refers to **how the model combines the features** — a weighted sum — *not* to the shape of anything you plot.

A **linear model** builds its decision from a weighted sum of the inputs:

```
z = w₁x₁ + w₂x₂ + … + wₙxₙ + b
```

Each feature `xᵢ` appears to the first power, just scaled by a weight `wᵢ` and added up — no x², no x₁·x₂, no sin(x). The familiar `y = ax + b` is simply the 1-feature version of this: `a` is the weight, `b` is the intercept/bias.

### Logistic regression is linear

The **log(odds)** is the linear part:

```
log( p / (1−p) ) = w₁x₁ + w₂x₂ + … + b
```

The output probability `p` is squashed through a sigmoid (curvy), but the thing being modeled — log(odds) — is a *straight* linear combination of the attributes (e.g. defaulting on a credit card). So we still call it linear; the non-linearity lives only in the final link function.

### SVM is linear

An SVM decides the same way, then takes the sign:

```
ŷ = sign( w₁x₁ + … + wₙxₙ + b )
```

The boundary is the set of points where `wᵀx + b = 0` — a **hyperplane** (a line in 2D, a plane in 3D, flat in higher dimensions). A flat boundary ⇒ linear model.

### Why this matters for the upcoming lectures

A purely linear SVM can **only** draw flat boundaries — but lots of data isn't separable by a straight line:

```
   o o o
  o  x  o      ← x's surrounded by o's:
   o o o          no straight line separates them
```

The **kernel** lectures resolve this without abandoning linearity: transform the features into a higher-dimensional space where the classes *do* become linearly separable, then apply the same linear SVM there. The boundary looks curved back in the original space, but it's still a linear model underneath.

> That's why "SVM is a linear model" must be cemented now — the kernel trick only makes sense as *keep the linear machinery, change the space it operates in.*

---

## 2.1 Classification — The Decision Rule

The classification rule turns the weighted score into an actual class label. Three steps:

```
1. Score    z = wᵀx + b = w₁x₁ + w₂x₂ + … + wₙxₙ + b
2. Sign     ŷ = sign(z)
3. Label    +1 = one class,  −1 = the other
```

```
        wᵀx + b > 0          ← positive side  → predict +1
   ───────────────────────   ← the boundary (wᵀx + b = 0)
        wᵀx + b < 0          ← negative side  → predict −1
```

The rule is literally **"which side of the hyperplane are you on?"** The vector `w`
points toward the `+1` side; `b` shifts the boundary away from the origin.

- **Sign → the label.** Positive vs negative tells you the class.
- **Magnitude → the confidence.** The larger `|wᵀx + b|`, the further the point sits
  from the boundary, so the more confident the prediction. Points right on the margin
  edges are the **support vectors** (see below).

### Same score, different final step

Both SVM and logistic regression compute the identical score `z = wᵀx + b` — they
only differ in what they do with it:

| | Score `z` | Final step | Output |
|-|-----------|------------|--------|
| **SVM** | `wᵀx + b` | `sign(z)` | class `±1` |
| **Logistic Reg.** | `wᵀx + b` | `sigmoid(z)`, threshold at 0.5 | probability → class |

> Both decide by *which side of the hyperplane* a point falls on — exactly why both
> are linear models. SVM commits to a hard sign; logistic regression squashes to a
> probability first.

---

## 2.2 The Correctness Condition — `y·(wᵀx + b)`

A neat trick lets us write *"this point is correctly classified"* as a **single
inequality**. The secret is coding the true label `y` as `+1` or `−1` (not 0/1).

Multiply the **score** by the **true label** and watch the sign:

```
True label y    Score wᵀx+b    Product (wᵀx+b)·y   Meaning
─────────────────────────────────────────────────────────────
   +1            positive (+)      (+)(+) = +        ✓ correct
   −1            negative (−)      (−)(−) = +        ✓ correct
   +1            negative (−)      (−)(+) = −        ✗ wrong
   −1            positive (+)      (+)(−) = −        ✗ wrong
```

```
y·(wᵀx + b) > 0   ⇔  classified CORRECTLY   (score & label agree → same sign)
y·(wᵀx + b) < 0   ⇔  MISclassified          (opposite signs)
```

**Why it collapses two rules into one.** Without the trick you'd need a separate
condition per class:

```
wᵀx + b > 0   for positive-class points
wᵀx + b < 0   for negative-class points
```

The `±1` encoding folds both into one condition the optimiser can use directly:

```
yᵢ·(wᵀxᵢ + b) > 0      for every training point i   ("all points on the correct side")
```

### Tightening it for the margin

The maximal-margin classifier doesn't just want *correct* — it wants every point a
full margin's distance away. This is the **second constraint** in the lecture-notes
maximal-margin formulation:

```
yᵢ·(wᵀxᵢ + b) ≥ 1      for all i

   y(wᵀx+b) ≥ 1     → correct AND outside the margin (safe)
   y(wᵀx+b) = 1     → sits exactly ON the margin edge → SUPPORT VECTOR
0< y(wᵀx+b) < 1     → correct but INSIDE the margin (a soft-margin violation)
   y(wᵀx+b) < 0     → wrong side entirely (misclassified)
```

The quantity `y·(wᵀx + b)` is called the **functional margin** of a point. "Maximum
margin" means pushing the *smallest* functional margin across all points as large as
possible.

> One-liner: coding labels as `±1` turns *"correctly classified"* into `y·(wᵀx+b) > 0`
> — one inequality instead of two, and its **size** measures how confidently the point
> is classified. This is the bridge into the maximum-margin maths. See [[4aMaximumMarginClassifier]].

---

## The Core Idea — Best Separating Line

Many lines can separate two classes. Which one is "best"?

```
        Class A (•)                Class A (•)
   •  •                       •  •
   •  •  \                    •  •  ┊
   •  •   \     ✗ bad          •  • ┊      ✓ good
          \   (too close      ┊┊┊┊┊┊┊  ← widest gap
   ╳  ╳    \   to points)     ┊    ┊
   ╳  ╳     \                 ╳  ╳ ┊
   ╳  ╳      Class B (╳)      ╳  ╳ Class B (╳)
```

SVM picks the line with the **widest margin** — the largest gap between the two classes. This is why it's also called a **maximum margin classifier**.

---

## Why "Support Vector"?

```
        • •
        • •  ←─────┐
      ──────────   │  margin
      │ MARGIN │   │
      ──────────   │
        ╳ ╳  ←─────┘
        ╳ ╳

The points sitting ON the margin edges = "support vectors".
They alone define the boundary. Move any OTHER point → boundary unchanged.
```

Only a handful of points (the support vectors) matter. This makes SVM:

- **Memory-efficient** — stores only the support vectors
- **Robust** — far-away points don't sway the decision

---

## Why Not Just Use Logistic Regression?

| | Logistic Regression | SVM |
|-|---------------------|-----|
| Boundary | Any separating line | **Maximum-margin** line |
| Output | Probability (0–1) | Class label (+ distance) |
| High dimensions | Struggles | **Strong** |
| Non-linear data | Needs manual feature engineering | **Kernel trick** handles it |
| Outlier sensitivity | Sensitive | More robust (margin-based) |

---

## Where SVM Shines

```
✓ Text / spam classification (high-dimensional, sparse features)
✓ Image & handwriting / letter recognition
✓ Bioinformatics (gene classification, many features, few samples)
✓ Any task where the number of features is large vs samples
```

> The module includes worked notebooks: **SVM Letter Recognition**,
> **SVM Spam Classification (linear & non-linear)**, alongside **Naive Bayes**.

---

## Summary

```
SVM = a LINEAR classifier that finds the MAXIMUM-MARGIN boundary.

Key ideas:
  • Linear model (like logistic regression) — line / plane / hyperplane
  • Maximises the margin → best generalisation
  • Defined only by "support vectors" → robust & efficient
  • Kernel trick (later) → handles non-linear data
  • Excels in high-dimensional spaces
```

> Next: the maths of the maximum-margin classifier, then soft margins (the `C` parameter), then kernels. See [[1BiasVsVariance]] — the `C` parameter is exactly a bias-variance knob.
