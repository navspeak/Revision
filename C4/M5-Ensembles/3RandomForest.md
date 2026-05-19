# Random Forest

Random Forest = **bagging + decision trees + random feature subsets**.

It's the most popular ensemble method — strong baseline accuracy, robust, almost no tuning needed to get good results.

---

## The Recipe

```
1. Bootstrap sampling
   - Draw N samples WITH replacement from the training data.
   - Repeat for each tree → each tree sees a different sample.

2. Random feature subsets
   - At EACH split in EACH tree, only a random subset of features is
     considered for the best-split decision.
   - For classification: typically sqrt(p) features per split
   - For regression: typically p/3 features per split

3. Train each tree fully (often unbounded depth)
   - Trees can overfit individually — that's fine, bagging handles it.

4. Aggregate predictions
   - Classification: majority vote (or average predicted probabilities)
   - Regression: average of predictions
```

---

## Concrete End-to-End Example

Predict whether a student **passes** (Pass=1 / Fail=0) using 3 features: `Hours`, `PrevGrade`, `Attendance`.

### Training data (8 rows)

| Row | Hours | PrevGrade | Attendance | Pass |
|-----|-------|-----------|------------|------|
| 1 | 5 | 75 | 90 | 1 |
| 2 | 2 | 60 | 70 | 0 |
| 3 | 6 | 80 | 95 | 1 |
| 4 | 1 | 55 | 60 | 0 |
| 5 | 4 | 70 | 85 | 1 |
| 6 | 3 | 65 | 75 | 0 |
| 7 | 7 | 85 | 100 | 1 |
| 8 | 2 | 58 | 65 | 0 |

We'll build a Random Forest with **3 trees**.

### Step 1 — Bootstrap each tree's training data

Sample 8 rows WITH replacement (so duplicates are OK, some rows are skipped):

```
Tree 1's bootstrap: rows [1, 3, 3, 5, 5, 7, 2, 8]   (row 4, 6 skipped; 3 and 5 doubled)
Tree 2's bootstrap: rows [2, 4, 6, 6, 8, 1, 3, 7]   (row 5 skipped; 6 doubled)
Tree 3's bootstrap: rows [4, 5, 1, 1, 6, 2, 7, 8]   (row 3 skipped; 1 doubled)
```

Each tree sees a different mix of training data.

### Step 2 — Random feature subset at every split

3 features → `sqrt(3) ≈ 1.7` → use **2 features per split**. At each split, pick 2 of the 3 features at random.

```
Tree 1, root:        consider {Hours, Attendance}   (PrevGrade not picked this time)
                     best split → Hours > 3.5

Tree 1, left child:  consider {Hours, PrevGrade}    (Attendance not picked)
                     best split → PrevGrade > 70

Tree 2, root:        consider {PrevGrade, Attendance}
                     best split → Attendance > 80

Tree 3, root:        consider {Hours, PrevGrade}
                     best split → PrevGrade > 65
```

Each tree splits on different features — that's the diversity Random Forest creates.

### Step 3 — Train each tree fully

Each tree grows until pure (or hits some stopping rule). The trees end up structurally different:

```
Tree 1:                  Tree 2:                  Tree 3:
   Hours > 3.5?              Attendance > 80?        PrevGrade > 65?
   /       \                 /         \             /         \
 Fail   PrevGrade > 70?    Fail    Hours > 4?      Fail      Hours > 5?
        /        \                  /     \                   /     \
      Fail     Pass               Fail   Pass               Fail    Pass
```

Each tree has its own decision rules.

### Step 4 — Predict on a new student

```
New point: Hours = 4.5, PrevGrade = 72, Attendance = 88
```

Route through each tree:

```
Tree 1:
   Hours > 3.5? → 4.5 > 3.5 → YES
   PrevGrade > 70? → 72 > 70 → YES
   → Pass (probability 0.85)

Tree 2:
   Attendance > 80? → 88 > 80 → YES
   Hours > 4? → 4.5 > 4 → YES
   → Pass (probability 0.70)

Tree 3:
   PrevGrade > 65? → 72 > 65 → YES
   Hours > 5? → 4.5 > 5 → NO
   → Fail (probability 0.40 for Pass)
```

### Aggregate the predictions

**Majority vote:**

```
Tree 1: Pass
Tree 2: Pass
Tree 3: Fail
→ 2 of 3 vote Pass → Predict Pass ✓
```

**Average probabilities (default in sklearn):**

```
P(Pass) = (0.85 + 0.70 + 0.40) / 3 = 0.65
→ 0.65 > 0.50 → Predict Pass ✓
```

Either method gives the same answer here. Even though Tree 3 was wrong, the **majority correction** saves the prediction.

### Same Recipe for Regression

If the target were a number (e.g. **final exam score**), the procedure is identical except the final step:

```
Tree 1: predicts 78
Tree 2: predicts 82
Tree 3: predicts 70

Final prediction = average = (78 + 82 + 70) / 3 = 76.7
```

That's the complete Random Forest pipeline in one example.

---

## Why the Random Feature Subsets?

Pure bagging gives each tree a different sample — but if one feature is **strongly predictive** (say `BP > 120`), almost every tree will pick it as the root split.

Result: trees are **too similar** despite different samples. Less diversity → less variance reduction.

Random Forest fixes this by **forcing trees to use different features**:

```
At each split, only a random subset of features can be used.

Tree 1's root might be   BP > 120
Tree 2's root might be   Age > 50    ← BP not in the subset for this split
Tree 3's root might be   Cholesterol > 200
```

This makes trees genuinely diverse — and that's what makes their average so accurate.

---

## Prediction Example — Classification

A new point arrives. Each tree votes:

```
Tree 1: predicts class A (probability 0.8)
Tree 2: predicts class B (probability 0.6)
Tree 3: predicts class A (probability 0.7)
Tree 4: predicts class A (probability 0.9)
Tree 5: predicts class B (probability 0.55)

Average probabilities:
   P(A) = (0.8 + 0.4 + 0.7 + 0.9 + 0.45) / 5 = 0.65
   P(B) = (0.2 + 0.6 + 0.3 + 0.1 + 0.55) / 5 = 0.35

Predicted class → A
```

For multiclass, same idea — average probabilities across all classes, pick the highest.

---

## Prediction Example — Regression

```
Tree 1: predicts 95
Tree 2: predicts 102
Tree 3: predicts 88
Tree 4: predicts 96
Tree 5: predicts 100

Final prediction = average = (95+102+88+96+100)/5 = 96.2
```

That's the whole "aggregate" step for regression — just the mean.

---

## Hyperparameters

The main ones — and rough guidance:

| Hyperparameter | sklearn name | Typical | Effect |
|----------------|--------------|---------|--------|
| Number of trees | `n_estimators` | 100–500 | More = better (with diminishing returns) |
| Max depth per tree | `max_depth` | None or 10–20 | Limits individual tree complexity |
| Features per split | `max_features` | `'sqrt'` (clf), `1.0`/p/3 (reg) | Controls diversity |
| Min samples per split | `min_samples_split` | 2 | Standard pre-pruning |
| Min samples per leaf | `min_samples_leaf` | 1–5 | Stabilises leaf predictions |
| Bootstrap | `bootstrap` | True | Use bootstrap sampling |
| OOB scoring | `oob_score` | True | Built-in validation (see `4EvaluatingRF.md`) |
| Random state | `random_state` | 42 | Reproducibility |
| Parallel jobs | `n_jobs` | -1 | Train trees in parallel |

In sklearn:

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    max_features='sqrt',
    bootstrap=True,
    oob_score=True,
    n_jobs=-1,
    random_state=42
)
model.fit(X_train, y_train)
```

---

## Why It Just Works

Random Forest is often called a "fire-and-forget" method:

```
✓ Works well out of the box
✓ Not very sensitive to hyperparameters
✓ Hard to overfit (more trees → more stability, not more overfit)
✓ Handles mixed numerical / categorical data
✓ Robust to noise and outliers
✓ No feature scaling needed
✓ Built-in feature importance + OOB error
✓ Parallelisable — trains fast on modern hardware
```

A solid baseline before considering more complex models like Gradient Boosting.

---

## When to Use Random Forest

```
✓ Tabular data with many features
✓ Need accuracy without much tuning effort
✓ Want feature importance for interpretability
✓ Some categorical features mixed in with numerical
✓ Noisy data with outliers
```

```
✗ Need extrapolation beyond training range → RF can't extrapolate
✗ Very high-dimensional sparse data (text) → linear models often better
✗ Need the absolute highest accuracy → boosting often wins
✗ Need a single interpretable tree → use one Decision Tree instead
```

---

## Summary

```
Random Forest =
   1. Bootstrap sample data for each tree
   2. Random feature subset at each split
   3. Train many trees in parallel
   4. Average / vote their predictions

Key strength: variance reduction via diverse trees
Trade-off: lose single-tree interpretability, but gain accuracy and stability
```

> Random Forest is the **strong, low-effort baseline** for tabular ML. Always try it before reaching for anything fancier.
