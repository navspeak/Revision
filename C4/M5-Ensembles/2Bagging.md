# Bagging — Bootstrap Aggregating

Bagging is the simpler ensemble strategy. Train many models on **different random samples**, then combine their predictions.

```
"Bagging" = "Bootstrap Aggregating"
   Bootstrap  → sampling with replacement
   Aggregate  → combine predictions (vote / average)
```

The key insight: a single model trained on one specific dataset can give an **unreliable picture** because it learns patterns too tightly tied to that sample. Many models trained on slightly different samples cancel out this instability.

---

## The Weight-Guessing Analogy

```
One person guesses an object's weight → may be way off (10 lbs too high)
Another guesses → may be way off (8 lbs too low)
Average 100 guesses → very close to the truth
```

Individual guesses are noisy. But the **average** of many noisy guesses converges to the truth — that's the wisdom of crowds.

Bagging applies this idea to ML models.

---

## How Bagging Works — Step by Step

```
1. Have a training set with N rows.

2. Create K bootstrap samples:
   - Each is N rows drawn WITH REPLACEMENT from the training set.
   - Each sample is roughly the same size as the original, but contains
     some duplicates and misses some rows entirely (~63% unique on average).

3. Train one model on each bootstrap sample.
   → K different models.

4. To predict on a new point:
   - Classification: each model votes; majority wins.
   - Regression: take the average of all model predictions.
```

```
Training set:
   [A, B, C, D, E, F, G, H, I, J]

Bootstrap 1: [A, A, C, D, E, F, F, G, H, J]   → train Model 1
Bootstrap 2: [B, B, C, C, D, E, G, H, I, J]   → train Model 2
Bootstrap 3: [A, B, B, C, E, E, F, G, I, I]   → train Model 3
...
Bootstrap K: ...                               → train Model K

New point → ask all K models → majority vote / average
```

---

## What Bagging Achieves — Variance Reduction

A single model has **high variance** — small changes in training data give wildly different predictions:

```
Tree trained on dataset A → predicts class 1
Tree trained on dataset A' (slightly different) → predicts class 0
```

Each bagged model has the same problem individually. But averaging across K models **stabilises** the prediction:

```
Bias of one model        = Bias of the ensemble (unchanged)
Variance of one model    ≈ V
Variance of K bagged     ≈ V/K (when models are independent)
```

Variance shrinks roughly by `1/K`. Bias stays the same. So **error goes down** — that's the whole point.

For variance reduction to work, the models need to be **somewhat independent**. Bootstrap sampling creates that independence — each tree sees a different sample.

---

## Why It Works for Unstable Models

Bagging shines with **high-variance, low-bias** learners — models that overfit easily:

```
Single deep decision tree:  low bias (fits well), high variance (unstable)
                            → IDEAL for bagging

Linear regression:          higher bias, low variance
                            → bagging helps LESS
```

That's why **decision trees** are the go-to base learner for bagging — they're naturally unstable, exactly the situation bagging fixes.

---

## A Simple Worked Example

Imagine predicting if a student passes (Yes/No) based on hours studied:

```
Tree 1 (bootstrap 1): predicts Yes
Tree 2 (bootstrap 2): predicts Yes
Tree 3 (bootstrap 3): predicts No

Majority vote → Yes ✓
```

Even though Tree 3 made a mistake, the ensemble corrects for it. As long as more trees are right than wrong, the vote is correct.

---

## Bagging vs Random Forest

Random Forest is a **specific kind of bagging** — bagging applied to decision trees, with one extra ingredient:

```
Bagging (general)        → bootstrap + any base model
Random Forest            → bootstrap + decision trees + random feature subsets at each split
```

The "random feature subsets" make trees even more diverse. More on this in `3RandomForest.md`.

---

## Summary

```
Bagging        = train many models on bootstrap samples → combine predictions
Reduces        → VARIANCE (errors cancel)
Best when      → base model is unstable / high-variance
Combine via    → majority vote (classification) or mean (regression)
Default choice → decision trees → Random Forest
```

> Bagging's whole job is making unstable learners stable. The deeper the trees, the more bagging helps.
