# Recall Quiz — Hyperplanes & Linear Classification (M1)

Covers [[3aLinearClassificationNumericFeatures]] and [[3bHyperplaneIn2D]].
Try each before peeking at the answer.

---

## Q1 — Which side? (the key question)

> A straight line **L**, given by `y = w1·x + w0`, divides points of two classes
> **C1** and **C2** in 2D space. If point **(a, b) ∈ C1** and **(p, q) ∈ C2**, then which is true?

```
(A)  (b − w1·a − w0) · (q − w1·p − w0)  > 0
(B)  (b − w1·a − w0) · (q − w1·p − w0)  < 0
(C)  (a − w1·b − w0) · (p − w1·q − w0)  > 0
(D)  (a − w1·b − w0) · (p − w1·q − w0)  < 0
```

<details><summary>Answer</summary>

**(B)** — the product is **< 0**.

**Why.** Write the line as a decision function by moving everything to one side:

```
y = w1·x + w0   ⇒   f(x, y) = y − w1·x − w0
```

(This is the explicit-line version of the `W1·x1 + W2·x2 + c = 0` form from
[[3bHyperplaneIn2D]]: here `W1 = −w1`, `W2 = 1`, `c = −w0`.)

The **sign of f decides the class**:

```
f(point) > 0  → above the line  → one class
f(point) < 0  → below the line  → the other class
f(point) = 0  → on the line
```

- For (a, b): `f = b − w1·a − w0`
- For (p, q): `f = q − w1·p − w0`

Since (a, b) and (p, q) are in **different** classes, they lie on **opposite sides**
of L, so their f-values have **opposite signs**. A positive times a negative is
**negative** → the product is `< 0`.

Options (C)/(D) are wrong because they swap x and y (they plug `a` where `x` should
be `b`, etc.) — that's not the line's decision function.

```
   y
   │      • (a,b) ∈ C1      f = b − w1a − w0  > 0   (above)
   │    ╱
   │  ╱   L: y = w1x + w0
   │╱
   │   ╳ (p,q) ∈ C2         f = q − w1p − w0  < 0   (below)
   └──────────────── x         product = (+)(−) < 0   ✓
```
</details>

---

## Q2 — What is a hyperplane?

> In a 2D feature space, what geometric object is the hyperplane, and what is it in n-D?

<details><summary>Answer</summary>

```
2D → a line
3D → a plane
nD → an (n−1)-dimensional hyperplane
```

It is the **boundary that separates the classes**. In SVM/logistic regression it
**is the model** you are building. See [[3bHyperplaneIn2D]].
</details>

---

## Q3 — Why must features be numeric?

> Why do SVMs require all attributes in numeric form? What do you do with a categorical feature?

<details><summary>Answer</summary>

An SVM places each sample as a **point in feature space** and draws a hyperplane —
you can only give a point coordinates if every attribute is a **number**.

Non-numeric features are converted in **data prep**:
one-hot (categories), ordinal/label encoding (ordered), TF-IDF / word-frequency (text).
See [[3aLinearClassificationNumericFeatures]].
</details>

---

## Q4 — Reading the decision value

> For `f(x) = W1·x1 + W2·x2 + c`, what do `f(x) > 0`, `f(x) < 0`, and `f(x) = 0` mean?

<details><summary>Answer</summary>

```
f(x) > 0  → class A (one side, e.g. blue / spam)
f(x) < 0  → class B (other side, e.g. red / ham)
f(x) = 0  → the point lies exactly ON the hyperplane
```

The **sign** is the prediction; the W coefficients and c are what the model learns.
</details>

---

## Q5 — Three candidate lines (margin teaser)

> The plot shows **three** different lines that all separate spam from ham equally well
> on the training data. If they all separate the data, which one should we prefer — and why?

<details><summary>Answer</summary>

Prefer the line with the **widest margin** — the largest gap to the nearest points of
each class. All three may have zero training error, but the maximum-margin line
**generalises best** to new emails. This is exactly the SVM idea (the *maximum-margin
classifier*) — see [[2SVMMotivation]]. Choosing it well is also a
**bias-variance** balance — see [[1BiasVsVariance]].
</details>

---

## Q6 — Why standardise before SVM?

> `word_freq_free` ranges ~0–5 but `capital_run_length_total` runs into the thousands.
> Why is feeding these raw to an SVM a problem?

<details><summary>Answer</summary>

SVM is **distance-based**. A feature with a huge range dominates the distance maths and
**hijacks the boundary**, drowning out small-range features. **Standardise**
(mean 0, std 1) so every feature gets a fair say. See
[[3aLinearClassificationNumericFeatures]].
</details>

---

## Score yourself

```
6/6 → solid. Ready for 3D hyperplanes & the maximum-margin maths.
4–5 → reread 3bHyperplaneIn2D (the sign rule) — that's the crux.
≤3  → revisit 3a + 3b and run both companion notebooks.
```

> **Next:** hyperplanes in 3D, then *which* separating hyperplane is best (maximum margin).
